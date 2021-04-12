<template>
  <div class="login-border">
    <div class="login-back">
      <div class="login-box">
        <span class="md-headline">Welcome</span>
        <md-field :class="validation">
          <label>Username</label>
          <md-input v-model="username"></md-input>
          <span class="md-error">{{ validationMessage }}</span>
        </md-field>
        <br />
        <md-button class="md-fab login-button" v-on:click="submit()">
          <md-icon> arrow_forward_ios</md-icon>
        </md-button>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Vue from "vue";
import { MdButton, MdField } from "vue-material/dist/components";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";

Vue.use(MdButton);
Vue.use(MdField);

export default {
  name: "Home",
  components: {},
  data() {
    return { username: "", validationMessage: "" };
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
        this.validationMessage = "Please enter your username.";
        return;
      }
      if (this.username) {
        this.validationMessage =
          "This username is in use. Please choose a new one.";
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
</style>
