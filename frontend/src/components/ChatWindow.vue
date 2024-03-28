<template>
  <div class="chat-area">
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
    <div class="room-members">
      <h3>Members</h3>
      <ul>
        <li v-for="member in members" :key="member.id">{{ member.username }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
import axios from 'axios';

export default {
  props: ['roomId'],
  data() {
    return {
      messages: [],
      newMessage: '',
      socket: null,
      members: [],
    };
  },
  async mounted() {
    this.socket = io('http://localhost:5000', {
      query: {token: localStorage.getItem('userToken')},
    });

    this.socket.on('receive_message', this.receiveMessage);
    this.socket.on('update_message_status', this.updateMessageStatus);

    this.socket.emit('join', {
      room: this.roomId,
      token: localStorage.getItem('userToken')
    });
    await this.fetchMessages();
    await this.fetchRoomMembers();
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/chat/rooms/${this.roomId}/messages`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('userToken')}`},
        });
        this.messages = response.data.messages;
      } catch (error) {
        console.error("Couldn't fetch messages:", error);
      }
    },
    sendMessage() {
      if (!this.newMessage.trim()) return;
      this.socket.emit('message', {room: this.roomId, message: this.newMessage});
      this.newMessage = '';
    },
    receiveMessage(message) {
      this.messages.push(message);
    },
    updateMessageStatus(data) {
      const message = this.messages.find(m => m.id === data.message_id);
      if (message) message.status = data.status;
    },
    async fetchRoomMembers() {
      try {
        const response = await axios.get(`http://localhost:5000/chat/rooms/${this.roomId}/members`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('userToken')}`},
        });
        this.members = response.data.members;
      } catch (error) {
        console.error("Couldn't fetch room members:", error);
      }
    },
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.emit('leave', {room: this.roomId});
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
.chat-area {
  display: flex;
  justify-content: center;
}

.chat-window {
  flex-grow: 2;
  display: flex;
  flex-direction: column;
  margin-right: 20px;
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

.room-members {
  flex-grow: 1;
  margin-left: 20px;
}

.status {
  font-size: 0.75rem;
  text-align: right;
}
</style>
