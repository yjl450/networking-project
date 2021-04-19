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
                @click="join_chat(c)"
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
      // id: -1,
      // username: "",
      id: this.$root.id,
      username: this.$root.username,

      // Display related
      mobile: false,
      initial: true,
      showlist: false,

      // Chat list content
      current_chat: null,

      chat_list: [102790, 1029981],
      // contact_list:{
      //   person:{},
      //   group:{},
      // },
      contact_list: {
        person: {
          102790: {
            102790: "Perry",
          },
          106290: {
            106290: "Maggie",
          },
        },
        group: {
          1029981: {
            10010: "hellen",
            10030: "mike",
            10040: "carol",
            10050: "vera",

            10060: "hellen",
            10070: "mike",
            10080: "carol",
            10090: "vera",

            10100: "hellen",
            10130: "mike",
            10240: "carol",
            10250: "vera",
          },
          1078981: {
            10010: "hellen",
            10030: "mike",
            10040: "carol",
            10050: "vera",
            13479: "Harry",
          },
        },
      },
      chat_message: {
        1029981: [
          { sender: 10040, message: "hello" },
          {
            sender: 10010,
            message: "Nice to meet you!",
          },
          { sender: 10040, message: "wefuwifhwiuofhuwfhhwfiuhwiufhwihfuihiw" },
          { sender: 10040, message: "hello" },
          { sender: 10040, message: "hello" },
          {
            sender: 10010,
            message: "Nice to meet you!",
          },
          { sender: 10040, message: "wefuwifhwiuofhuwfhhwfiuhwiufhwihfuihiw" },
          { sender: 10040, message: "hello" },
          { sender: 10040, message: "hello" },
          {
            sender: 10010,
            message: "Nice to meet you!",
          },
          { sender: 10040, message: "wefuwifhwiuofhuwfhhwfiuhwiufhwihfuihiw" },
          { sender: 10040, message: "hello" },
        ],
      },
    };
  },
  created() {
      // Back to login page if no login token
    if (this.$root.id !== "") {
      this.id = this.$root.id;
      this.username = this.$root.username;
    } else {
      this.$router.push("/");
    }
  },
  mounted() {
    this.resize();
    window.onresize = this.resize;
  },
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
        newObj.sender = this.current_chat.member[e.sender];
        newObj.message = e.message;
        newObj.me = e.sender === this.id;
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
        if (this.chat_list[cid] % 10 === 0) {
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
      var id = 0;
      for (var i in this.contact_list.group) {
        id = parseInt(i);
        if (!this.chat_list.includes(id)) {
          var newObj = {};
          newObj.id = id;
          newObj.names = this.chat_naming(this.contact_list.group[id]);
          newObj.member = this.contact_list.group[id];
          returnArray.push(newObj);
        }
      }
      return returnArray;
    },

    person_list() {
      var returnArray = [];
      var id = 0;
      for (var i in this.contact_list.person) {
        id = parseInt(i);
        if (!this.chat_list.includes(id)) {
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
    join_chat(c) {
      this.current_chat = {};
      this.current_chat.id = c.id;
      this.current_chat.member = c.member;
      this.chat_list.push(c.id);
      this.chat_message[c.id] = [];
      if (this.mobile && this.showlist) {
        this.showlist = !this.showlist;
      }
    },
    chat_naming(name_record) {
      var names = { ...name_record };
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
    togglelist(showlist) {
      this.showlist = showlist;
    },
    quit_chat(q) {
      delete this.chat_message[this.current_chat.id];
      this.chat_message = { ...this.chat_message };
      this.chat_list = this.chat_list.filter(
        (item) => item !== this.current_chat.id
      );
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
