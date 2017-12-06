<template>
  <b-row id="sidebar">
    <b-col cols="12">
      <b-row id="sidebar1">
        <b-col cols="12">
          <info-box v-on:deleteSubject="deleteSubjects" :selected="selected"></info-box>
        </b-col>
      </b-row>
      <b-row id="sidebar2">
        <b-col cols="12">
          <subject-box></subject-box>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
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

#sidebar {
  position: fixed;
  width: 25%;
}

#sidebar1 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  border-bottom-width: thin;
  border-bottom-color: #5e67b4;
  border-bottom-style: solid;

  margin-top: 0;
  min-height: 12rem;
  max-height: 12rem;
}

#sidebar2 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  background-color: rgba(252, 225, 229, 0.12);
  min-height: 35rem;
  max-height: 35rem;
  overflow: hidden;
}

</style>
