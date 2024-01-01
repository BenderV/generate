import csv
import os
from inspect import cleandoc
from io import StringIO
from textwrap import dedent
from typing import List

import langchain
import yaml
from langchain.cache import SQLAlchemyCache
from langchain.chains import LLMChain, SequentailChainWithPreviousContext
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from sqlalchemy import create_engine
from transformers import GPT2TokenizerFast

os.environ["TOKENIZERS_PARALLELISM"] = "false"

LOGIT_BIAS = {}
UNWANTED_WORDS = [
    "etc",
    "rows",
    "...",
    "....",
    ".....",
    "......",
    ".......",
    "........",
    ".........",
    ".............",
]
# Add words with leading space if the word is 3 characters or less
UNWANTED_WORDS += [f" {word}" for word in UNWANTED_WORDS if len(word) <= 3]


def get_logit_bias():
    # Load the tokenizer
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    # Generate tokens from UNWANTED_TOKENS, with a logit_bias of -100 if there is only one token
    for word in UNWANTED_WORDS:
        tokens = tokenizer(word)["input_ids"]
        if len(tokens) == 1:
            LOGIT_BIAS[tokens[0]] = -100
        else:
            print(f"WARNING: {word} is not a single token. Skipping")


get_logit_bias()

# Create a database engine
engine = create_engine(os.environ["DATABASE_URL"])
# Avoid caching for now
langchain.llm_cache = SQLAlchemyCache(engine)

ESTIMATED_ROWS_TEMPLATE = """
Try to estimate the number of rows for each entities.
Precision is from 0 (can't know) to 1 (perfectly known)
If there is a number in the title, use it as a hint.

FORMAT YAML
precision: float
rows: integer

### 

Estimation of size: "belgium cities (top 10)"
precision: 1
rows: 10 
---

Estimation of size: "planets in the solar system"
precision: 1
rows: 8
---

Estimation of size: "car brand"
precision: 0.9
rows: 90
---

Estimation of size: "countries"
precision: 0.8
rows: 195
---

Estimation of size: "{{ title }}"
"""


llm = OpenAI(temperature=0, stop=["---"])
llmCSV = OpenAI(
    temperature=0,
    max_tokens=3500,
    stop=["---"],
    logit_bias=LOGIT_BIAS,
)


def generate_data(title: str, fields: List[dict]) -> list:
    chains = []
    template = cleandoc(
        """
        Question: If someone ask for a list of "{{title}}" with theses fields:
        {% for field in fields %}
        * {{ field.name }}: {{ field.type }} ({{ field.description }}){% endfor %}
        
        What are they expecting ? (explain without examples)
        Format: string
        Response: 
    """
    )

    prompt = PromptTemplate(
        template_format="jinja2",
        template=template,
        input_variables=["title", "fields"],
    )
    chains.append(LLMChain(llm=llm, prompt=prompt, output_key="expecting"))

    template = "\n\n" + cleandoc(
        """
        Question: Examples (max 3):\n
        Format: string
        Response: 
    """
    )
    prompt = PromptTemplate(template=template)
    chains.append(LLMChain(llm=llm, prompt=prompt, output_key="examples"))

    template = "\n\n" + cleandoc(
        """
        Question: What is the size / range implied or usual for this list ? (guess with a number / range)
        Format: integer
        Template: the maximum number of rows is XX rows.
        Response: the maximum number of rows is 
        """
    )

    prompt = PromptTemplate(template=template)
    chains.append(LLMChain(llm=llm, prompt=prompt, output_key="estimated_size"))

    fchain = SequentailChainWithPreviousContext(
        chains=chains,
        verbose=True,
        input_variables=["title", "fields"],
        output_variables=["expecting", "examples", "estimated_size"],
    )

    fchain_result = fchain(
        {
            "title": title,
            "fields": fields,
        }
    )

    metadata = {}
    expected_rows = "unknown (max 100)"
    try:
        metadata["estimated_size"] = int(
            fchain_result["estimated_size"]
            .replace("rows.", "")
            .replace(" ", "")
            .replace(",", "")  #  10,000 rows.
            .strip()
        )
        expected_rows = min(metadata["estimated_size"], 100)
    except Exception as e:
        print(e)
        pass

    template = "\n\n" + cleandoc(
        """
    Now, this person ask you for the full CSV
    Using this CSV Config:
    - Separator is ";" (semicolon)
    - Integer should be without "," (comma)
    - Float should use . (dot) as decimal separator
    - You can't use "..." and skip rows
    Close the CSV with a new line "---"

    FULL {{title_slug}}.csv
    LENGTH: {{ expected_rows }} rows
    OUTPUT:
    {{ fields | map(attribute="name") | join(";") }}

    """
    )

    template = PromptTemplate(
        template_format="jinja2",
        template=fchain.context + template,
        input_variables=["title_slug", "fields", "expected_rows"],
    )
    prompt = template.format(
        title_slug=title.lower().replace(" ", "_"),
        fields=fields,
        expected_rows=expected_rows,
    )
    prompt += "\n"  # Add a new line to make sure the header is not in the same line as the prompt
    csv_result = llmCSV(prompt).strip()
    # If one line, it's a error
    # Try to split by ";" if there is only one line and one column
    if "\n" not in csv_result and len(fields) == 1:
        csv_result = csv_result.replace(";", "\n")

    f = StringIO(";".join([f["name"] for f in fields]) + "\n" + csv_result)
    reader = csv.DictReader(f, delimiter=";")

    rows = [row for row in reader]
    columns_types = {f["name"]: type_mapper(f["type"]) for f in fields if f.get("type")}
    rows = [cast_dict_columns(row, columns_types) for row in rows]

    # Limit to max 100 rows
    rows = rows[:100]
    return rows, metadata


def cast_dict_columns(data: dict, columns: dict) -> dict:
    result = {}
    for column, column_type in columns.items():
        if column in data and isinstance(data[column], column_type):
            result[column] = data[column]

        try:
            if column_type == bool:
                result[column] = str2bool(data[column])
            elif column_type == int:
                # Handle int('11.5')
                result[column] = int(float(data[column]))
            else:
                result[column] = column_type(data[column])
        except Exception as e:
            print(e)
            result[column] = None
    return result


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError("Boolean value expected.")


def type_mapper(type_name: str):
    """Map type name to python type"""
    if type_name == "integer":
        return int
    elif type_name == "float":
        return float
    elif type_name == "string":
        return str
    elif type_name == "boolean":
        return bool
    else:
        raise ValueError(f"Unknown type {type_name}")
