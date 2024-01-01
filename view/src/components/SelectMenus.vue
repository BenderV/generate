<template>
  <Listbox as="div" v-model="selectedOption">
    <ListboxLabel class="sr-only"> Change published status </ListboxLabel>
    <div class="relative">
      <div class="inline-flex divide-x divide-indigo-900 rounded-md shadow-sm">
        <div
          class="inline-flex divide-x divide-indigo-900 rounded-md shadow-sm"
        >
          <div
            class="inline-flex items-center rounded-l-md border border-transparent bg-indigo-600 py-2 pl-3 pr-4 text-white shadow-sm"
          >
            <p class="ml-2.5 text-sm font-medium">
              {{ selectedOption.review }}
            </p>
          </div>
          <ListboxButton
            class="inline-flex items-center rounded-l-none rounded-r-md bg-indigo-600 p-2 text-sm font-medium text-white hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-50"
          >
            <span class="sr-only">Change published status</span>
            <ChevronDownIcon class="h-5 w-5 text-white" aria-hidden="true" />
          </ListboxButton>
        </div>
      </div>

      <transition
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute left-0 z-10 mt-2 w-72 origin-top-left divide-y divide-gray-200 overflow-hidden rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
        >
          <ListboxOption
            as="template"
            v-for="option in publishingOptions"
            :key="option.review"
            :value="option"
            v-slot="{ active, selectedOption }"
          >
            <li
              :class="[
                active ? 'text-white bg-indigo-500' : 'text-gray-900',
                'cursor-default select-none p-4 text-sm',
              ]"
            >
              <div class="flex flex-col">
                <div class="flex justify-between">
                  <p :class="selectedOption ? 'font-semibold' : 'font-normal'">
                    {{ option.review }}
                  </p>
                  <span
                    v-if="selectedOption"
                    :class="active ? 'text-white' : 'text-indigo-500'"
                  >
                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                  </span>
                </div>
              </div>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>

<script setup>
import { ref, watch } from "vue";
import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions,
} from "@headlessui/vue";
import { CheckIcon, ChevronDownIcon } from "@heroicons/vue/20/solid";

const publishingOptions = [
  {
    review: "Unreviewed",
  },
  {
    review: "Good quality",
  },
  {
    review: "Fake data",
  },
  {
    review: "Incomplete data",
  },
];

const props = defineProps({
  review: {
    type: String,
    default: null,
  },
});

// Take first if no props
const selectedOption = ref(
  props.review
    ? publishingOptions.find((option) => option.review === props.review)
    : publishingOptions[0]
);

const emits = defineEmits(["selected"]);
// Watch
// If props.review change (and only this), update selectedOption
watch(
  () => props.review,
  (newReview) => {
    selectedOption.value = props.review
      ? publishingOptions.find((option) => option.review === props.review)
      : publishingOptions[0];
  }
);
// If selectOption is different from props, emit event
watch(
  () => selectedOption.value,
  (newSelectedOption) => {
    if (newSelectedOption.review !== props.review) {
      emits("selected", newSelectedOption.review);
    }
  }
);
</script>
