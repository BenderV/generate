import { createApp } from "vue";
import { createPinia } from "pinia";
// @ts-ignore
import Notifications from "notiwind";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
app.use(Notifications);
app.use(router);

app.mount("#app");
