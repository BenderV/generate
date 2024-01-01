<template>
  <form onsubmit="event.preventDefault();">
    <label class="block text-sm font-medium text-gray-700" for="title"
      >Title</label
    >
    <input
      type="text"
      id="title"
      v-model="extract.title"
      class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      placeholder="french cities (top 100)"
      required
    />
    <br />
    <h3 class="block text-sm font-medium text-gray-700">
      Specify Fields (optional)
    </h3>
    <div id="fields">
      <div class="item" :key="key" v-for="(field, key) in extract.fields">
        -
        <label class="mr-2 text-sm font-medium text-gray-700" for="item-1-name"
          >Name</label
        >
        <input
          type="text"
          id="item-1-name"
          name="fields[1][name]"
          v-model="field.name"
          class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          required
        />
        <label
          class="ml-4 mr-2 text-sm font-medium text-gray-700"
          for="item-1-description"
          >Description</label
        >
        <input
          type="text"
          id="item-1-description"
          name="fields[1][description]"
          v-model="field.description"
          class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
        <label
          for="item-1-type"
          class="ml-4 mr-2 text-sm font-medium text-gray-700"
          >Type</label
        >
        <select
          id="item-1-type"
          name="fields[1][type]"
          v-model="field.type"
          class="mt-1 rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        >
          <option value="string">string</option>
          <option value="integer">integer</option>
          <option value="float">float</option>
          <option value="boolean">boolean</option>
        </select>

        <!-- delete button (icon X) -->
        <!-- doesn't display if only one field -->
        <!-- grey color, red on hover -->
        <button
          type="button"
          class="ml-4 inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded-full text-gray-700 bg-gray-100 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="removeField(key)"
        >
          <svg
            class="h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
    <button
      type="button"
      class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 mt-1"
      id="add-field"
      @click="addField"
    >
      Add field
    </button>
    <br /><br />
    <input
      type="submit"
      class="w-full cursor-pointer inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      value="Generate data"
      @click="generateData"
      v-if="!loading"
    />
    <button
      v-if="loading"
      type="button"
      class="w-full cursor-pointer inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition ease-in-out duration-150 cursor-not-allowed"
      disabled=""
    >
      <svg
        class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      Processing...
    </button>
  </form>
  <div v-if="!loading && extract.output">
    <div class="relative mt-6">
      <div class="absolute inset-0 flex items-center" aria-hidden="true">
        <div class="w-full border-t border-gray-300" />
      </div>
      <div class="relative flex justify-center">
        <span class="bg-white px-3 text-lg font-medium text-gray-900"
          >Result</span
        >
      </div>
    </div>
    <div v-if="!loading && extract.output.length == 0">
      Sorry, we couldn't find any data matching your query.
    </div>
    <div v-if="!loading && extract.output?.length">
      <BaseAlert>
        <p>
          The current AI model used (Large Language Model) is known to be
          <b>unreliable</b>. Please check the results carefully.<br />
        </p>
      </BaseAlert>
      <BaseAlert
        v-if="extract.metadata && extract.metadata.estimated_size > 100"
        class="mt-2"
      >
        Estimated size: {{ extract.metadata.estimated_size }} rows, but
        <b>limited to 100</b> for now.
      </BaseAlert>

      <div class="float-left my-2">
        <SelectMenus @selected="onReviewSelected" :review="extract.review" />
      </div>

      <button
        type="submit"
        class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 float-right my-2"
        @click="exportData"
        v-if="extract.output"
      >
        Download
      </button>
      <button
        type="submit"
        class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 float-right my-2 mr-2"
        @click="copyToClipboard"
        v-if="extract.output"
      >
        <span v-if="!copied">Copy</span><span v-else>Copied!</span>
      </button>
    </div>

    <BaseTable
      v-if="!loading && extract.output"
      :data="extract.output"
    ></BaseTable>
  </div>
</template>

<script setup>
import BaseTable from "./BaseTable.vue";
import BaseAlert from "./BaseAlert.vue";
import SelectMenus from "./SelectMenus.vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { ref, reactive, watch } from "vue";
import router from "../router";
import { notify } from "notiwind";

const route = useRoute();

const copied = ref(false);

// Default field values
const defaultField = {
  name: "",
  description: "",
  type: "string",
};
const extract = ref({
  name: "",
  description: "",
  fields: [],
  output: null,
  metadata: null,
});

const onReviewSelected = async (value) => {
  await axios.post(`/api/extracts/${extract.value.id}/review`, {
    review: value,
  });

  notify(
    {
      group: "foo",
      title: "Successfully reviewed",
      message: "Thanks for your feedback!",
    },
    4000
  );
};

const loadExtract = (id) => {
  axios
    .get(`/api/extracts/${id}`)
    .then((response) => {
      extract.value = response.data;
    })
    .catch((error) => {
      console.log(error);
      // If error, redirect to home
      router.push("/");
    });
};

if (route.params.id) {
  loadExtract(route.params.id);
}

// Fill form with data from database if id is provided
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
      loadExtract(route.params.id);
    }
  }
);

// Add new item when clicking on Add item button
const addField = () => {
  extract.value.fields.push({ ...defaultField });
};

const removeField = (index) => {
  console.log(index);
  extract.value.fields.splice(index, 1);
};

const loading = ref(false);

// Generate data when clicking on Generate data button
const generateData = (event) => {
  // Avoid form submission
  console.log(extract.value.fields);

  // Check form validity
  // title must be filled
  // at least field name must be filled
  if (!extract.value.title) {
    return;
  }
  if (
    extract.value.fields.length > 0 &&
    !extract.value.fields.some((field) => field.name)
  ) {
    return;
  }
  loading.value = true;

  // Call /api/generate, return data
  axios
    .post("/api/generate", {
      title: extract.value.title,
      fields: extract.value.fields,
    })
    .then((response) => {
      router.push(`/${response.data.slug}`);
    })
    .catch((error) => {
      console.log(error);
    })
    .finally(() => {
      loading.value = false;
    });
};

function copyToClipboard(data) {
  // Convert the data to a CSV file
  const csv = convertToCSV(extract.value.output);

  // Copy the CSV file to clipboard
  navigator.clipboard.writeText(csv);

  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 1000);
}

function exportData(data) {
  // Convert the data to a CSV file
  const csv = convertToCSV(extract.value.output);

  // Prompt the user to download the CSV file
  // Use title as filename, slugify it
  const filename = extract.value.title
    .toLowerCase()
    .replace(/ /g, "-")
    .replace(/[^\w-]+/g, "");
  download(csv, filename + ".csv", "text/csv");
}

function convertToCSV(data) {
  // Convert the data to a CSV string
  // (Assuming the data is an array of objects)
  // Header
  const header = Object.keys(data[0]).join(",");
  // Content
  const csv = data
    .map((row) =>
      Object.values(row)
        // Escape commas
        .map((value) => value?.toString().replace(/,/g, "\\,"))
        .join(",")
    )
    .join("\n");

  // Join header and content
  return header + "\n" + csv;
}

function download(content, fileName, contentType) {
  // Create a download link element
  const a = document.createElement("a");
  a.download = fileName;
  a.href = URL.createObjectURL(new Blob([content], { type: contentType }));

  // Trigger the download
  a.click();
}
</script>
