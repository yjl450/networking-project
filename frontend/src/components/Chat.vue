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
              <md-menu-item @click="join_confirm = true" v-if="current_chat"
                >Create Group</md-menu-item
              >
              <md-menu-item v-if="current_chat" @click="leave = true"
                >Leave Conversation</md-menu-item
              >
              <md-menu-item @click="logout = true">Log Out</md-menu-item>
            </md-menu-content>
          </md-menu>
          <md-dialog :md-active.sync="join_confirm">
            <md-dialog-title
              v-if="current_chat && current_chat.id.length === 20"
              >Choose a third member to form a group</md-dialog-title
            >
            <md-dialog-title
              v-if="current_chat && current_chat.id.length === 10"
              >Add a new member to the chat</md-dialog-title
            >
            <md-content id="add_group_panel">
              <md-field v-if="current_chat && current_chat.id.length === 20">
                <label for="member">User</label>
                <md-select
                  v-model="new_member"
                  name="member"
                  v-if="person_list"
                >
                  <md-option
                    v-for="c in person_list"
                    :key="c.id"
                    :value="JSON.stringify(c)"
                    >{{ c.names }}</md-option
                  >
                </md-select>
              </md-field>

              <!-- <md-field v-else>
                <label for="member">User</label>
                <md-select v-model="third" name="member">
                  <md-option value="fight-club">Fight Club</md-option>
                </md-select>
              </md-field> -->
            </md-content>

            <md-dialog-actions>
              <md-button class="md-primary" @click="join_confirm = false"
                >Cancel</md-button
              >
              <md-button class="md-primary" @click="join_group()"
                >Confirm</md-button
              >
            </md-dialog-actions>
          </md-dialog>
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
        <md-empty-state v-if="!current_chat">
          <md-icon class="md-size-5x">🤣</md-icon><br /><br>
          <span class="md-display-1">Start a conversation!</span>
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
      join_confirm: false,
      new_member: "",
    };
  },
  props: {
    username: String,
    id: String,
    mobile: Boolean,
    showlist: Boolean,
    current_chat: Object,
    current_messages: Array,
    person_list: Array,
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
  // beforeDestroy() {
  //   this.close_app();
  // },
  methods: {
    // #region gui related
    handleEmojiPicked(e) {
      document.getElementById("textbox").innerHTML += e;
      // this.new_message = document.getElementById("textbox").textContent;
    },
    togglelist() {
      this.listshow = !this.showlist;
      this.$emit("togglelist", this.listshow);
    },
    // #endregion
    // #region Network related
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
    join_group() {
      if (this.new_member == "") {
        this.join_confirm = false;
        return;
      }
      // Only in one-to-one chat
      var newmember = eval("(" + this.new_member + ")");
      if (this.current_chat.id.length === 20) {
        var member = {};
        member[this.id] = this.username;
        member[newmember.id] = newmember.names;
        member[this.current_chat.id] = this.current_chat.member[
          this.current_chat.id
        ];
        this.$root.s.emit("create_group", { sender: this.id, member: member });
      } else {
        this.$root.s.emit("join_group", {
          groupid: this.current_chat.id,
          sender: newmember.id,
        });
      }
      this.new_member = "";
      this.join_confirm = false;
    },
    logout_confirm() {
      this.$router.push("/");
      this.logout = false;
    },
    leave_confirm() {
      if (this.current_chat.id.length !== 20) {
        this.$root.s.emit("leave_group", {
          groupid: this.current_chat.id,
          sender: this.id,
        });
      }
      this.$emit("quit_chat", null);
      this.leave = false;
    },
    close_app() {
      this.$root.s.emit("logout", { sender: this.id });
      for (var listener in this.$root.s.$events) {
        if (listener != undefined) {
          this.$root.s.removeAllListeners(listener);
        }
      }
      this.$root.s.close();
      if (!this.$root.s.connected) {
        this.$root.id = "";
        this.$root.username = "";
        this.$root.contact = {};
        this.$root.s = null;
      }
    },
    // #endregion
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

#add_group_panel {
  padding: 30px;
}
</style>