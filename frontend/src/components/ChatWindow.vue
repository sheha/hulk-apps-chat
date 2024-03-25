<template>
  <div class="chat">
    <div class="messages">
      <!-- Iterate over messages and display them here -->
    </div>
    <input v-model="inputMessage" type="text" placeholder="Type a message..."/>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      messages: [],
      inputMessage: '',
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000');
    this.socket.on('receive_message', (message) => {
      this.messages.push(message);
    });
  },
  methods: {
    sendMessage() {
      this.socket.emit('message', {text: this.inputMessage, room: 'YourRoom'});
      this.inputMessage = '';
    },
  },
};
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.chat .messages {
  width: 90%;
  max-width: 600px;
  min-height: 300px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  overflow-y: auto;
}

.chat input, .chat button {
  margin: 5px;
  padding: 10px;
  width: 200px;
}
</style>