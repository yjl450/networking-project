<template>
  <div id="chat">
    <md-app md-waterfall md-mode="fixed" id="messages">
      <md-app-toolbar class="md-primary">
        <md-button class="md-icon-button" @click="togglelist" v-if="mobile">
          <md-icon>people</md-icon>
        </md-button>
        <span class="md-title" id="title" @click="full_title = true"
          >{{ chat_member }}
          <md-dialog-alert
            :md-active.sync="full_title"
            :md-content="chat_member"
          />
        </span>

        <div class="md-toolbar-section-end">
          <md-menu md-direction="bottom-start">
            <md-button class="md-icon-button" md-menu-trigger
              ><md-icon>more_vert</md-icon></md-button
            >

            <md-menu-content>
              <md-menu-item v-if="current_chat" @click="leave = true"
                >Leave Conversation</md-menu-item
              >
              <md-menu-item @click="logout = true">Log Out</md-menu-item>
            </md-menu-content>
          </md-menu>
          <md-dialog-confirm
            :md-active.sync="logout"
            md-title="Leave all your conversation and log out?"
            md-content="You will lose all your chat history.<br> You will need to create a new user when you log in next time."
            md-confirm-text="Confirm"
            md-cancel-text="Cancel"
            @md-cancel="logout = false"
            @md-confirm="logout_confirm"
          />
          <md-dialog-confirm
            :md-active.sync="leave"
            md-title="Leave this conversation?"
            md-content="You will lose all the history of this chat."
            md-confirm-text="Confirm"
            md-cancel-text="Cancel"
            @md-cancel="leave = false"
            @md-confirm="leave_confirm"
          />
        </div>
      </md-app-toolbar>
      <md-app-content id="messages" class="md-scrollbar">
        <Bubble :key="m.index" v-for="m in current_messages" :message="m" />
        <md-empty-state
          md-icon="speaker_notes_off"
          md-label="Start a conversation!"
          v-if="!current_chat"
        >
          <span v-if="!mobile"
            >Select an online user on the left to start a conversation.</span
          >
          <span v-if="mobile"
            >Select an online user to start a conversation by click the button
            the top left or click</span
          >

          <md-button
            class="md-primary md-raised"
            @click="togglelist"
            v-if="mobile"
            >Chat with other online user</md-button
          >
        </md-empty-state>
      </md-app-content>
    </md-app>
    <div id="input-area" v-show="current_chat">
      <div id="pseudo-textarea">
        <twemoji-picker
          :emojiData="emojiData"
          :emojiGroups="emojiGroups"
          @emojiUnicodeAdded="handleEmojiPicked"
        >
          <template v-slot:twemoji-picker-button>
            <md-button class="md-icon-button chat_button md-mini">
              <md-icon id="emoji">insert_emoticon</md-icon>
            </md-button>
          </template>
        </twemoji-picker>

        <div
          id="textbox"
          contenteditable="plaintext-only"
          display:inline-block
        ></div>
      </div>
      <md-button
        class="md-icon-button chat_button md-mini"
        @click="send_message"
      >
        <md-icon>send</md-icon>
      </md-button>
    </div>
  </div>
</template>

<script>
import { TwemojiPicker } from "@kevinfaguiar/vue-twemoji-picker";
import emojiData from "@/assets/emoji-all-groups.json";
import emojiGroups from "@/assets/emoji-groups.json";
import Bubble from "@/components/Bubble.vue";

export default {
  name: "Chat",
  components: {
    TwemojiPicker,
    Bubble,
  },
  data() {
    return {
      // toggle for confirmation
      logout: false,
      leave: false,
      full_title: false,
      listshow: false,
      emojiData: emojiData,
      emojiGroups: emojiGroups,
      message: "",
    };
  },
  props: {
    username: String,
    id: String,

    mobile: Boolean,
    showlist: Boolean,
    current_chat: Object,

    current_messages: Array,
  },
  mounted() {
    document.getElementById("textbox").addEventListener("keydown", (evt) => {
      if (evt.keyCode === 13) {
        evt.preventDefault();
        this.send_message();
      }
    });
  },
  computed: {
    chat_member() {
      if (this.current_chat === null) {
        return "Welcome, " + this.username;
      }
      var names = { ...this.current_chat.member };
      delete names[this.id];
      names = Object.values(names);
      if (names.length > 1) {
        return (
          "(" +
          (names.length + 1) +
          ") " +
          names.join(", ") +
          ", " +
          this.username
        );
      }
      return names[0];
    },
  },
  beforeDestroy() {
    this.close_app();
  },
  methods: {
    handleEmojiPicked(e) {
      document.getElementById("textbox").innerHTML += e;
      // this.new_message = document.getElementById("textbox").textContent;
    },
    togglelist() {
      this.listshow = !this.showlist;
      this.$emit("togglelist", this.listshow);
    },
    // Network related
    send_message() {
      this.$root.s.emit("message", {
        sender: this.id,
        receiver: this.current_chat.id,
        message: document.getElementById("textbox").textContent,
      });
      this.$emit("new_message", {
        sender: this.id,
        receiver: this.current_chat.id,
        message: document.getElementById("textbox").textContent,
      });
      document.getElementById("textbox").innerHTML = "";
    },
    logout_confirm() {
      // TODO: send logout info to server
      this.close_app();
      this.logout = false;
    },
    leave_confirm() {
      if (this.current_chat.id.length !== 20) {
        // TODO: send info to server
      }
      this.$emit("quit_chat", null);
      this.leave = false;
    },
    close_app() {},
  },
};
</script>

<style scoped>
#chat {
  height: 100%;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

#messages {
  flex-grow: 1;
  overflow: auto;
}

#title {
  overflow: hidden;
}

#input-area {
  /* border-top: 1px solid #a8a8a8; */
  background-color: white;
  display: flex;
  align-items: center;
  width: 100%;
  padding-bottom: 5px;
  padding-top: 5px;
}

#pseudo-textarea {
  width: calc(100% - 60px);
  background-color: rgb(226, 223, 223);
  display: flex;
  align-items: center;
  border-radius: 6ex;
  margin-left: 10px;
}

#textbox {
  width: calc(100% - 100px);
  padding-left: 10px;
  min-height: 2ex;
  max-height: 11ex;
  margin-top: 5px;
  margin-bottom: 5px;
  resize: none;
  font-family: inherit;
  border: 0;
  overflow: auto;
  font-family: Roboto;
  font-size: 16px;
}

#textbox:focus {
  outline: 0;
}

.chat_button {
  margin-left: 5px;
  margin-right: 5px;
}

#emoji {
  color: rgb(236, 63, 184);
}
</style>