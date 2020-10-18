<template>
  <div>
    <button id="open-sidebar" @click="state.open = true">
      <img src="../assets/open_sidebar.svg" />
    </button>
    <div class="sidebar-backdrop" @click="state.open = false" v-if="state.open"></div>
    <transition name="slide">
      <div id="side-nav" v-if="state.open">
        <nav id="nav-container" class="center">
          <button id="close-sidebar" @click="state.open = false"><img src="../assets/close.svg" /></button>
          <a href="#">
            <img src="../assets/home.svg" />
            Home
          </a>
          <a href="#commands">
            <img src="../assets/commands.svg" />
            Commands
          </a>
          <a href="#hall-of-fame">
            <img src="../assets/hall_of_fame.svg" />
            Hall of Fame
          </a>
          <a href="#leaderboard">
            <img src="../assets/leaderboard.svg" />
            Leaderboard
          </a>
        </nav>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "NavBar",
  data: () => {
    return {
      state: {
        open: false,
      },
    }
  },
})
</script>

<style lang="scss" scoped>
button {
  cursor: pointer;
}
#open-sidebar {
  position: absolute;
  top: 0;
  left: 0;
  background-color: transparent;
  border: none;
  padding: 0;
}
.sidebar-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  cursor: pointer;
}
#side-nav {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 125px;
  background-color: #00703c;
  padding: 0px 30px;
  overflow: auto;

  nav {
    display: flex;
    flex-direction: column;
    max-height: 100%;

    #close-sidebar {
      background-color: transparent;
      border: none;
      margin: 12px auto 0px auto;
      width: fit-content;
      padding: 6px;
    }

    a {
      font-size: 18px;
      font-weight: bold;
      color: #e5e5e5;
      font-family: "Play";
      text-decoration: none !important;
      margin-top: 5vh;
      text-align: center;

      img {
        width: 50%;
        display: block;
        margin: auto;
      }
    }
  }
}
.slide-enter-active {
  animation: slide-in 200ms;
}
.slide-leave-active {
  animation: slide-in 200ms reverse;
}
@keyframes slide-in {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0px);
  }
}
</style>