import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import TestHome from "@/components/test-service/TestHome.vue";
import TopComponent from "@/components/TopComponent.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/top",
    name: "TopComponent",
    component: TopComponent,
  },
  {
    path: "/TestHome",
    name: "TestHome",
    component: TestHome,
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;
