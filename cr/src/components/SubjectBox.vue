<template>
  <b-row class="subject-box">
    <b-col cols="12">
      <b-row>
        <b-col cols="12" class="px-0">
          <b-dropdown :text="navText" right id="bucketDrop" size="lg">
            <b-dropdown-header id="header0">Requirements</b-dropdown-header>
            <b-dropdown-item v-for="bucket in reqs" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
            <b-dropdown-header id="header1">Buckets</b-dropdown-header>
            <b-dropdown-item v-for="bucket in custom" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
          </b-dropdown>
        </b-col>
      </b-row>
      <b-row class="req-container">
        <b-col cols="12">
          <req-cell v-for="(cell, index) in selectedCells" :cell="cell" :key="index" :class="{ mid: index !== 0 }"></req-cell>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>
  import ReqCell from './ReqCell'

  export default {
    name: 'subject-box',

    data () {
      return {
        ok: true,
        selectedBucketID: 0,
        // Invariant: id === index in buckets
        buckets: [
          {
            custom: false,
            name: 'GIRs',
            id: 0,
            cells: [
              {
                name: 'Physics',
                rows: [
                  {
                    text: 'Physics I',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'Physics II',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  }
                ]
              },
              {
                name: 'Calculus',
                rows: [
                  {
                    text: 'Calculus I',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'Calculus II',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  }
                ]
              },
              {
                name: 'Biology',
                rows: [
                  {
                    text: '1 of:',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: '7.012',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '7.012'
                  },
                  {
                    text: '7.013',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '7.013'
                  },
                  {
                    text: '7.014',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '7.014'
                  },
                  {
                    text: '7.015',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '7.015'
                  },
                  {
                    text: '7.016',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: '7.016'
                  }
                ]
              },
              {
                name: 'Chemistry',
                rows: [
                  {
                    text: '1 of:',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: '5.111',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '5.111'
                  },
                  {
                    text: '5.112',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '5.112'
                  },
                  {
                    text: '3.091',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: '3.091'
                  }
                ]
              },
              {
                name: 'HASS',
                rows: [
                  {
                    text: 'Distribution',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'HASS-H',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'HASS-S',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'HASS-A',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'Concentration',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: 'Electives',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: 'HASS-E (1)',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'HASS-E (2)',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: ''
                  }
                ]
              },
              {
                name: 'REST',
                rows: [
                  {
                    text: 'REST (1)',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: 'REST (2)',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  }
                ]
              },
              {
                name: 'LAB',
                rows: [
                  {
                    text: 'Institute Lab',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  }
                ]
              }
            ]
          },
          {
            custom: false,
            name: '6-3',
            id: 1,
            cells: [
              {
                name: 'Intro/Programming',
                rows: [
                  {
                    text: '1 of:',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: 'Path One',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '1 of:',
                    indentLevel: 2,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '6.01',
                    indentLevel: 3,
                    checked: 'y',
                    buttonText: '6.01'
                  },
                  {
                    text: '6.S08',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.S08'
                  },
                  {
                    text: '6.S080',
                    indentLevel: 2,
                    checked: 'n',
                    buttonText: '6.S080'
                  },
                  {
                    text: 'Path Two',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '1 of:',
                    indentLevel: 2,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '6.01',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.01'
                  },
                  {
                    text: '6.S08',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.S08'
                  },
                  {
                    text: '6.02',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.02'
                  },
                  {
                    text: '6.03',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.03'
                  },
                  {
                    text: '1 of:',
                    indentLevel: 2,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '6.0001',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.0001'
                  },
                  {
                    text: '6.0002',
                    indentLevel: 3,
                    checked: 'n',
                    buttonText: '6.0002'
                  }
                ]
              },
              {
                name: 'Foundation',
                rows: [
                  {
                    text: '6.004',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: '6.004'
                  },
                  {
                    text: '6.006',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: '6.006'
                  },
                  {
                    text: '6.009',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: '6.009'
                  }
                ]
              },
              {
                name: 'Header',
                rows: [
                  {
                    text: '6.031',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: '6.031'
                  },
                  {
                    text: '6.033',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: '6.033'
                  },
                  {
                    text: '1 of:',
                    indentLevel: 0,
                    checked: '',
                    buttonText: ''
                  },
                  {
                    text: '6.034',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '6.034'
                  },
                  {
                    text: '6.036',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '6.036'
                  },
                  {
                    text: '1 of:',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: ''
                  },
                  {
                    text: '6.045',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '6.045'
                  },
                  {
                    text: '6.046',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: '6.046'
                  }
                ]
              },
              {
                name: 'Communication',
                rows: [
                  {
                    text: '1 of',
                    indentLevel: 0,
                    checked: 'n',
                    buttonText: ''
                  },
                  {
                    text: '6.UAR',
                    indentLevel: 1,
                    checked: 'y',
                    buttonText: '6.UAR'
                  },
                  {
                    text: '6.UAT',
                    indentLevel: 1,
                    checked: 'n',
                    buttonText: '6.UAT'
                  }
                ]
              },
              {
                name: 'AUS',
                rows: [
                  {
                    text: 'AUS',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: 'AUS'
                  }
                ]
              },
              {
                name: 'EECS',
                rows: [
                  {
                    text: 'EECS',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: 'EECS'
                  }
                ]
              },
              {
                name: 'II',
                rows: [
                  {
                    text: 'II',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: 'II'
                  }
                ]
              },
              {
                name: 'Math',
                rows: [
                  {
                    text: '6.042',
                    indentLevel: 0,
                    checked: 'y',
                    buttonText: '6.042'
                  }
                ]
              }
            ]
          },
          {
            custom: true,
            name: 'HASS Ideas',
            id: 2,
            cells: []
          },
          {
            custom: true,
            name: 'Want To Take',
            id: 3,
            cells: []
          }
        ]
      }
    },

    methods: {
      keyPressed (event) {
        var key = event.key

        switch (key) {
          case 'ArrowLeft':
            alert('left key pressed')
            break
          case 'ArrowRight':
            alert('right key pressed')
            break
        }
      },

      updateBucket (bucket) {
        this.selectedBucketID = bucket.id
      }
    },

    computed: {
      navText: function () {
        var selected = this.buckets[this.selectedBucketID]
        return selected.name
      },

      reqs: function () {
        var requirements = []

        for (var i = 0; i < this.buckets.length; i++) {
          var bucket = this.buckets[i]

          if (!bucket.custom) {
            requirements.push(bucket)
          }
        }

        return requirements
      },

      custom: function () {
        var customBuckets = []

        for (var i = 0; i < this.buckets.length; i++) {
          var bucket = this.buckets[i]

          if (bucket.custom) {
            customBuckets.push(bucket)
          }
        }

        return customBuckets
      },

      selectedCells: function () {
        return this.buckets[this.selectedBucketID].cells
      }
    },

    created: function () {
      window.addEventListener('keyup', this.keyPressed)
    },

    components: {
      ReqCell
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .subject-box {
    /*background-color: rgba(138, 149, 255, 0.24);*/
    min-height: 100%;
    min-width: 100%;
    color: #aeaeae;
    justify-content: center;
    overflow: scroll;
    height: 100%;
  }

  #bucketDrop {
    width: 100%;
  }

  #bucketDrop__BV_toggle_ {
    width: 100%;
    background-color: #dfe2fa;
    color: #000000;
    border-width: 0;
    border-radius: 0;
    border-color: #5e67b4;
    border-bottom-width: thin;
  }

  .req-container {
    margin-top: 1rem;
  }

  .req-cell.mid {
    border-top-style: none;
  }

  .btn {
    background-color: #5e67b4;
    border-style: none;
  }

</style>
