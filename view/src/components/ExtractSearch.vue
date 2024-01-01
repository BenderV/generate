<script setup>
import Search from "./Search.vue";
import Prompt from "./Prompt.vue";
import { ref } from "vue";
import axios from "axios";
import router from "../router";

// Fetch extract from /api/extracts
const extracts = ref([]);
const loading = ref(false);
const error = ref();

const fetchExtracts = () => {
  loading.value = true;
  axios
    .get("/api/extracts")
    .then((response) => {
      console.log(response);
      extracts.value = response.data;
    })
    .catch((error) => {
      console.log(error);
      error.value = error;
    })
    .finally(() => {
      loading.value = false;
    });
};

fetchExtracts();

const selectExtract = (extract) => {
  router.push(`/${extract.slug ?? extract.id}`);
};

</script>

<template>
  <div role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
    <div
      v-for="extract in extracts"
      :key="extract.id"
      class="cursor-pointer col-span-1 divide-y divide-gray-200 rounded-lg bg-white shadow"
      @click="selectExtract(extract)"
      
    >
      <div class="flex w-full items-center justify-between space-x-6 p-6">
        <div class="flex-1 truncate">
          <div class="flex items-center space-x-3">
            <h3 class="truncate text-sm font-medium text-gray-900">
              {{ extract.title }}
            </h3>
          </div>
          <p class="mt-1 truncate text-sm text-gray-500">
            <!-- Display number of fields -->
            <span class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800">
              {{ extract.size }} rows
            </span>

            <br />
            <!-- Loop on sample key -->
            <div class="py-1">
              <span v-for="(field, key) in extract.fields" :key="field">
                <!-- not the first row -->
                <span v-if="key !== 0"> • </span>
                {{ field.name }}
              </span>
            </div>

            <!-- first row:
            <ul>
              <li v-for="(field, key) in extract.sample" :key="field">
                • <b>{{ key }}</b>: {{ field }}
              </li>
            </ul> -->
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
