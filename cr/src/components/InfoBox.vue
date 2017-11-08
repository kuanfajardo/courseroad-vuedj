<template>
  <div class="info">
    <b-container>
      <b-row id="row1">
        <b-col id="col1" cols="4">
          <p></p>
        </b-col>
        <b-col cols="8" id="col2">
          <p align="right">8.01</p>
        </b-col>
      </b-row>
      <b-row v-for="property in data">
        <b-col cols="4">
          <p class="small-text"><b>{{ property.label }}</b></p>
        </b-col>
        <b-col cols="8">
          <p class="small-text">{{ property.value }}</p>
        </b-col>
      </b-row>
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
        data: [
          {
            label: 'Name', value: 'Elements of Sofware Construction'
          },
          {
            label: 'Units', value: '5-0-7'
          },
          {
            label: 'Description', value: 'Hello. Physics is HARD.'
          }
        ]
      }
    }
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
  }

  #col3 {
    background-color: #3a33d1;
  }

  .small-text {
    font-size: 1rem;
    margin: 0.5em 0 0 0;
    padding: 0;
  }
</style>
