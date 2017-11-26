<template>
  <b-container class="req-cell py-3" fluid>
    <b-row v-for="row in rows" align-v="center" align-h="between">
      <b-col cols="8">
        <b-form-checkbox size="md" :style="{ 'margin-left': row.indentLevel + 'rem' }" v-model="row.checked" value="y" disabled>
          {{ row.text }}
        </b-form-checkbox>
      </b-col>
      <b-col cols="3">
        <class-thumb v-if="row.buttonText !== ''" :text="row.buttonText"></class-thumb>
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
        rows: [
          {
            text: '1 of:',
            indentLevel: 0,
            checked: 'n',
            buttonText: ''
          },
          {
            text: '6.01',
            indentLevel: 1,
            checked: 'y',
            buttonText: '6.01'
          },
          {
            text: '6.S08',
            indentLevel: 1,
            checked: 'n',
            buttonText: '6.S08'
          }
        ]
      }
    },

    components: {
      ClassThumb
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
}

.custom-control-input:checked ~ .custom-control-indicator {
  color: #fff;
  background-color: #768bcd;
}

</style>
