<template>
  <section id="home">
    <div class="container">
      <div class="text">
        <h1>Norm the Six Mans Bot</h1>
        <h2>The official six mans Discord bot for the UNC Charlotte Rocket League Community.</h2>
        <div class="sub-text">
          <h3>Created by Caleb, Twan, and Tux</h3>
          <h3>Check out the latest release <a href="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/releases">here <img alt="Github" src="../assets/github.svg" width="25" /></a></h3>
        </div>
      </div>
      <div class="logo">
        <img alt="Six Mans Logo" src="../assets/SixMansLogo.png" />
      </div>
    </div>
  </section>
</template>

<script lang="ts">
export default {

}
</script>

<style lang="scss" scoped>
  #home {
    height: 100vh;

    .container {
      display: flex;
      justify-content: center;
      place-items: center;
      height: 90%;
      flex-wrap: wrap-reverse;

      .text {
        width: 50%;

        .sub-text {
          display: flex;
          justify-content: space-between;
          margin-top: 80px;

          img {
            vertical-align: middle;
            margin-left: 6px;
            margin-top: -6px;
          }
        }
      }

      .logo {
        width: 35%;
        margin-left: 60px;
        img {
          width: 100%;
        }
      }
    }
  }

  h1 {
    font-family: "Play";
    color: #ffffff;
    font-size: 4.5rem;
    margin-bottom: 16px;
  }

  h2 {
    color: #d4d4d4;
    font-size: 1.63rem;
    font-weight: normal;
  }

  h3 {
    font-weight: normal;
    font-size: 1.5rem;
    color: #d4d4d4;
  }

  a {
    text-decoration: none;
    color: #EBDF8C;

    &:hover {
      text-decoration: underline;
    }
  }
</style>