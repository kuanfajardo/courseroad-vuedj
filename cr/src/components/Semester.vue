<template>
  <div class="semester"
       :hidden="hidden"
       v-on:dragover="dragOver"
       v-on:dragleave="dragLeave"
       v-on:drop="drop"
      :class="{ dropzone : dropzone }">

    <b-container fluid class="semester-container pl-5 pr-5">
      <b-row v-for="row in num_rows" class="row" :key="row">
        <b-col v-for="(cls, index) in classes" class="class-col" cols="2" :key="cls.number">
          <class-button
              :text="cls.number"
              @click.native="toggle($event.target, cls, index)"
              :hasConflict="cls.has_conflict"
              :semester="id"
              :index="index"
              :year="year"
              :obj="cls">
          </class-button>
        </b-col>
      </b-row>
    </b-container>
  </div>

</template>

<script>
  import ClassButton from './ClassButton.vue'

  export default {
    data () {
      return {
        dropzone: false,
        draggedSubject: null,
        num_rows: parseInt(this.classes.length / 6) + 1
      }
    },

    props: [
      'hidden', 'classes', 'id', 'year'
    ],

    components: {
      'class-button': ClassButton
    },

    methods: {
      toggle (target, cls, index) {
        target.classList.toggle('selected')
        this.$emit('toggle', {
          target: target,
          name: cls.number,
          semester: this.id,
          year: this.year,
          index: index
        })
      },

      dragOver (event) {
        event.preventDefault()
        event.dataTransfer.dropEffect = 'move'
        this.dropzone = true
      },

      dragLeave () {
        this.dropzone = false
      },

      drop (event) {
        this.dropzone = false
        var obj = JSON.parse(event.dataTransfer.getData('text'))

        // Edit semester!
        obj.semester_id = this.id

        this.$emit('drp', {
          oldSemester: obj.oldSemester,
          oldYear: obj.oldYear,
          index: obj.index,
          newYear: this.year,
          newSemester: this.id,
          obj: obj.obj
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .semester {
    margin: 0;
    /*background-color: #f7e1b5;*/
    min-height: 75pt;
    width: 100%;
    height: 3rem;
    /*color: #000000;*/
    /*font-size: 1rem;*/
    border-radius: 7pt;
    display: block;
    opacity: 1.0;
  }

  p {
    margin-left: 1%;
    margin-top: 1%;
  }

  .semester-container {
    align-items: center;
    height: 100%;
    border-radius: 7pt;
    background-color: transparent;
  }

  .class-col {
    /*background-color: #1b1e21;*/
    align-items: center;
  }

  .row {
    align-items: center;
    height: 100%;
  }

  .fall {
    background-color: #f7e1b5;
  }


  .spring {
    background-color: #00d6b2;
  }


  .iap {
    background-color: #cee0f3;
  }

  .dropzone {
    opacity: 0.5;
  }

</style>
