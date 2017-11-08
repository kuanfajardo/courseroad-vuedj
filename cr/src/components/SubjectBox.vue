<template>
  <div class="subject-box">
    <p align="right">course/subjects</p>
  </div>
</template>

<script>
  export default {
    name: 'subject-box',

    data () {
      return {
        msg: 'msg'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .subject-box {
    /*background-color: rgba(138, 149, 255, 0.24);*/
    min-height: 100%;
    min-width: 100%;

    justify-content: center;
  }

  p {
    font-size: 1.5em;
    color: #aeaeae;
    padding-top: 1rem;
    padding-right: 1.5rem;
  }
</style>
