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
}

.rooms-list {
  width: 20%;
  overflow-y: auto;
  height: 100vh;
  padding: 1rem;
}

.chat-container {
  flex-grow: 1;
  padding: 1rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  cursor: pointer;
  margin-bottom: 0.5rem;
}

form {
  margin-bottom: 1rem;
}
</style>
