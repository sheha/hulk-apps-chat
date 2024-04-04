<template>
  <div class="chat-screen">
    <RoomsList
        :rooms="rooms"
        @createRoom="createRoom"
        @selectRoom="selectRoom"/>
    <ChatWindow
        v-if="selectedRoomId"
        :roomId="selectedRoomId"
        :messages="messages"
        @sendMessage="sendMessage"/>
    <MembersList
        v-if="selectedRoomId"
        :roomId="selectedRoomId"
        :members="members"
        :isRoomCreator="isRoomCreator"
        :userId="currentUserId"
        @removeMember="removeMember"/>
  </div>
</template>

<script>
import RoomsList from './RoomsList.vue';
import ChatWindow from './ChatWindow.vue';
import MembersList from './MembersList.vue';
import axios from "axios";
import io from 'socket.io-client';

export default {
  components: {
    RoomsList,
    ChatWindow,
    MembersList
  },
  data() {
    return {
      rooms: [],
      members: [],
      messages: [],
      socket: null,
      selectedRoomId: null,
      isRoomCreator: false,
      currentUserId: null, // you would set this based on the logged-in user's id
    };
  },
  async created() {
    await this.fetchRooms();
    this.initializeSocket();
    // Assuming you have a method to get the current user ID,
    // you would set `currentUserId` here.
    this.currentUserId = this.getCurrentUserId();
  },
  methods: {

    getCurrentUserId() {
      // Logic to get current user ID
    },

    initializeSocket() {
      this.socket = io('http://localhost:5000', {
        query: {token: localStorage.getItem('userToken')},
      });

      this.socket.on('connect', () => {
        if (this.selectedRoomId) {
          this.joinRoom(this.selectedRoomId);
        }
      });

      this.socket.on('receive_message', this.receiveMessage);
      this.socket.on('update_message_status', this.updateMessageStatus);

    },
    joinRoom(selectedRoomId) {
      this.socket.emit('join', {
        room: selectedRoomId,
        token: localStorage.getItem('userToken'),
      });
      this.fetchRoomMembers(selectedRoomId);
      this.fetchMessages(selectedRoomId);
    },
    async fetchMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/chat/rooms/${this.selectedRoomId}/messages`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('userToken')}`},
        });
        this.messages = response.data.messages;
      } catch (error) {
        console.error("Couldn't fetch messages:", error);
      }
    },
    // sendMessage() {
    //   if (!this.newMessage.trim()) return;
    //   this.socket.emit('message', {room: this.selectedRoomId, message: this.newMessage});
    //   this.newMessage = '';
    // },
    sendMessage(message) {
      if (!message.trim()) return;
      this.socket.emit('message', {
        room: this.selectedRoomId,
        message: message
      });
    },
    receiveMessage(message) {
      this.messages.push(message);
    },
    updateMessageStatus(data) {
      const message = this.messages.find(m => m.id === data.message_id);
      if (message) message.status = data.status;
    },


    async fetchRoomMembers(selectedRoomId) {
      try {
        const response = await axios.get(`http://localhost:5000/chat/rooms/${selectedRoomId}/members`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('userToken')}`},
        });
        this.members = response.data.members;
        this.isRoomCreator = response.data.members.some(member =>
            member.id === this.currentUserId && member.isCreator);
      } catch (error) {
        console.error("Couldn't fetch room members:", error);
      }
    },
    async removeMember(memberId) {
      try {
        await axios.post(
            `http://localhost:5000/chat/rooms/${this.selectedRoomId}/remove_member`,
            {user_id: memberId},
            {headers: {Authorization: `Bearer ${localStorage.getItem('userToken')}`}}
        );
        // Refresh the members list after removing a member
        await this.fetchRoomMembers(this.selectedRoomId);
      } catch (error) {
        console.error("Couldn't remove member:", error);
      }
    },
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


    async createRoom(roomDetails) {
      try {
        await axios.post(
            'http://localhost:5000/chat/rooms',
            roomDetails,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('userToken')}`
              }
            }
        );
        // After creating the room, fetch the rooms list again
        await this.fetchRooms();
      } catch (error) {
        console.error("Couldn't create room:", error);
      }
    },
    handleRoomChange() {
      if (this.socket) {
        // Leave the old room if roomId changes
        this.socket.emit('leave', {room: this.oldRoomId});
        this.joinRoom(); // Join the new room
      }
    },


    async selectRoom(selectedRoomId) {
      this.selectedRoomId = selectedRoomId;
      await this.fetchRoomMembers(selectedRoomId);
      await this.fetchMessages(selectedRoomId);
    },

    watch: {
      selectedRoomId(newVal, oldVal) {
        if (newVal !== oldVal && newVal != null) {
          this.joinRoom(newVal);
          if (oldVal != null) {
            this.socket.emit('leave', {room: oldVal});
          }
        }
      },
    },
    beforeDestroy() {
      if (this.socket) {
        this.socket.emit('leave', {room: this.selectedRoomId});
        this.socket.disconnect();
      }
    },

  }
};
</script>

<style scoped>
.chat-screen {
  display: flex;
  justify-content: space-between;
  background-color: var(--background-color);
  color: var(--text-color);
  flex-direction: row;
  align-items: flex-start;

  .rooms-list {
    flex: 1; /* 1: Take up 1 fraction of the space available */
    max-width: 20%; /* Maximum width of the rooms list */

  }

  .chat-window {
    flex: 3; /* 3: Take up 3 fractions of the space available */
  }

  .members-list {
    flex: 1; /* 1: Take up 1 fraction of the space available */
    max-width: 15%; /* Maximum width of the members list */
  }

  @media (max-width: 768px) {
    .chat-screen {
      flex-direction: column;
    }

    /* Responsive design for smaller screens */
    .rooms-list,
    .members-list {
      max-width: 100%;
      flex: none; /* Stack them on top of each other instead */
    }

    .chat-window {
      flex: none; /* Allow chat window to take full width */
    }


  }

}

</style>
