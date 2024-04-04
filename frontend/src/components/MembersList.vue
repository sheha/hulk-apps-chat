<template>
  <div class="members-list">
    <h3>Members</h3>
    <ul>
      <li v-for="member in members" :key="member.id" class="member">
        <span class="online-indicator" :class="{ 'is-online': member.isOnline }"></span>
        {{ member.username }}
        <button v-if="isRoomCreator && member.id !== userId" @click="removeMember(member.id)" class="remove-member">
          X
        </button>
      </li>
    </ul>
  </div>
</template>


<script>
export default {
  props: {
    roomId: Number,
    members: Array,
    isRoomCreator: Boolean,
    userId: Number,
    removeMember: Function // Pass this method from ChatScreen
  },
  removeMember(memberId) {
    this.$emit('removeMember', memberId);
  }
};
</script>

<style scoped>
.room-members {
  margin-left: auto;
  /* Adjust styles as needed */
}

.member {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.online-indicator {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 5px;
  background-color: grey; /* Default offline color */
}

.online-indicator.online {
  background-color: green; /* Online color */
}

button {
  margin-left: 10px;
  /* Style your button as needed */
}

.remove-member {
  background: none;
  border: none;
  cursor: pointer;
  color: red; /* or a subtle color */
  margin-left: 10px;
  /* additional styles for the remove button */
}

.remove-member:hover {
  color: darkred; /* darker shade on hover */
}
</style>