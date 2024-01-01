<template>
  <div>
    <label for="search" class="block text-sm font-medium text-gray-700"
      >Quick search</label
    >
    <div class="relative mt-1 flex items-center">
      <input
        type="text"
        name="search"
        id="search"
        class="block w-full rounded-md border-gray-300 pr-12 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
      <div class="absolute inset-y-0 right-0 flex py-1.5 pr-1.5">
        <kbd
          class="inline-flex items-center rounded border border-gray-200 px-2 font-sans text-sm font-medium text-gray-400"
          >⌘K</kbd
        >
      </div>
    </div>
  </div>
</template>
