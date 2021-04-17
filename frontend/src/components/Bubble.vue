<template>
  <div class="message-block" v-if="!message.me">
    <div class="identity">{{ message.sender }}</div>
    <div class="content">{{ message.message }}</div>
  </div>
  <div class="message-block" id="block-me" v-else>
    <div class="content" id="content-me">{{ message.message }}</div>
    <div class="identity" id="id-me">{{ message.sender }}</div>
  </div>
</template>

<script>
export default {
  name: "Bubble",
  props: {
    message: {
      sender: String,
      message: String,
      me: Boolean,
      index: Number,
    },
  },
};
</script>

<style scoped>
.message-block {
  display: flex;
  font-family: Roboto;
  font-size: 16px;
  margin-bottom: 8px;
  width: 100%;
}

.identity {
  overflow-wrap: break-word;
  padding-left: 0;
  font-weight: bold;
  border-radius: 25px;
  padding-top: 0;
}

.content {
  background-color: #fcc8bd;
  margin-left: 5px;
  padding: 6px;
  font-size: 15px;
  border-radius: 5px 20px 20px 20px;
  max-width: 65%;
  text-align: center;
  overflow-x: hidden;
  word-wrap: break-word;
  word-break: break-all;
}

#block-me {
  justify-content: flex-end;
}

#id-me {
  margin-left: 5px;
}

#content-me {
  color: white;
  background-color: #1e8bdf;
  border-radius: 20px 5px 20px 20px;
}
</style>