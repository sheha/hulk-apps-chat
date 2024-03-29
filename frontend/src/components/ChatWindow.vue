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
  watch: {
    roomId(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.handleRoomChange();
      }
    },
  },
  mounted() {
    this.initializeSocket();
  },

  methods: {
    initializeSocket() {
      this.socket = io('http://localhost:5000', {
        query: {token: localStorage.getItem('userToken')},
      });

      this.socket.on('connect', () => {
        this.joinRoom();
      });

      this.socket.on('disconnect', (reason) => {
        console.log(`Disconnected: ${reason}`);
      });

      this.socket.on('receive_message', this.receiveMessage);
      this.socket.on('update_message_status', this.updateMessageStatus);
    },
    joinRoom() {
      if (this.roomId) {
        this.socket.emit('join', {
          room: this.roomId,
          token: localStorage.getItem('userToken'),
        });
        this.fetchRoomMembers();
        this.fetchMessages();
      }
    },
    handleRoomChange() {
      if (this.socket) {
        // Leave the old room if roomId changes
        this.socket.emit('leave', {room: this.oldRoomId});
        this.joinRoom(); // Join the new room
      }
    },
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
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: 16px;
}

.chat-window, .room-members {
  background-color: #222;
  border: 2px solid var(--border-color);
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
}

.messages {
  max-height: 300px;
  overflow-y: auto;
}

.message {
  background: #000;
  color: var(--neon-color);
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.message-input {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

input, button {
  padding: 10px;
  border: 1px solid var(--border-color);
  background-color: #222;
  color: var(--text-color);
  border-radius: 4px;
}

button {
  cursor: pointer;
  background-color: var(--neon-color);
  color: #000;
}

button:hover {
  background-color: var(--text-color);
}
</style>
