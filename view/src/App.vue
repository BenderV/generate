<script setup lang="ts">
import { RouterView } from "vue-router";
import Header from "./components/Header.vue";
import Notification from "./components/Notification.vue";
</script>

<template>
  <Header />
  <RouterView />
  <Notification />
</template>
