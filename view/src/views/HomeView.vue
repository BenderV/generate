<script setup lang="ts">
import ExtractSearch from "../components/ExtractSearch.vue";
import Prompt from "../components/Prompt.vue";
import BaseAlert from "../components/BaseAlert.vue";
import Modal from "../components/Modal.vue";

import { ref } from "vue";
const showEmailCapture = ref(false);
</script>

<template>
  <main class="container mx-auto px-4 max-w-5xl">
    <h1 class="text-4xl my-4 text-center">Generate</h1>
    <h2 class="text-3xl my-4 text-center">
      Create data on-the-fly using AI knowledge.
    </h2>
    <div class="cta text-center" @click="showEmailCapture = true">
      <label class="label">new</label>
      Get the gsheet integration →
    </div>
    <Modal v-model="showEmailCapture" />
    <br />
    <Prompt />
    <br />
    <hr />
    <br />
    <h2 class="text-2xl my-4">Previously generated</h2>
    <ExtractSearch />
  </main>
</template>

<style scoped>
h1 {
  line-height: 1;
  font-weight: 500;
  font-size: 4rem;
  letter-spacing: -0.1875rem;
  padding-top: 2rem;
}

.cta {
  cursor: pointer;
}
.label {
  background-color: #3e8ef1;
  color: white;
  padding: 0.1rem;
  font-size: 0.8rem;
  border-radius: 0.2rem;
  cursor: inherit;
}
</style>
