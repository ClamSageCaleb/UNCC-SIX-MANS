<template>
  <main>
    <NavBar />
    <Home />
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "./components/NavBar.vue"
import Home from "./components/Home.vue"

export default defineComponent({
  name: "App",
  components: {
    NavBar,
    Home,
  },
})
</script>

<style>
#app {
  scroll-behavior: smooth;
  font-family: "Roboto";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
}
</style>
