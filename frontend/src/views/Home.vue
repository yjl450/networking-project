<template>
  <div class="login-border">
    <div class="login-back">
      <div class="login-box">
        <div id="login-input">
          <span class="md-headline">Welcome</span><br /><br />
          <md-field :class="validation">
            <label>Username</label>
            <md-input v-model="username"></md-input>
            <span class="md-error">{{ validationMessage }}</span>
          </md-field>
          <br />
          <br />
          <md-button class="md-fab login-button" v-on:click="submit()">
            <md-icon> arrow_forward_ios</md-icon>
          </md-button>
        </div>
        <md-dialog :md-active.sync="showDialog">
          <md-tabs md-dynamic-height>
            <md-tab md-label="Credit" id="credit-content">
              <p>
                This project is created by Leyi Sun & Yijian Liu<br />
                For Computer Networking Spring 2021 <br /><br />
                Source:
                <a href="https://github.com/yjl450/networking-project"
                  >github.com/yjl450/networking-project</a
                >
              </p>
            </md-tab>
          </md-tabs>

          <md-dialog-actions>
            <md-button class="md-primary" @click="showDialog = false"
              >Close</md-button
            >
          </md-dialog-actions>
        </md-dialog>

        <md-button class="" id="credit" @click="showDialog = true"
          >Credit</md-button
        >
      </div>
    </div>
  </div>
</template>

<script>
// color palette https://flatuicolors.com/palette/us

// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Vue from "vue";
import {
  MdButton,
  MdField,
  MdDialog,
  MdTabs,
} from "vue-material/dist/components";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";

Vue.use(MdButton);
Vue.use(MdField);
Vue.use(MdDialog);
Vue.use(MdTabs);

export default {
  name: "Home",
  components: {},
  data() {
    return {
      username: "",
      validationMessage: "",
      id: -1,
      showDialog: false,
    };
  },
  computed: {
    validation() {
      return {
        "md-invalid": this.validationMessage,
      };
    },
  },
  mounted() {
    if (window.innerWidth <= 400) {
      document.getElementsByClassName("login-box")[0].style.border = "0";
    }
  },
  methods: {
    submit() {
      if (this.username === "") {
        // no empty username
        this.validationMessage = "Please enter your username.";
        return;
      }
      window.hello = 1;
      // Send username to server, get user id, redirect to chatting page
      // var ws = new WebSocket("ws://" + process.env.VUE_APP_BASE_API);

      if (this.username) {
        // No repeat username
        this.validationMessage =
          "This username is in use. Please choose a new one.";
        return;
      }
      // save login token
      if (this.id != -1) {
        window.sessionStorage.setItem("id", this.id);
        window.sessionStorage.setItem("username", this.username);
        this.$router.push("main");
      }
    },
  },
};
</script>

<style scoped>
.login-border {
  width: 100%;
  height: 100%;
  background-color: #e17055;
}

.login-back {
  width: calc(100%);
  height: calc(100%);
  border-radius: 3em;
  border: 2em solid #e17055;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.login-box {
  width: 400px;
  height: 600px;
  margin-left: 4em;
  margin-right: 4em;
  padding: 3em;
  border: 1px solid #bdbdbd;
  border-radius: 1em;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.login-button {
  background-color: #00b894 !important;
}

#login-input {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  flex: 1 0 auto;
  width: 200px;
}

#credit {
  flex: 0 0 auto;
}

#credit-content {
  padding: 20px;
}
</style>
