<template>
  <div id="app">
    <nav-bar v-on:addSubject="addSubject"
             :buckets="buckets"
             :semesters="semesters"
             :courses="courses"
             :selectedCourse="'6-3'"
             :text="navBarText"
    ></nav-bar>
    <b-container class="main h-100" fluid>
      <b-row>
        <b-col cols="9" class="coll-1" :class="{ loading: isLoading, updated: !isLoading}">
          <year v-for="year in years"
                :key="year.year_id"
                :id="year.year_id"
                :title="year.title"
                :semesters="year.semesters"
                v-on:toggle="toggle"
                v-on:drp="drp">
          </year>
        </b-col>
      <b-col cols="3" class="coll-2">
        <side-bar v-on:deleteSubjects="deleteSelectedSubjects" :selected="selected"></side-bar>
      </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import NavBar from './components/NavBar'
import Year from './components/Year'
import SideBar from './components/SideBar'

export default {
  name: 'app',
  data () {
    return {
      courses: [
        '6-3', '9', '5', '16', '2'
      ],
      semesters: [
        {
          type: 's',
          name: 'Freshman Fall',
          id: 0
        },
        {
          type: 's',
          name: 'Freshman IAP',
          id: 1
        },
        {
          type: 's',
          name: 'Freshman Spring',
          id: 2
        },
        {
          type: 's',
          name: 'Sophomore Fall',
          id: 3
        },
        {
          type: 's',
          name: 'Sophomore IAP',
          id: 4
        },
        {
          type: 's',
          name: 'Sophomore Spring',
          id: 5
        },
        {
          type: 's',
          name: 'Junior Fall',
          id: 6
        },
        {
          type: 's',
          name: 'Junior IAP',
          id: 7
        },
        {
          type: 's',
          name: 'Junior Spring',
          id: 8
        },
        {
          type: 's',
          name: 'Senior Fall',
          id: 9
        },
        {
          type: 's',
          name: 'Senior IAP',
          id: 10
        },
        {
          type: 's',
          name: 'Senior Spring',
          id: 11
        }
      ],
      buckets: [
        {
          type: 'b',
          name: 'HASS Ideas',
          id: 0
        },
        {
          type: 'b',
          name: 'Want To Take',
          id: 1
        }
      ],
      selectedSubjects: {},
      selected: {},
      years: [],
      isLoading: false,
      navBarText: ''
    }
  },

  components: {
    NavBar,
    Year,
    SideBar
  },

  methods: {
    addSubject (obj) {
      this.addSubjectAPI(obj, true)
      this.years[obj.year].semesters[obj.semester].subjects.push(obj)
    },

    toggle (obj) {
      var alreadySelected = this.selectedSubjects.hasOwnProperty(obj.name)

      if (alreadySelected) {
        delete this.selectedSubjects[obj.name]
      } else {
        this.selectedSubjects[obj.name] = obj
      }

      this.updateSelected()
    },

    deleteSelectedSubjects () {
      // TODO: FIX LATER
      for (var subjectNumber in this.selectedSubjects) {
        if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
          this.deleteSubjectAPI(this.selectedSubjects[subjectNumber], true)
        }
      }

      // TODO: Add to closure call of deleteSubject call
      this.selectedSubjects = {}
      this.updateSelected()
    },

    drp (obj) {
      if (obj.oldSemester === obj.newSemester && obj.oldYear === obj.newYear) {
        return
      }

      // Opaque screen
      this.isLoading = true

      // Temporarily "show" results
      var index = obj.index
      this.years[obj.oldYear].semesters[obj.oldSemester].subjects.splice(index, 1)
      this.years[obj.newYear].semesters[obj.newSemester].subjects.push(obj.obj)

      // TODO: Make addSubjectAPI call only happen if delete successful
      // Delete from old
      this.deleteSubjectAPI({
        year: obj.oldYear,
        semester: obj.oldSemester,
        name: obj.obj.subject.subjectId
      }, false)

      // Add to new
      this.addSubjectAPI({
        year: obj.newYear,
        semester: obj.newSemester,
        number: obj.obj.subject.subjectId
      }, true)
    },

    // TODO: add closure parameter
    addSubjectAPI (subject, clearLoading) {
      this.navBarText = ''

      var body = {
        'number': subject.number
      }

      var url = 'years/' + subject.year + '/semesters/' + subject.semester + '/subjects/'
      this.isLoading = true

      this.$http.post(url, body)
        .then(response => {
          // SUCCESS
          this.refreshData(clearLoading)
          this.navBarText = ''
        }, response => {
          // HANDLE ERROR
          this.isLoading = false
          var errorType = response.body.error_type

          switch (errorType) {
            case 0:
              this.navBarText = 'Subject does not exist. \uD83D\uDE15'
              break
            default:
              this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'
          }

          this.refreshData()
        })
    },

    // TODO: add closure parameter
    deleteSubjectAPI (subject, clearLoading) {
      this.navBarText = ''

      var url = 'years/' + subject.year + '/semesters/' + subject.semester + '/subjects/' + subject.name
      this.isLoading = true

      this.$http.delete(url)
        .then(response => {
          // SUCCESS
          this.refreshData(clearLoading)
        }, response => {
          // HANDLE ERROR
          this.refreshData()
          this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'
          this.isLoading = false
        })
    },

    // TODO: add closure parameter
    refreshData (clearLoading) {
      var url = 'run/ABC/8/'

      this.$http.get(url)
        .then(response => {
          this.$http.get('')
            .then(response => {
              this.years = response.body.years
              if (clearLoading) {
                this.isLoading = false
              }
            }, response => {
              // HANDLE ERROR
              this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'
              this.isLoading = false
            })
        }, response => {
          // HANDLE ERROR
          this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'
          this.isLoading = false
        })
    },

    updateSelected () {
      switch (Object.keys(this.selectedSubjects).length) {
        case 0:
          this.selected = {
            number: 'info',
            title: 'No Subjects Selected',
            units: '',
            description: '',
            hideLinks: true,
            hideDelete: true
          }
          break

        case 1:
          var key = Object.keys(this.selectedSubjects)[0]
          var subject = this.selectedSubjects[key]

          this.selected = {
            number: subject.obj.subject.subjectId,
            title: subject.obj.subject.title,
            units: subject.obj.subject.units,
            description: subject.obj.subject.description,
            hideLinks: false,
            hideDelete: false
          }
          break

        default:
          this.selected = {
            number: 'info',
            title: Object.keys(this.selectedSubjects).length + ' Subjects Selected',
            units: ' Tread carefully',
            description: '',
            hideLinks: true,
            hideDelete: false
          }
          break
      }
    }
  },

  created: function () {
    this.refreshData(true)
    this.updateSelected()
  }
}
</script>

<style>

@font-face {
  font-family: "KG Second Chances Sketch";,
  src: "./assets/KGSecondChancesSketch.ttf";
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  /*font-family: "KG Second Chances Sketch", sans-serif;*/
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  margin-bottom: 4rem;

}

.updated {
  opacity: 1;
}

.loading {
  opacity: 0.5;
}

.coll-1 {
  height: 100%;
}

.coll-2 {
  height: 100%;
}

body {
  background-color: #fafafa;
}

</style>
