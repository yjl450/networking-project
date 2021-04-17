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
        <md-empty-state
          md-icon="speaker_notes_off"
          md-label="You don't have any chat."
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
          @input="onInput"
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

export default {
  name: "Chat",
  components: {
    TwemojiPicker,
  },
  data() {
    return {
      // toggle for confirmation
      logout: false,
      leave: false,
      full_title: false,
      listshow: false,
      new_message: "",
      emojiData: emojiData,
      emojiGroups: emojiGroups,
    };
  },
  props: {
    mobile: Boolean,
    showlist: Boolean,
    current_chat: {},
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
        return "Welcome";
      }
      var names = Object.values(this.current_chat.member);
      if (names.length > 1) {
        return "(" + names.length + ") " + names.join(", ");
      }
      return names.join(", ");
    },
  },
  methods: {
    handleEmojiPicked(e) {
      document.getElementById("textbox").innerHTML += e;
      this.new_message = document.getElementById("textbox").textContent;
    },
    onInput(text) {
      this.new_message = text.target.textContent;
    },
    send_message() {
      console.log(this.new_message);
      document.getElementById("textbox").innerHTML = "";
      this.new_message = "";
    },
    logout_confirm() {
      this.logout = false;
    },
    leave_confirm() {
      this.leave = false;
    },
    togglelist() {
      this.listshow = !this.showlist;
      this.$emit("togglelist", this.listshow);
    },
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