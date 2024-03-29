<template>
  <div id="app">
    <router-link to="/">Home</router-link> |
    <router-link v-if="!isLoggedIn" to="/login">Login</router-link> |
    <router-link v-if="!isLoggedIn" to="/register">Register</router-link> |
    <router-link v-if="isLoggedIn" to="/rooms">Chat Rooms</router-link> |
    <button v-if="isLoggedIn" @click="logout">Logout</button>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    // Computed property to check if user is logged in
    isLoggedIn() {
      return !!localStorage.getItem('userToken');
    }
  },
  methods: {
    // Logout method to clear the token and redirect
    logout() {
      localStorage.removeItem('userToken'); // Clear the token
      this.$router.push('/login'); // Redirect to login page
    }
  }
}
</script>

<style>
:root {
  --background-color: #333;
  --neon-color: #0f0;
  --text-color: #fff;
  --border-color: #555;
}

body {
  margin: 0;
  font-family: 'Poppins', sans-serif; /* Apply Poppins as the default font */
  background-color: var(--background-color);
  color: var(--text-color);
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'Poppins', sans-serif;
}
body, .chat-area, .rooms-list, .login {
  background-color: #121212; /* Dark background */
  color: #cfcfcf; /* Light text */
}

/* Input Fields Styling */
/* Input Fields Styling */
input {
  background-color: #333; /* Darker background for inputs */
  border: 1px solid #0f0; /* Neon green border */
  color: #cfcfcf; /* Light text */
  padding: 10px;
  margin-bottom: 10px;
  box-shadow: 0 0 5px #0f0; /* Neon glow effect */
  border-radius: 8px; /* Rounded corners */
}

/* Button Styling */
button {
  background-color: #333; /* Dark background for buttons */
  border: none;
  padding: 10px 20px;
  color: #cfcfcf; /* Light text */
  cursor: pointer;
  box-shadow: 0 0 5px #0f0, /* Inner neon glow */
              0 0 15px #0f0; /* Outer neon glow */
  transition: all 0.3s ease;
  border-radius: 8px; /* Rounded corners */
}

button:hover {
  background-color: #0f0; /* Neon color on hover */
  color: #121212; /* Dark text on hover */
}

/* Applying Poppins font globally */
body {
  font-family: 'Poppins', sans-serif;
}

a {
  color: var(--neon-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

#app {
  text-align: center;
}

.router-link {
  margin: 10px;
  font-size: 18px;
  font-weight: bold;
}

.router-link-active {
  color: var(--neon-color);
}
</style>