<template>
  <div class="login">
    <h2>Login</h2>
    <input v-model="username" type="text" placeholder="Username"/>
    <input v-model="password" type="password" placeholder="Password"/>
    <button @click="login">Login</button>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('userToken', response.data.access_token);
        await this.$router.push('/chat');
      } catch (error) {
        console.log(error)
      }
    },
  },
};
</script>


<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 60px;
}

.login input, .login button {
  margin: 10px;
  padding: 10px;
  width: 200px;
}
</style>