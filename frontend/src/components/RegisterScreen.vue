<template>
  <div class="login">
    <h2>Register</h2>
    <input v-model="username" type="text" placeholder="Username"/>
    <input v-model="password" type="password" placeholder="Password"/>
    <button @click="register">Register</button>
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
    async register() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          password: this.password,
        });
        console.log(response)
        await this.$router.push('/login');
      } catch (error) {
        console.error(error)
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