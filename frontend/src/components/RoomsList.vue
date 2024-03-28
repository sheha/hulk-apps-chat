<template>
  <div class="rooms-list">
    <h2>Chat Rooms</h2>
    <ul>
      <li v-for="room in rooms" :key="room.id" @click="joinRoom(room.id)">
        {{ room.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rooms: [],
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
    joinRoom(roomId) {
      // Navigate to the ChatWindow component for the selected room
      this.$router.push({name: 'Chat', params: {roomId}});
    },
  },
};
</script>

<style scoped>
.rooms-list {
  padding: 1rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  cursor: pointer;
  margin: 0.5rem 0;
}
</style>
