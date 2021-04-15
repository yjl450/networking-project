<template>
  <div>main page</div>
</template>

<script>
// color palette https://flatuicolors.com/palette/us

// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Vue from "vue";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";

Vue.use(VueMaterial);

export default {
  name: "Main",
  components: {},
  data() {
    return {
      id: -1,
      username: "",
    };
  },
  computed: {},
  created() {
    //   Back to login page if no login token
    // if (window.sessionStorage.getItem("id")) {
    //   this.id = window.sessionStorage.getItem("id");
    //   this.username = window.sessionStorage.getItem("username");
    // } else {
    //   this.$router.push("/");
    // }
  },
  mounted() {},
  methods: {
    submit() {},
  },
};
</script>

<style scoped>
</style>
