import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import LoginScreen from '@/components/LoginScreen.vue';
import ChatWindow from '@/components/ChatWindow.vue';
import RoomsList from '@/components/RoomsList.vue';
import RegisterScreen from "@/components/RegisterScreen.vue";

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/register', name: 'Register', component: RegisterScreen },
    { path: '/login', name: 'Login', component: LoginScreen },
    { path: '/chat', name: 'Chat', component: ChatWindow, props: true }, // Enable props to receive roomId
    { path: '/rooms', name: 'Rooms', component: RoomsList },
  ],
});
