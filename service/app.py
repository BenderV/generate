import difflib
from datetime import datetime

from ai import generate_data
from fields import guess_fields
from flask import Flask, jsonify, request
from model import Extract, FormSubscriptions
from peewee import fn
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def calculate_similarity(s1, s2):
    # Create a SequenceMatcher object and calculate the ratio of matching characters
    matcher = difflib.SequenceMatcher(None, s1, s2)
    ratio = matcher.ratio()
    return ratio


def deduplicate(objects, field, similarity_threshold):
    unique_objects = []

    for obj in objects:
        similar = False
        for other_obj in unique_objects:
            similarity = calculate_similarity(obj[field], other_obj[field])
            if similarity > similarity_threshold:
                similar = True
                break
        if not similar:
            unique_objects.append(obj)

    # Return the sorted list of unique objects
    return unique_objects


@app.route("/generate", methods=["POST"])
def generate_string():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    metadata = {}
    # Guess fields if not provided
    if not data.get("fields"):
        data["fields"] = guess_fields(data["title"])
        metadata["guessed_fields"] = True

    rows, metadata_generated = generate_data(**data)
    metadata = {**metadata, **metadata_generated}
    # Save to database
    extract = Extract.create(**data, output=rows, metadata=metadata)
    print(extract)
    return jsonify(model_to_dict(extract))


@app.route("/subscribe", methods=["POST"])
def submit_form():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    FormSubscriptions.create(**data)
    return "ok"


@app.route("/extracts/<int:extract_id>/review", methods=["POST"])
def review_extract(extract_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Check if extract exists
    try:
        extract = Extract.get(Extract.id == extract_id)
    except Extract.DoesNotExist:
        return jsonify({"error": "Extract not found"}), 404

    # Update extract
    extract.review = data["review"]
    extract.review_at = datetime.now()
    extract.save()
    return "ok"


# Route to access favorite generated extracts
# Take 100 random extracts, with Distinct title
@app.route("/extracts", methods=["GET"])
def get_all_extracts():
    extracts_subquery = Extract.select(Extract.id).distinct(Extract.title)
    extracts = (
        Extract.select()
        .where(Extract.id.in_(extracts_subquery))
        .order_by(fn.Random())
        .limit(60)
        .dicts()
    )

    # Remove extracts with backlisted words
    blacklist = [
        "jew",
        "race",
        "slave",
        "racism",
        "prejudice",
        "bigot",
        "bigoty",
        "bigotism",
        "bigoted",
        "ethnic",
        "ethnic cleansing",
        "ethnocentrism",
        "ethnic prejudice",
        "ethnocentric",
        "ethnocentricity",
        "racial",
        "racial discrimination",
        "racialism",
        "racialist",
        "raciocentricity",
        "murder",
        "racist",
        "skin",
        "cancel",
        "gay",
        "derville",
        "shit",
        "fuck",
        "stupid",
    ]
    extracts = [
        extract
        for extract in extracts
        if not any(word in extract["title"].lower() for word in blacklist)
    ]

    # Compare extract title, and remove those you are close (similarity > 0.9)
    deduplicated_extracts = deduplicate(extracts, "title", 0.8)

    # Only extract the first row of the field output
    for extract in deduplicated_extracts:
        if extract.get("output"):
            extract["sample"] = extract["output"][0]
            extract["size"] = len(extract["output"])
        else:
            extract["sample"] = None
            extract["size"] = 0
        del extract["output"]

    return jsonify(deduplicated_extracts[:42])


@app.route("/extracts/<int:extract_id>", methods=["GET"])
def get_extract(extract_id):
    try:
        extract = Extract.get(Extract.id == extract_id)
    except Extract.DoesNotExist:
        return jsonify({"error": "Extract not found"}), 404
    return jsonify(model_to_dict(extract))


@app.route("/extracts/<string:extract_slug>", methods=["GET"])
def get_extract_by_slug(extract_slug):
    try:
        extract = Extract.get(Extract.slug == extract_slug)
    except Extract.DoesNotExist:
        return jsonify({"error": "Extract not found"}), 404
    return jsonify(model_to_dict(extract))


if __name__ == "__main__":
    app.run()
