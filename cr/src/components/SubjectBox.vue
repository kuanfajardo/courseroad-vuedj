<template>
  <div class="subject-box">
    <!--<p v-if="ok" align="right">course/subjects</p>-->
    <b-dropdown :text="navText" right id="bucketDrop" size="lg">
      <b-dropdown-header id="header0">Requirements</b-dropdown-header>
      <b-dropdown-item v-for="bucket in reqs" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
      <b-dropdown-header id="header1">Custom</b-dropdown-header>
      <b-dropdown-item v-for="bucket in custom" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
    </b-dropdown>
  </div>
</template>

<script>
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

</style>
