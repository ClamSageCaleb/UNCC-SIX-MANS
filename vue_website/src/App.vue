<template>
  <NavBar />
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "./components/NavBar.vue"

export default defineComponent({
  name: "App",
  components: {
    NavBar,
  },
})
</script>

<style>
#app {
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
}
</style>
