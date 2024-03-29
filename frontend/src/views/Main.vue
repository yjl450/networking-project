<template>
  <div class="main md-layout">
    <transition
      name="slideLeft"
      enter-active-class="slideInLeft"
      leave-active-class="slideOutLeft"
    >
      <div
        class="md-layout-item"
        id="list"
        v-show="(mobile && showlist) || !mobile"
        style="animation-duration: 0.3s"
      >
        <md-list :md-expand-single="mobile">
          <md-list-item>
            <h2 class="md-list-item-text" id="logo">Convo!</h2>
            <md-button
              class="md-icon-button"
              @click="showlist = !showlist"
              v-if="mobile"
            >
              <md-icon>arrow_forward</md-icon>
            </md-button>
          </md-list-item>
          <md-list-item md-expand>
            <md-icon>chat</md-icon>
            <h3 class="md-list-item-text">Chattings</h3>

            <md-list slot="md-expand">
              <md-list-item
                class="md-ripple"
                @click="returnChat(c)"
                v-for="c in connected_chat_list"
                :key="c.id"
                >{{ c.names }}</md-list-item
              >
            </md-list>
          </md-list-item>

          <md-list-item md-expand>
            <md-icon>group</md-icon>
            <h3 class="md-list-item-text">Groups</h3>

            <md-list slot="md-expand">
              <md-list-item
                class="md-ripple"
                v-for="c in group_list"
                :key="c.id"
                @click="list_join_group(c)"
                >{{ c.names }}
              </md-list-item>
            </md-list>
          </md-list-item>

          <md-list-item md-expand :md-expanded.sync="initial">
            <md-icon>person_add</md-icon>
            <h3 class="md-list-item-text">Contacts</h3>

            <md-list slot="md-expand">
              <md-list-item
                class="md-ripple"
                v-for="c in person_list"
                :key="c.id"
                @click="join_chat(c)"
                >{{ c.names }}
              </md-list-item>
            </md-list>
          </md-list-item>
        </md-list>
      </div>
    </transition>

    <transition
      name="slideRight"
      enter-active-class="slideInRight"
      leave-active-class="slideOutRight"
    >
      <div
        class="md-layout-item"
        id="chat-panel"
        v-show="!mobile || (mobile && !showlist)"
        style="animation-duration: 0.3s"
      >
        <Chat
          :current_chat="current_chat"
          :mobile="mobile"
          :id="id"
          :username="username"
          :current_messages="current_messages"
          :showlist="showlist"
          :person_list="person_list"
          v-on:new_message="new_message"
          v-on:togglelist="togglelist"
          v-on:quit_chat="quit_chat"
        />
      </div>
    </transition>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Vue from "vue";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";
import Chat from "@/components/Chat.vue";

Vue.use(VueMaterial);

export default {
  name: "Main",
  components: { Chat },
  data() {
    return {
      // current account
      id: this.$root.id,
      username: this.$root.username,

      // Display related
      mobile: false,
      initial: true,
      showlist: false,

      // Chat list content
      current_chat: null,
      chat_list: [],
      contact_list: {},
      chat_message: {},
    };
  },
  created() {
    // Back to login page if no login token
    if (this.$root.id !== "") {
      this.id = this.$root.id;
      this.username = this.$root.username;
    } else {
      this.$router.push("/");
      return;
    }

    // window.addEventListener("beforeunload", this.preventRefresh);
  },
  mounted() {
    window.onbeforeunload = () => {
      this.close_app();
      return undefined;
    };
    this.resize();
    window.onresize = this.resize;
    this.contact_list = this.$root.contact;
    // register contact update listener
    this.$root.s.on("contact", (r) => {
      this.contact_list = {};
      this.contact_list.person = r["person"];
      this.contact_list.group = r["group"];
      for (let i = 0; i < this.chat_list.length; i++) {
        if (
          !(this.chat_list[i] in this.contact_list.person) &&
          !(this.chat_list[i] in this.contact_list.group)
        ) {
          if (this.chat_message[this.chat_list[i]]) {
            delete this.chat_message[this.chat_list[i]];
          }
          if (this.current_chat.id === this.chat_list[i]) {
            this.current_chat = null;
          }
          this.chat_list.splice(i, 1);
        }
      }
    });
    this.$root.s.on("message", (r) => {
      this.new_message(r);
    });
    this.$root.s.on("update_group", this.group_nogui);
    this.$root.s.on("delete_group", this.group_delete);
  },
  // beforeDestroy() {
  //   this.close_app("");
  // },
  computed: {
    current_messages() {
      if (
        this.current_chat == null ||
        this.chat_message[this.current_chat.id] == undefined
      ) {
        return [];
      }
      var newArray = [];
      var i = 0;
      this.chat_message[this.current_chat.id].forEach((e) => {
        var newObj = {};
        newObj.sender = e["name"];
        newObj.message = e["message"];
        newObj.me = e["sender"] == this.id;
        newObj.index = i;
        i++;
        newArray.push(newObj);
      });
      return newArray;
    },
    connected_chat_list() {
      var returnArray = [];
      for (let cid = 0; cid < this.chat_list.length; cid++) {
        var newObj = {};
        //one-on-one
        if (this.chat_list[cid].length == 20) {
          newObj.names = this.chat_naming(
            this.contact_list.person[this.chat_list[cid]]
          );
          newObj.member = this.contact_list.person[this.chat_list[cid]];
        } else {
          // group chat
          newObj.names = this.chat_naming(
            this.contact_list.group[this.chat_list[cid]]
          );
          newObj.member = this.contact_list.group[this.chat_list[cid]];
        }
        newObj.id = this.chat_list[cid];
        returnArray.push(newObj);
      }
      return returnArray;
    },

    group_list() {
      var returnArray = [];
      var id = "";
      for (var i in this.contact_list.group) {
        id = i;
        if (!this.chat_list.includes(id)) {
          var newObj = {};
          newObj.id = id;
          newObj.names = this.chat_naming(this.contact_list.group[id], false);
          newObj.member = this.contact_list.group[id];
          returnArray.push(newObj);
        }
      }
      return returnArray;
    },

    person_list() {
      var returnArray = [];
      var id = "";
      for (var i in this.contact_list.person) {
        id = i;
        if (!this.chat_list.includes(id) && id !== this.id) {
          var newObj = {};
          newObj.id = id;
          newObj.names = this.contact_list.person[id][id];
          newObj.member = this.contact_list.person[id];
          returnArray.push(newObj);
        }
      }
      return returnArray;
    },
  },
  methods: {
    returnChat(c) {
      this.current_chat = {};
      this.current_chat.id = c.id;
      this.current_chat.member = c.member;
      if (this.mobile && this.showlist) {
        this.showlist = !this.showlist;
      }
    },
    group_gui(r) {
      console.log("GUI");
      var chatObj = {};
      chatObj.id = r["groupid"];
      chatObj.member = r["member"];
      this.join_chat(chatObj);
      this.$root.s.off("update_group", this.group_gui);
      this.$root.s.on("update_group", this.group_nogui);
    },
    group_nogui(r) {
      if (this.current_chat !== null && this.current_chat.id == r["groupid"]) {
        this.group_gui(r);
      } else {
        console.log("NOGUI");
        if (!this.chat_list.includes(r["groupid"])) {
          this.chat_list.push(r["groupid"]);
        }
      }
    },
    list_join_group(c) {
      this.$root.s.off("update_group", this.group_nogui);
      this.$root.s.on("update_group", this.group_gui);
      this.$root.s.emit("join_group", { groupid: c.id, sender: this.id });
    },
    group_delete(c) {
      if (!this.chat_list.includes(c.groupid)) {
        return;
      }
      if (this.current_chat !== null && this.current_chat.id === c.groupid) {
        this.quit_chat(null);
      } else {
        delete this.chat_message[c.groupid];
        this.chat_message = { ...this.chat_message };
        console.log("brefore", this.chat_list);

        this.chat_list.splice(this.chat_list.indexOf(c.groupid), 1);
        console.log("after", this.chat_list);
      }
    },
    join_chat(c) {
      this.current_chat = {};
      this.current_chat.id = c.id;
      this.current_chat.member = c.member;
      // this.chat_list.push(c.id);
      if (!this.chat_list.includes(c.id)) {
        this.chat_list.push(c.id);
      }
      if (this.mobile && this.showlist) {
        this.showlist = !this.showlist;
      }
    },
    chat_naming(name_record) {
      var names = { ...name_record };
      // delete names[this.id];
      names = Object.values(names);
      if (names.length > 1) {
        return "(" + names.length + ") " + names.join(", ");
      }
      return names[0];
    },
    togglelist(showlist) {
      this.showlist = showlist;
    },
    new_message(m) {
      var s = m.sender;
      var mm = m.message;
      var newObj = {};
      newObj["sender"] = s;
      newObj["message"] = mm;
      newObj["name"] = this.contact_list.person[s][s];
      if (m.receiver.length === 20 && m.sender !== this.id) {
        if (!this.chat_list.includes(m.sender)) {
          this.chat_list.push(m.sender);
        }
        if (this.chat_message[m.sender] === undefined) {
          this.chat_message[m.sender] = []; //[m.receiver] = [];
        }
        this.chat_message[m.sender].push(newObj);
        this.chat_message = { ...this.chat_message };
      } else {
        if (!this.chat_list.includes(m.receiver)) {
          this.chat_list.push(m.receiver);
        }
        if (this.chat_message[m.receiver] === undefined) {
          this.chat_message[m.receiver] = []; //[m.receiver] = [];
        }
        this.chat_message[m.receiver].push(newObj);
        this.chat_message = { ...this.chat_message };
      }
    },
    quit_chat(q) {
      delete this.chat_message[this.current_chat.id];
      this.chat_message = { ...this.chat_message };
      this.chat_list.splice(this.chat_list.indexOf(this.current_chat.id), 1);
      this.current_chat = q;
    },
    resize() {
      if (window.innerWidth <= 420) {
        this.mobile = true;
        document.getElementById("list").classList.remove("md-size-25");
        document.getElementById("list").style.width = window.innerWidth + "px";
        document.getElementById("chat").style.width = window.innerWidth + "px";
        document.getElementById("chat").style.marginLeft = "0";
        document.getElementById("title").style.width =
          document.getElementById("chat").style.width.replace("px", "") -
          136 +
          "px";
      } else if (window.innerWidth <= 840) {
        this.mobile = false;
        document.getElementById("list").classList.remove("md-size-25");
        document.getElementById("list").style.width = "210px";
        document.getElementById("chat").style.width =
          window.innerWidth - 210 + "px";
        document.getElementById("chat").style.marginLeft = 210 + "px";
        document.getElementById("title").style.width =
          window.innerWidth - 210 - 85 + "px";
      } else {
        this.mobile = false;
        document.getElementById("list").classList.add("md-size-25");
        document.getElementById("chat").style.width =
          (window.innerWidth / 4) * 3 + "px";
        document.getElementById("chat").style.marginLeft =
          window.innerWidth / 4 + "px";
        document.getElementById("title").style.width =
          (window.innerWidth / 4) * 3 - 85 + "px";
      }
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
      return "";
    },
  },
};
</script>

<style scoped>
.main {
  height: 100%;
  width: 100%;
  position: relative;
}

#logo {
  font-family: "Libre Baskerville", serif;
}

#list {
  height: 100%;
  overflow: auto;
  border-right: 1px solid #c9c9c9;
}

.md-layout-item {
  height: 100%;
  position: absolute;
}
</style>
