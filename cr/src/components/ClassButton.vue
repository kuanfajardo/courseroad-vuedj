<template>
  <span v-on:dragstart="dragStart">
    <button type="button" class=class-button :class="{ok: !hasConflict, red: hasConflict}" draggable="true">{{ text }}</button>
  </span>
</template>

<script>
  export default {
    name: 'class-button',

    data () {
      return {
        msg: 'msg'
      }
    },

    props: ['hasConflict', 'text', 'semester', 'index', 'year', 'obj'],

    methods: {
      dragStart (event) {
        var obj = JSON.stringify({
          index: this.index,
          oldSemester: this.semester,
          oldYear: this.year,
          obj: this.obj
        })

        event.dataTransfer.setData('text', obj)
        event.dataTransfer.effectAllowed = 'move'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .class-button {
    /*position: relative;*/
    color: #FFFFFF;
    font-size: large;
    border: none;
    border-radius: 4pt;
    padding: .65rem .5rem;
    outline: none;
    width: 100%;
    height: auto;
    max-width: 6rem;
  }

  .ok {
    background-color: #758acf;
  }

  .red {
    background-color: lightcoral;
  }

  button::selection {
    border-style: solid;
    border-color: white;
  }

  .selected {
    border-style: solid;
    border-color: white;
  }

</style>
