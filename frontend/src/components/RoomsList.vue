<template>
  <div class="app-container">
    <div class="rooms-list">
      <h2>Chat Rooms</h2>
      <form @submit.prevent="createRoom">
        <input v-model="newRoomName" type="text" placeholder="Room Name" required />
        <input v-model="newRoomDescription" type="text" placeholder="Description (Optional)" />
        <button type="submit">Create Room</button>
      </form>
      <ul>
        <li v-for="room in rooms" :key="room.id" @click="selectRoom(room.id)">
          {{ room.name }} - Created by: {{ room.creator }}
        </li>
      </ul>
    </div>
    <div class="chat-container">
      <!-- ChatWindow component will be dynamically rendered here -->
      <ChatWindow v-if="selectedRoomId" :roomId="selectedRoomId" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ChatWindow from './ChatWindow.vue';

export default {
  components: {
    ChatWindow,
  },
  data() {
    return {
      rooms: [],
      newRoomName: '',
      newRoomDescription: '',
      selectedRoomId: null,
    };
  },
  async mounted() {
    await this.fetchRooms();
  },
  methods: {
    async fetchRooms() {
      try {
        const response = await axios.get('http://localhost:5000/chat/rooms', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('userToken')}`,
          },
        });
        this.rooms = response.data.rooms;
      } catch (error) {
        console.error("Couldn't fetch rooms:", error);
      }
    },
    async createRoom() {
      try {
        await axios.post(
            'http://localhost:5000/chat/rooms',
            {
              name: this.newRoomName,
              description: this.newRoomDescription,
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('userToken')}`,
              },
            }
        );
        this.newRoomName = '';
        this.newRoomDescription = '';
        await this.fetchRooms(); // Refresh the list after creating a new room
      } catch (error) {
        console.error("Couldn't create room:", error);
      }
    },
    selectRoom(roomId) {
      // Set the selectedRoomId to render ChatWindow for the selected room
      this.selectedRoomId = roomId;
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  background-color: var(--background-color);
  color: var(--text-color);
}

.rooms-list, .chat-container {
  padding: 20px;
  border: 2px solid var(--border-color);
  margin: 10px;
  border-radius: 8px;
  background-color: #222;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  cursor: pointer;
  color: var(--neon-color);
  margin-bottom: 10px;
}

li:hover {
  color: var(--text-color);
}

form input, form button {
  padding: 10px;
  margin: 5px 0;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: #222;
  color: var(--text-color);
}

form button {
  cursor: pointer;
  background-color: var(--neon-color);
  color: #000;
}

form button:hover {
  background-color: var(--text-color);
}
</style>
