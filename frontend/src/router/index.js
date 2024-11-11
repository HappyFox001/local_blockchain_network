import { createRouter, createWebHistory } from 'vue-router';
import About from '../views/About.vue';
import Dashboard from '../views/Dashboard.vue';
const routes = [
    {
        path: '/',
        name: 'about',
        component: About,
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
