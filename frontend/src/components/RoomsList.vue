<template>
  <div class="rooms-list">
    <h2>Chat Rooms</h2>
    <form @submit.prevent="emitCreateRoom">
      <input v-model="newRoomName" type="text" placeholder="Room Name" required/>
      <input v-model="newRoomDescription" type="text" placeholder="Description (Optional)"/>
      <button type="submit">Create Room</button>
    </form>
    <ul>
      <li v-for="room in rooms" :key="room.id" @click="emitSelectRoom(room.id)">
        {{ room.name }} - Created by: {{ room.creator }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    rooms: Array
  },
  data() {
    return {
      newRoomName: '',
      newRoomDescription: '',
    };
  },
  methods: {
    emitCreateRoom() {
      if (!this.newRoomName.trim()) return;
      // Emitan event with the new room details
      this.$emit('createRoom', {
        name: this.newRoomName,
        description: this.newRoomDescription
      });

      this.newRoomName = '';
      this.newRoomDescription = '';
    },
    emitSelectRoom(roomId) {

      this.$emit('selectRoom', roomId);
    },
  }
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
