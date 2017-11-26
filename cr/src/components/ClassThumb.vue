<template>
  <span v-on:dragstart="dragStart">
    <button type="button" class="class-thumb" draggable="true">{{ text }}</button>
  </span>
</template>

<script>
  export default {
    name: 'class-thumb',

    data () {
      return {
        msg: 'msg'
      }
    },

    props: ['text'],

    methods: {
      dragStart (event) {
        var obj = JSON.stringify({
          oldSemester: -1,
          oldYear: -1,
          number: this.text
        })

        event.dataTransfer.setData('text', obj)
        event.dataTransfer.effectAllowed = 'move'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .class-thumb {
    background-color: #758acf;
    color: #FFFFFF;
    font-size: small;
    border: none;
    border-radius: 4pt;
    padding: .3rem .2rem;
    outline: none;
    width: 100%;
    height: auto;
    max-width: 6rem;
  }

</style>
