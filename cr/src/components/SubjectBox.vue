<template>
  <div class="subject-box">
    <!--<p v-if="ok" align="right">course/subjects</p>-->
    <b-dropdown :text="navText" right id="bucketDrop" size="lg">
      <b-dropdown-header id="header0">Requirements</b-dropdown-header>
      <b-dropdown-item v-for="bucket in reqs" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
      <b-dropdown-header id="header1">Custom</b-dropdown-header>
      <b-dropdown-item v-for="bucket in custom" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
    </b-dropdown>

    <b-container class="req-container">
      <req-cell v-for="(cell, index) in cells" :cell="cell" :key="index" :class="{ mid: index !== 0 }"></req-cell>
    </b-container>
  </div>
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
            id: 0
          },
          {
            custom: false,
            name: '6-3',
            id: 1
          },
          {
            custom: true,
            name: 'HASS Ideas',
            id: 2
          },
          {
            custom: true,
            name: 'Want To Take',
            id: 3
          }
        ],
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
    /*overflow-style: auto;*/
  }

  /*p {*/
    /*font-size: 1.5em;*/
    /*padding-top: 1rem;*/
    /*padding-right: 1.5rem;*/
  /*}*/

  .navbar {
    background-color: rgba(138, 149, 255, 0.29);
  }

  #navTitle {
    color: #0a0a0a;
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
    /*width: 100%;*/
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
