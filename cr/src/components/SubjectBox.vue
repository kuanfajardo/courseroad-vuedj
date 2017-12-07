<template>
  <b-row class="subject-box">
    <b-col cols="12">
      <b-row>
        <b-col cols="12" class="px-0">
          <b-dropdown :text="navText" right id="bucketDrop" size="lg">
            <b-dropdown-header id="header0">Requirements</b-dropdown-header>
            <b-dropdown-item v-for="bucket in reqs" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
            <b-dropdown-header v-if="custom.length > 0" id="header1">Buckets</b-dropdown-header>
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
        selectedBucketIndex: 0
      }
    },

    props: ['buckets'],

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
        this.selectedBucketIndex = this.buckets.indexOf(bucket)
      }
    },

    computed: {
      navText: function () {
        var selected = this.buckets[this.selectedBucketIndex]

        if (selected === undefined) {
          return ''
        }

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
        var bucket = this.buckets[this.selectedBucketIndex]

        if (bucket === undefined) {
          return []
        }

        return bucket.cells
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
