<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="relative z-10" @close="open = false">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-sm sm:p-6"
            >
              <div>
                <div
                  class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-100"
                >
                  <RocketLaunchIcon
                    class="h-6 w-6 text-blue-600"
                    aria-hidden="true"
                  />
                </div>
                <div class="mt-3 text-center sm:mt-5">
                  <DialogTitle
                    as="h3"
                    class="text-lg font-medium leading-6 text-gray-900"
                    >Join the waiting list</DialogTitle
                  >
                  <p class="text-sm text-gray-500">
                    <br />
                    Keep in touch with us! <br />
                    Get first access to our next features.
                  </p>
                  <div class="mt-2">
                    <form class="mt-5 sm:flex sm:items-center">
                      <div class="w-full sm:max-w-xs">
                        <label for="email" class="sr-only">Email</label>
                        <input
                          type="email"
                          name="email"
                          v-model="email"
                          id="email"
                          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                          placeholder="you@example.com"
                        />
                      </div>
                      <button
                        type="submit"
                        @click.prevent="saveEmail()"
                        class="mt-3 inline-flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                      >
                        Save
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { computed, ref } from "vue";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from "@headlessui/vue";
import { RocketLaunchIcon } from "@heroicons/vue/24/outline";
import { defineProps, defineEmits } from "@vue/runtime-core";
import axios from "axios";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

const email = ref("");
const emit = defineEmits(["update:modelValue"]);
const open = computed({
  get: () => props.modelValue,
  set: (value) => {
    props.modelValue = value;
    emit("update:modelValue", value);
  },
});

// Call api to save email
const saveEmail = async () => {
  const response = await axios.post("/api/subscribe", { email: email.value });
  console.log(response);
  if (response.status === 200) {
    open.value = false;
  }
};
</script>
