<template>
  <div class="info">
    <b-container>
      <b-row id="row1">
        <b-col id="col1" cols="4">
          <button type="button" id="deleteButton" v-on:click="deleteSubject" hidden>Delete</button>
        </b-col>
        <b-col cols="8" id="col2">
          <p align="right">{{selected.number}}</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <p class="subject-title"><b>{{ selected.title }}</b></p>
          <p class="units"><i>{{ selected.units }}</i></p>
          <p>{{ selected.description }}</p>
        </b-col>
      </b-row>
      <!--<b-row v-for="(property, index) in data" :key="index">-->
        <!--<b-col cols="4">-->
          <!--<p class="small-text"><b>{{ property.label }}</b></p>-->
        <!--</b-col>-->
        <!--<b-col cols="8">-->
          <!--<p class="small-text">{{ property.value }}</p>-->
        <!--</b-col>-->
      <!--</b-row>-->
    </b-container>
  </div>
</template>

<script>
  export default {
    name: 'info-box',

    components: [
//      'data'
    ],

    data () {
      return {

      }
    },

    methods: {
      deleteSubject () {
        this.$emit('deleteSubject')
      }
    },

    props: [
      'selected'
    ]
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .info {
    background-color: rgba(138, 149, 255, 0.24);
    min-height: 100%;
    min-width: 100%;

    justify-content: center;
  }

  #row1 {
    padding-top: 1rem;
    font-size: 1.5em;
    height: 40pt;
    padding-right: 0.5rem;
  }

  #col1 {
    color: #000000;
    padding-left: 1rem;
    /*background-color: #0c5460;*/
  }

  #col2 {
    color: #aeaeae;
    /*background-color: #00b3ee;*/
    font-size: 1.3rem;
  }

  #col3 {
    background-color: #3a33d1;
  }

  .small-text {
    font-size: 1rem;
    margin: 0.5em 0 0 0;
    padding: 0;
  }

  #deleteButton {
    margin-bottom: 3rem;
    font-size: 0.8rem;
    max-height: 70%;
    border-radius: 0.5rem;
    background-color: rgb(249, 247, 252);
    border-color: #e7f2fa;
  }

  .subject-title {
    margin-bottom: 0;
  }

  .units {
    margin-bottom: 0.3rem;
  }
</style>
