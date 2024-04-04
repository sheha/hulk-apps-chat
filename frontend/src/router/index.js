import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import LoginScreen from '@/components/LoginScreen.vue';
import ChatScreen from "@/components/ChatScreen.vue";
import RegisterScreen from "@/components/RegisterScreen.vue";

Vue.use(Router);

// Function to check if the user is logged in
function isLoggedIn() {
  return !!localStorage.getItem('userToken');
}

const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/register', name: 'Register', component: RegisterScreen, meta: { requiresGuest: true } },
    { path: '/login', name: 'Login', component: LoginScreen, meta: { requiresGuest: true } },
    { path: '/chat', name: 'Chat', component: ChatScreen, props: true, meta: { requiresAuth: true } },
    // { path: '/rooms', name: 'Rooms', component: RoomsList, meta: { requiresAuth: true } },
  ],
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  const authRequired = to.matched.some(record => record.meta.requiresAuth);
  const guestOnly = to.matched.some(record => record.meta.requiresGuest);

  if (authRequired && !isLoggedIn()) {
    next('/login');
  } else if (guestOnly && isLoggedIn()) {
    next('/rooms');
  } else {
    next();
  }
});

export default router;
