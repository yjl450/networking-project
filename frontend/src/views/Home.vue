<template>
  <div class="login-border">
    <div class="login-back">
      <div class="login-box">
        <div id="login-input">
          <span class="md-title"
            >Welcome<br />
            Let's start a <span id="logo">Convo!</span></span
          ><br />
          <md-field :class="validation">
            <label>Username</label>
            <md-input v-model="name" maxlength="10" required @input="validate()"></md-input>
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
import { io } from "socket.io-client";
export default {
  name: "Home",
  components: {},
  data() {
    return {
      name: "",
      validationMessage: "",
      // id: -1,
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
    validate() {
      if (this.name === "") {
        this.validationMessage = "Please enter a username.";
        return false;
      } else {
        this.validationMessage = "";
        return true;
      }
    },
    submit() {
      // Send username to server, get user id, redirect to chatting page
      if (!this.validate()) {
        return;
      }
      if (this.$root.s === null) {
        console.log(process.env.VUE_APP_BASE_API);
        this.$root.s = io(process.env.VUE_APP_BASE_API);
      }
      this.$root.s.on("login-response", (r) => {
        if (r["result"] === "success") {
          this.$root.username = r["username"];
          this.$root.id = r["userid"];
          this.$router.push("main");
        }
        if (r["result"] === "duplicate") {
          // No repeat username
          this.validationMessage =
            "This username is in use. Please choose a new one.";
        }
      });
      this.$root.s.on("contact", (r) => {
        this.$root.contact = r;
      });
      this.$root.s.emit("login", { username: this.name });
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
  --md-theme-default-primary: #6c5ce7 !important;
}

.md-focused label {
  color: #6c5ce7 !important;
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

#logo {
  font-family: "Libre Baskerville", serif;
}
</style>
