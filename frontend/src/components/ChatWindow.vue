<template>
  <div class="chat-window">
    <div class="messages">
      <div v-for="message in messages" :key="message.id" class="message">
        <div><strong>{{ message.username }}</strong>: {{ message.message }}</div>
        <div class="status">{{ message.status }}</div>
      </div>
    </div>
    <div class="message-input">
      <input v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage">
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
import axios from 'axios';

export default {
  props: ['roomId'], // Assume roomId is passed to this component
  data() {
    return {
      messages: [],
      newMessage: '',
      socket: null,
    };
  },
  async mounted() {
    this.socket = io('http://localhost:5000', {
      query: {
        token: localStorage.getItem('userToken'), // Assuming you're storing the token in localStorage
      },
    });

    this.socket.on('receive_message', this.receiveMessage);
    this.socket.on('update_message_status', this.updateMessageStatus);

    // Join the room
    this.socket.emit('join', {room: this.roomId});

    // Fetch existing messages for the room
    await this.fetchMessages();
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/chat/rooms/${this.roomId}/messages`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('userToken')}`,
          },
        });
        this.messages = response.data.messages;
      } catch (error) {
        console.error("Couldn't fetch messages:", error);
      }
    },
    sendMessage() {
      if (!this.newMessage.trim()) return;

      // Emit message to server
      this.socket.emit('message', {
        room: this.roomId,
        message: this.newMessage,
        // Add recipient_id if it's a private message
      });

      this.newMessage = ''; // Clear input after sending
    },
    receiveMessage(message) {
      this.messages.push(message);
    },
    updateMessageStatus(data) {
      // Find the message by ID and update its status
      const message = this.messages.find(m => m.id === data.message_id);
      if (message) {
        message.status = data.status;
      }
    },
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  max-width: 500px;
  margin: auto;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
}

.message-input {
  display: flex;
  margin-top: 1rem;
}

input, button {
  padding: 0.5rem;
  margin: 0.25rem;
}

.status {
  font-size: 0.75rem;
  text-align: right;
}
</style>
