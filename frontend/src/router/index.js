// src/router/index.js
import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import LoginScreen from '@/components/LoginScreen.vue';
import ChatWindow from '@/components/ChatWindow.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginScreen,
    },
    {
      path: '/chat',
      name: 'Chat',
      component: ChatWindow,
    },
  ],
});
