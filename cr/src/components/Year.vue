<template>
  <div class="year">
    <span class="year-label">
      {{ title }}
    </span>
    <br>
    <!--<semester v-for="semester in sem"-->
              <!--:key="yearID * 3 + semester['id']"-->
              <!--:id="yearID * 3 + semester['id']"-->
              <!--:class="semester['name'].toLowerCase()"-->
              <!--:hidden="semester['hidden']"-->
              <!--:classes="subjects[semester['id']]"-->
              <!--v-on:toggle="toggle"-->
              <!--v-on:drp="drp">-->
    <!--</semester>-->


    <semester v-for="semester in semesters"
              :key="semester.semester_id"
              :id="semester.semester_id"
              :class="semester.type"
              :hidden="semester.hidden"
              :classes="semester.subjects"
              :year="id"
              v-on:toggle="toggle"
              v-on:drp="drp">
    </semester>
  </div>
</template>

<script>
  import Semester from './Semester'

  export default {
    data () {
      return {
//        sem: [
//          {
//            id: 0,
//            name: 'Fall',
//            hidden: false
//          },
//
//          {
//            id: 1,
//            name: 'IAP',
//            hidden: true
//          },
//
//          {
//            id: 2,
//            name: 'Spring',
//            hidden: false
//          }
//        ]
      }
    },

    components: {
      Semester
    },

    props: [
      'semesters', 'title', 'id'
    ],

    methods: {
      toggle (cls) {
        this.$emit('toggle', cls)
      },

      drp (e) {
        this.$emit('drp', e)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .year {
    margin-top: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
  }


  .year-label {
    width: 100%;
    font-size: 1em;
  }

</style>
