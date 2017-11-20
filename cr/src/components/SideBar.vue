<template>
  <b-container class="sidebar">
    <b-row>
      <b-col cols="4" class="sidebar1">
        <info-box v-on:deleteSubject="deleteSubjects" :selected="selected"></info-box>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="4" class="sidebar2">
        <subject-box></subject-box>
      </b-col>
    </b-row>
 </b-container>
</template>

<script>
import InfoBox from './InfoBox'
import SubjectBox from './SubjectBox'

export default {
  name: 'side-bar',

  data () {
    return {
      msg: 'msg'
    }
  },

  components: {
    InfoBox,
    SubjectBox
  },

  methods: {
    deleteSubjects () {
      this.$emit('deleteSubjects')
    }
  },

  props: [
    'selected'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.sidebar {
  position: fixed;
  /*top:50%;*/
  /*left:0;*/
  /*bottom: 50%;*/
  /*top: 0;*/
  /*right: 2%;*/
  height: 20rem;
  /*background-color: #0c5460;*/
}

.sidebar1 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  border-bottom-width: thin;
  border-bottom-color: #5e67b4;
  border-bottom-style: solid;

  padding-left: 0;
  margin-top: 0;
  padding-right: 2rem;
  /*background-color: #ffc520;*/
  min-height: 13rem;
  max-height: 13rem;
}

.sidebar2 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  padding-left: 0;
  padding-right: 2rem;
  background-color: rgba(252, 225, 229, 0.12);
  min-height: 34rem;
}

</style>
