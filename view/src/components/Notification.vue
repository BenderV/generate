<template>
  <!-- Global notification live region, render this permanently at the end of the document -->
  <NotificationGroup group="foo">
    <div
      class="fixed inset-0 flex items-start justify-end p-6 px-4 py-6 pointer-events-none"
    >
      <div class="w-full max-w-sm">
        <Notification
          v-slot="{ notifications }"
          enter="transform ease-out duration-300 transition"
          enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
          enter-to="translate-y-0 opacity-100 sm:translate-x-0"
          leave="transition ease-in duration-500"
          leave-from="opacity-100"
          leave-to="opacity-0"
          move="transition duration-500"
          move-delay="delay-300"
        >
          <div
            class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md"
            v-for="notification in notifications"
            :key="notification.id"
          >
            <div
              aria-live="assertive"
              class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6"
            >
              <div
                class="flex w-full flex-col items-center space-y-4 sm:items-end"
              >
                <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
                <div
                  class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
                >
                  <div class="p-4">
                    <div class="flex items-start">
                      <div class="flex-shrink-0">
                        <CheckCircleIcon
                          class="h-6 w-6 text-green-400"
                          aria-hidden="true"
                        />
                      </div>
                      <div class="ml-3 w-0 flex-1 pt-0.5">
                        <p class="text-sm font-medium text-gray-900">
                          {{ notification.title }}
                        </p>
                        <p class="mt-1 text-sm text-gray-500">
                          {{ notification.message }}
                        </p>
                      </div>
                      <div class="ml-4 flex flex-shrink-0">
                        <button
                          type="button"
                          @click="show = false"
                          class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        >
                          <span class="sr-only">Close</span>
                          <XMarkIcon class="h-5 w-5" aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Notification>
      </div>
    </div>
  </NotificationGroup>
</template>

<script setup>
import { ref, watch } from "vue";
import { CheckCircleIcon } from "@heroicons/vue/24/outline";
import { XMarkIcon } from "@heroicons/vue/20/solid";
</script>
