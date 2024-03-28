<template>
  <div id="app">
    <router-link to="/">Home</router-link> |
    <router-link to="/login">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link to="/rooms">Chat Rooms</router-link>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
