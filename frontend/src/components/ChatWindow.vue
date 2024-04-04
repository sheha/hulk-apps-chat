<template>
  <div class="chat-window">
    <div class="message-list">
      <div v-for="message in [...messages].reverse()" :key="message.id" class="message">
        <span class="username">{{ message.username }}</span>
        <span class="text">{{ message.message }}</span>
        <span class="timestamp">{{ message.timestamp }}</span>
        <!-- Here you can add icons or labels for message status -->
        <span class="status">{{ message.status }}</span>
      </div>
    </div>
    <div class="message-input">
      <input v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage"/>
      <button @click="handleSendMessage">Send</button>
    </div>
  </div>
</template>

<script>


export default {
  props: {
    roomId: Number,
    messages: Array,
    sendMessage: Function
  },

  data() {
    return {
      newMessage: ''
    };
  },
  methods: {
    handleSendMessage() {
      if (!this.newMessage.trim()) return;
      this.sendMessage(this.newMessage);
      this.newMessage = '';
    },
  },
};
</script>

<style scoped>

.chat-window {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden; /* Prevents window from growing */
  background-color: #222;
  border: 2px solid var(--border-color);
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
}

.message-list {
  overflow-y: auto; /* Allows scrolling */
  flex-grow: 1; /* Takes up all available space */
}

.message {
  background: #000;
  color: var(--neon-color);
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;

}

.username {
  font-weight: bold;
}

.text {
  margin-left: 10px;
  flex-grow: 1;
}

.timestamp {
  font-size: 0.8em;
  margin-left: 10px;
}

.status {
  font-size: 0.8em;
  margin-left: 10px;
  /* Add icons or styles for different statuses */
}

.message-input {
  display: flex;
  justify-content: space-between;
  margin-top: 1em;
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
