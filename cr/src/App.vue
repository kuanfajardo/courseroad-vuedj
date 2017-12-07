<template>
  <div id="app">
    <nav-bar v-on:addSubject="addSubject"
             :buckets="customBuckets"
             :semesters="semesters"
             :courses="courses"
             :selectedCourse="'6-3'"
             :text="navBarText"
    ></nav-bar>
    <b-container class="main h-100" fluid>
      <b-row>
        <b-col cols="9" :class="{ loading: isLoading, updated: !isLoading}">
          <year v-for="year in years"
                :key="year.year_id"
                :id="year.year_id"
                :title="year.title"
                :semesters="year.semesters"
                v-on:toggle="toggle"
                v-on:drp="drp">
          </year>
        </b-col>
        <b-col cols="3">
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
          name: 'Freshman Fall',
          id: 0
        },
        {
          name: 'Freshman IAP',
          id: 1
        },
        {
          name: 'Freshman Spring',
          id: 2
        },
        {
          name: 'Sophomore Fall',
          id: 3
        },
        {
          name: 'Sophomore IAP',
          id: 4
        },
        {
          name: 'Sophomore Spring',
          id: 5
        },
        {
          name: 'Junior Fall',
          id: 6
        },
        {
          name: 'Junior IAP',
          id: 7
        },
        {
          name: 'Junior Spring',
          id: 8
        },
        {
          name: 'Senior Fall',
          id: 9
        },
        {
          name: 'Senior IAP',
          id: 10
        },
        {
          name: 'Senior Spring',
          id: 11
        }
      ],
      selectedSubjects: {},
      selected: {},
      years: [],
      isLoading: false,
      navBarText: '',

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

  components: {
    NavBar,
    Year,
    SideBar
  },

  methods: {
    addSubject (obj) {
      this.isLoading = true

      this.addSubjectAPI(obj, (_, response) => {
        this.refreshData((_, response) => {
          this.isLoading = false
        })
      })

      this.years[obj.year].semesters[obj.semester].subjects.push(obj)
    },

    // Toggle Selection
    toggle (obj) {
      var alreadySelected = this.selectedSubjects.hasOwnProperty(obj.subjectID)

      if (alreadySelected) {
        delete this.selectedSubjects[obj.subjectID]
      } else {
        this.selectedSubjects[obj.subjectID] = obj
      }

      this.updateSelected()
    },

    deleteSelectedSubjects () {
      var len = Object.keys(this.selectedSubjects).length
      var i = 1
      this.isLoading = true

      for (var subjectNumber in this.selectedSubjects) {
        if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
          this.selectedSubjects[subjectNumber].target.classList.toggle('selected')

          if (i === len) { // i.e. this is the last call
            this.deleteSubjectAPI(this.selectedSubjects[subjectNumber], (error, response) => {
              if (error === null) {
                this.selectedSubjects = {}
                this.updateSelected()
              } else {
                // Failure - retoggle classes to 'selected'
                for (var subjectNumber in this.selectedSubjects) {
                  if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
                    this.selectedSubjects[subjectNumber].target.classList.toggle('selected')
                  }
                }
              }

              this.refreshData((_, response) => {
                this.isLoading = false
              })
            })
          } else {
            this.deleteSubjectAPI(this.selectedSubjects[subjectNumber], (_, response) => {})
          }
        }

        i++
      }
    },

    drp (obj) {
      // Dragged into same semester
      if (obj.oldSemester === obj.newSemester && obj.oldYear === obj.newYear) {
        return
      }

      // Dragged over from sidebar
      if (obj.oldSemester === -1 && obj.oldYear === -1) {
        var newObj = {
          year: obj.newYear,
          semester: obj.newSemester,
          subjectID: obj.subjectID
        }

        this.addSubject(newObj)

        return
      }

      // Opaque screen
      this.isLoading = true

      // Temporarily "show" results
      var index = obj.index
      this.years[obj.oldYear].semesters[obj.oldSemester].subjects.splice(index, 1)
      this.years[obj.newYear].semesters[obj.newSemester].subjects.push(obj.obj)

      // Unselected everything

      // Delete from old
      this.deleteSubjectAPI({
        year: obj.oldYear,
        semester: obj.oldSemester,
        subjectID: obj.subjectID
      }, (error, response) => {
        if (error === null) {
          // Add to new
          this.addSubjectAPI({
            year: obj.newYear,
            semester: obj.newSemester,
            subjectID: obj.subjectID
          }, (_, response) => {
            this.refreshData((_, response) => {
              this.isLoading = false

              // Un-select any subjects that were moved
              for (var subjectNumber in this.selectedSubjects) {
                if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
                  if (subjectNumber === obj.subjectID) {
                    this.toggle(this.selectedSubjects[subjectNumber])
                  }
                }
              }
            })
          })
        } else {
          this.refreshData((_, response) => {
            this.isLoading = false
          })
        }
      })
    },

    addSubjectAPI (subject, callback) {
      this.navBarText = ''

      var body = {
        'subjectID': subject.subjectID
      }

      var url = 'years/' + subject.year + '/semesters/' + subject.semester + '/subjects/'

      this.$http.post(url, body)
        .then(response => {
          // SUCCESS
          this.navBarText = ''
          callback(null, response)
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

          callback(errorType, response)
        })
    },

    deleteSubjectAPI (subject, callback) {
      this.navBarText = ''

      var url = 'years/' + subject.year + '/semesters/' + subject.semester + '/subjects/' + subject.subjectID + '/'

      this.$http.delete(url)
        .then(response => {
          // SUCCESS
          callback(null, response)
        }, response => {
          // HANDLE ERROR
          var errorType = response.body.error_type
          this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'
          callback(errorType, response)
        })
    },

    refreshData (callback) {
      var url = 'run/'

      this.$http.get(url)
        .then(response => {
          this.$http.get('')
            .then(response => {
              this.years = response.body.years
              callback(null, response)
            }, response => {
              // HANDLE ERROR
              var errorType = response.body.error_type
              this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'

              callback(errorType, response)
            })
        }, response => {
          // HANDLE ERROR
          var errorType = response.body.error_type
          this.navBarText = 'Oops! Looks like something went wrong \uD83D\uDE4A'

          callback(errorType, response)
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
    this.refreshData((_, response) => {})
    this.updateSelected()
  },

  computed: {
    customBuckets: function () {
      var customBuckets = []

      for (var i = 0; i < this.buckets.length; i++) {
        var bucket = this.buckets[i]

        if (bucket.custom) {
          customBuckets.push(bucket)
        }
      }

      return customBuckets
    }
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

body {
  background-color: #fafafa;
}

::-webkit-scrollbar {
    display: none;
}

</style>
