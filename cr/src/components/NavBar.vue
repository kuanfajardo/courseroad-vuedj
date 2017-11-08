<template>
  <b-navbar toggleable="md" type="dark" sticky>
    <b-nav-toggle target="nav_collapse"></b-nav-toggle>

    <b-navbar-brand href="#">courseroad</b-navbar-brand>
    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-nav is-nav-bar class="ml-auto">

        <b-nav-form class="padded-form">
          <b-form-input v-model="subject" size="sm" class="mr-sm-2" type="text" placeholder="18.01"/>
          <b-button size="sm" class="my-2 my-sm-0" type="text" v-on:click="addSubject">Add</b-button>
        </b-nav-form>

        <b-nav-item-dropdown :text=dropdownText right class="mr-sm-2 dropdown">
          <b-dropdown-header id="header0">Buckets</b-dropdown-header>
          <b-dropdown-item v-for="bucket in buckets" v-on:click=updateBucket(bucket) href="#" :key="bucket.id">{{ bucket.name }}</b-dropdown-item>
          <b-dropdown-header id="header1">Semesters</b-dropdown-header>
          <b-dropdown-item v-for="semester in semesters" v-on:click=updateSemester(semester) href="#" :key="semester.id">{{ semester.name }}</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item href="#">Login</b-nav-item>

      </b-nav>

    </b-collapse>
  </b-navbar>
</template>

<script>
  export default {
    name: 'nav-bar',

    data () {
      return {
        selectedBucketID: -1,
        selectedSemesterID: 0,
        subject: ''
      }
    },

    props: ['semesters', 'buckets'],

    methods: {
      updateSemester (semester) {
        this.selectedSemesterID = semester.id
        this.selectedBucketID = -1
      },

      updateBucket (bucket) {
        this.selectedSemesterID = -1
        this.selectedBucketID = bucket.id
      },

      addSubject () {
        this.$emit('addSubject', {
          year: this.selectedYear,
          semester: this.selectedSemester,
          number: this.subject.toUpperCase()
        })

        this.subject = ''
      }
    },

    computed: {
      dropdownText: function () {
        var name

        if (this.selectedSemesterID >= 0) { // semester selected
          name = this.semesters[this.selectedSemesterID].name
        } else {
          name = this.buckets[this.selectedBucketID].name
        }

        return 'Add To: ' + name
      },

      selectedYear: function () {
        return parseInt(this.selectedSemesterID / 3)
      },

      selectedSemester: function () {
        return this.selectedSemesterID % 3
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .navbar {
    background-color: #7488d2;
  }

  .my-2 {
     background-color: #5e67b4;
  }

  .dropdown {
    padding-left: 2rem;
    padding-right: 3rem;
  }
</style>
