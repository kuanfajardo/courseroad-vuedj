<template>
  <div id="app">
    <nav-bar v-on:addSubject="addSubject"
             :buckets="buckets"
             :semesters="semesters"
             :courses="courses"
             :selectedCourse="'6-3'"
    ></nav-bar>
    <!--<button type="button" v-on:click="deleteSelectedSubjects">Delete</button>-->
    <b-container class="main h-100" fluid>
      <b-row>
        <b-col cols="9" class="coll-1">
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
        <b-container class="sidebar">
          <b-row>
            <b-col cols="4" class="sidebar1">
<!---->       <info-box></info-box>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="4" class="sidebar2">
<!---->       <subject-box></subject-box>
            </b-col>
          </b-row>
        </b-container>
        <!--<div class="mt-3 classes">-->
          <!--<h3 align="center">Classes</h3>-->
          <!--<p>{{ s }}</p>-->
          <!--<div>-->
<!---->
          <!--</div>-->
        <!--&lt;!&ndash;</div>&ndash;&gt;-->
      </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import NavBar from './components/NavBar'
import Year from './components/Year'
import InfoBox from './components/InfoBox'
import SubjectBox from './components/SubjectBox'

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
      s: 'None Selected',
      selectedSubjects: {},
      years: []
    }
  },

  components: {
    NavBar,
    Year,
    InfoBox,
    SubjectBox
  },

  methods: {
    addSubject (obj) {
      this.addSubjectAPI(obj)
//      this.years[obj.year].semesters[obj.semester].subjects.push(obj)
    },

    toggle (obj) {
      var alreadySelected = this.selectedSubjects.hasOwnProperty(obj.name)

      if (alreadySelected) {
        delete this.selectedSubjects[obj.name]
      } else {
        this.selectedSubjects[obj.name] = obj
      }
    },

    updateText () {
      return 'SDFGH'
//      if (this.selectedSubjectNames.length === 0) {
//        return 'None Selected'
//      } else if (this.selectedSubjectNames.length === 1) {
//        return this.selectedSubjectNames[0]
//      } else {
//        return this.selectedSubjectNames.length + ' subjects selected.'
//      }
    },

    deleteSelectedSubjects () {
      // FIX LATER
      for (var subjectNumber in this.selectedSubjects) {
        if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
          this.deleteSubjectAPI(this.selectedSubjects[subjectNumber])
        }
      }
    },

    drp (obj) {
      // Delete from old
      this.deleteSubjectAPI({
        year: obj.oldYear,
        semester: obj.oldSemester,
        name: obj.obj.number
      })

//      var index = obj.index
//      this.years[obj.oldYear].semesters[obj.oldSemester].subjects.splice(index, 1)

      // Add to new
      this.addSubjectAPI({
        year: obj.newYear,
        semester: obj.newSemester,
        number: obj.obj.number
      })
//      this.years[obj.newYear].semesters[obj.newSemester].subjects.push(obj.obj)
    },

    addSubjectAPI (subject) {
      var headers = {
        'authorization': 'Basic anVhbmZhamFyZG86YWRtaW4xMjM=',
        'accept': 'application/json'
      }

      var body = {
        'title': 'A Testt',
        'number': subject.number
      }

      var url = 'http://127.0.0.1:8000/users/juanfajardo/years/' + subject.year + '/semesters/' + subject.semester + '/subjects/'

      this.$http.post(url, body, {headers: headers})
        .then(response => {
          // SUCCESS
          this.refreshData()
        }, response => {
          // HANDLE ERROR
        })
    },

    deleteSubjectAPI (subject) {
      var headers = {
        'authorization': 'Basic anVhbmZhamFyZG86YWRtaW4xMjM=',
        'accept': 'application/json'
      }

      var url = 'http://127.0.0.1:8000/users/juanfajardo/years/' + subject.year + '/semesters/' + subject.semester + '/subjects/' + subject.name

      this.$http.delete(url, {headers: headers})
        .then(response => {
          // SUCCESS
          this.refreshData()
        }, response => {
          // HANDLE ERROR
          alert(JSON.stringify(response))
        })
    },

    refreshData () {
      var headers = {
        'authorization': 'Basic anVhbmZhamFyZG86YWRtaW4xMjM=',
        'accept': 'application/json'
      }

      this.$http.get('http://127.0.0.1:8000/run/ABC/8/', {headers: headers})
        .then(response => {
          this.$http.get('http://127.0.0.1:8000/users/juanfajardo/', {headers: headers})
            .then(response => {
              this.years = response.body.years
            }, response => {
              // HANDLE ERROR
            })
        }, response => {
          // HANDLE ERROR
        })
    }
  },

  created: function () {
    this.refreshData()
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

.coll-1 {
  height: 100%;
}

.coll-2 {
  height: 100%;
}

.sidebar {
  position: fixed;
  /*top:50%;*/
  /*left:0;*/
  /*bottom: 50%;*/
  /*top: 0;*/
  /*right: 2%;*/
  height: 20rem;
  /*background-color: #0c5460;*/
}

.sidebar1 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  border-bottom-width: thin;
  border-bottom-color: #5e67b4;
  border-bottom-style: solid;

  padding-left: 0;
  margin-top: 0;
  padding-right: 2rem;
  /*background-color: #ffc520;*/
  min-height: 13rem;
}

.sidebar2 {
  border-left-width: thin;
  border-left-color: #5e67b4;
  border-left-style: solid;

  padding-left: 0;
  padding-right: 2rem;
  background-color: rgba(252, 225, 229, 0.12);
  min-height: 34rem;
}

body {
  background-color: #fafafa;
}

</style>
