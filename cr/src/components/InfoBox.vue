<template>
  <div class="info">
    <b-container>
      <b-row id="row1">
        <b-col id="col1" cols="4">
          <!--<button type="button" id="deleteButton" v-on:click="deleteSubject">Delete</button>-->
        </b-col>
        <b-col cols="8" id="col2">
          <p align="right">{{selected.number}}</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <p class="subject-title"><b>{{ selected.title }}</b></p>
          <p class="units"><i>{{ selected.units }}</i></p>
          <!--<p>{{ selected.description }}</p>-->
          <!--<button type="button" class="cr-button" :href="catalogLink">Subject Catalog</button>-->
          <!--<button type="button" class="cr-button" v-on:click="deleteSubject">Course Evaluations</button>-->
          <!--<button type="button" class="cr-button" v-on:click="deleteSubject">Delete</button>-->
          <b-button class="cr-button" size="sm" @click="openCatalogLink" :hidden="selected.hideLinks">Subject Catalog</b-button>
          <b-button class="cr-button" size="sm" @click="openEvalLink" :hidden="selected.hideLinks">Course Evaluations</b-button>
          <b-button class="cr-button" size="sm" @click="deleteSubject" :hidden="selected.hideDelete">Delete</b-button>
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
      },

      openCatalogLink () {
        window.open(
          this.catalogLink,
          '_blank' // <- This is what makes it open in a new window.
        )
      },

      openEvalLink () {
        window.open(
          this.evalLink,
          '_blank' // <- This is what makes it open in a new window.
        )
      }
    },

    props: [
      'selected'
    ],

    computed: {
      catalogLink: function () {
        return 'http://student.mit.edu/catalog/search.cgi?search=' + this.selected.number + '&style=verbatim'
      },

      evalLink: function () {
        return 'https://edu-apps.mit.edu/ose-rpt/subjectEvaluationSearch.htm?termId=&departmentId=&subjectCode=' + this.selected.number + '&instructorName=&search=Search'
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

  .cr-button {
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-size: 0.8rem;
    max-height: 70%;
    border-radius: 0.5rem;
    background-color:#758acf;
    border-color: #364ca7;
    border-style: solid;
    color: #ffffff;
    margin-left: 0.1rem;
    margin-right: 0.1rem;
  }

  .subject-title {
    margin-bottom: 0;
  }

  .units {
    margin-bottom: 0.3rem;
  }
</style>
