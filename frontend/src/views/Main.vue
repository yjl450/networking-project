<template>
  <div class="main md-layout">
    <transition
  name="slideLeft"
  enter-active-class="slideInLeft"
  leave-active-class="slideOutLeft"
>
    <div class="md-layout-item" id="list" v-show="(mobile && showlist) || !mobile">
     
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
            <md-list-item class="md-inset">World</md-list-item>
          </md-list>
        </md-list-item>

        <md-list-item md-expand :md-expanded.sync="initial">
          <md-icon>person_add</md-icon>
          <h3 class="md-list-item-text">Contacts</h3>

          <md-list slot="md-expand">
            <md-list-item class="md-inset">Console</md-list-item>
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
    <div class="md-layout-item" id="chat-panel" v-show="!mobile || (mobile && !showlist)">
     
      <Chat
        :current_chat="current_chat"
        :mobile="mobile"
        :showlist="showlist"
        v-on:togglelist="togglelist"
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
      id: -1,
      username: "",

      // Display related
      mobile: false,
      initial: true,
      showlist: false,

      // Chat list content
      current_chat: null,
      // current_chat: {
      //   id: 10020,
        // member: {
        //   10010: "hellen",
        //   10030: "mike",
        //   10040: "carol",
        //   10050: "vera",

        //   10060: "hellen",
        //   10070: "mike",
        //   10080: "carol",
        //   10090: "vera",

        //   10100: "hellen",
        //   10130: "mike",
        //   10240: "carol",
        //   10250: "vera",
        // },
      // },
      chat_list: null,
    };
  },
  created() {
    //   Back to login page if no login token
    // if (window.sessionStorage.getItem("id")) {
    //   this.id = window.sessionStorage.getItem("id");
    //   this.username = window.sessionStorage.getItem("username");
    // } else {
    //   this.$router.push("/");
    // }
  },
  mounted() {
    this.resize();
    window.onresize = this.resize;
  },
  computed: {
  },
  methods: {
    togglelist(showlist) {
      this.showlist = showlist;
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
        document.getElementById("chat").style.width = (window.innerWidth / 4)*3 + "px";
        document.getElementById("chat").style.marginLeft = (window.innerWidth / 4) + "px";
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
