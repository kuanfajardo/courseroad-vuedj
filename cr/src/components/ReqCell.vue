<template>
  <b-container class="req-cell" fluid>
     <b-row align-h="between" align-v="center">
      <b-col cols="8" class="pt-3">
        <p>{{ cell.name }}</p>
      </b-col>
      <b-col cols="2">
        <button type="button" class="collapse-button py-1" v-on:click="collapsed()">{{ buttonText }}</button>
      </b-col>
    </b-row>
    <b-row :class="[ collapse ? 'pb-0' : 'pb-3' ]">
      <b-col cols="12">
        <b-container v-if="!collapse" class="px-0">
          <b-row v-for="(row, index) in cell.rows" align-v="center" align-h="between" :key="index">
            <b-col cols="8">
              <b-form-checkbox size="md" :style="{ 'margin-left': row.indentLevel * 1.5 + 'rem' }" v-model="row.checked" value="y" disabled>
               {{ row.text }}
              </b-form-checkbox>
            </b-col>
            <b-col cols="3">
              <!--<class-thumb v-if="row.buttonText !== ''" :text="row.buttonText"></class-thumb>-->
            </b-col>
          </b-row>
        </b-container>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  import ClassThumb from './ClassThumb'
  export default {
    name: 'req-cell',

    data () {
      return {
        collapse: true
      }
    },

    components: {
      ClassThumb
    },

    props: [ 'cell' ],

    methods: {
      collapsed () {
        this.collapse = !this.collapse
      }
    },

    computed: {
      buttonText: function () {
        return this.collapse ? '+' : '-'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.req-cell {
  border-style: solid;
  border-width: thin;
  border-left-style: none;
  border-right-style: none;
  border-color: #5e67b4;
  color: #000;
}


.custom-control-input:checked ~ .custom-control-indicator {
  color: #fff;
  background-color: #768bcd;
}

.collapse-button {
    background-color: #768bcd;
  border-radius: 1rem;
  border-style: none;
  color: #fff;
  width: 2rem;
}

.collapse-button:active {
  background-color: #768bcd;
}

.collapse-button:hover {
  background-color: #5e67b4;
}

.collapse-button:focus {
  outline: none;
}


</style>
