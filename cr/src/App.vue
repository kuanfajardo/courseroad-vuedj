<template>
  <div id="app">
    <nav-bar v-on:addSubject="addSubject" :buckets="buckets" :semesters="semesters"></nav-bar>
    <b-container class="main h-100" fluid>
      <b-row>
      <b-col cols="9" class="coll-1">
        <!--<year v-for="year in years"-->
              <!--:key="year.id"-->
              <!--:year="year.name"-->
              <!--:yearID="year.id"-->
              <!--:subjects="year.subjects"-->
              <!--v-on:toggle="toggle"-->
              <!--v-on:drp="drp"-->
        <!--&gt;-->
        <!--</year>-->
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
        <div class="mt-3 classes">
          <h3 align="center">Classes</h3>
          <p>{{ s }}</p>
          <div>
            <button type="button" v-on:click="deleteSelectedSubjects">Delete</button>
          </div>
        </div>
      </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import NavBar from './components/NavBar'
import Year from './components/Year'

export default {
  name: 'app',
  data () {
    return {
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
      semesterInFocus: 0,
      s: 'None Selected',
      selectedSubjects: {},
//      selectedSubjectNames: [],

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

      years: [

      ]

//          subjects: [
//            ['24.02', '18.02A', '8.01'],
//            ['3.091'],
//            ['12.020']
//          ]
//        },
//        {
//          id: 1,
//          name: 'Sophomore',
//          subjects: [
//            [],
//            [],
//            []
//          ]
//        },
//        {
//          id: 2,
//          name: 'Junior',
//          subjects: [
//            [],
//            [],
//            []
//          ]
//        },
//        {
//          id: 3,
//          name: 'Senior',
//          subjects: [
//            [],
//            [],
//            []
//          ]
//        }
    }
  },

  components: {
    NavBar,
    Year
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

//      if (this.selectedSubjectNames.includes(subject.name)) {
//        this.selectedSubjects.splice(this.selectedSubjectNames.indexOf(subject.name), 1)
//        this.selectedSubjectNames.splice(this.selectedSubjectNames.indexOf(subject.name), 1)
//      } else {
//        this.selectedSubjects.push(subject)
//        this.selectedSubjectNames.push(subject.name)
//      }

      this.s = this.updateText()
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
      for (var subjectNumber in this.selectedSubjects) {
        if (this.selectedSubjects.hasOwnProperty(subjectNumber)) {
          alert(subjectNumber)
          var subject = this.selectedSubjects[subjectNumber]
          var index = subject.index

          alert(JSON.stringify(this.selectedSubjects[subjectNumber]))
          this.years[subject.year].semesters[subject.semester].subjects.splice(index, 1)
          delete this.selectedSubject[subjectNumber]
//          subject.target.classList.remove('selected')
        }
      }
//      this.selectedSubjects = {}
      alert(JSON.stringify(this.selectedSubjects))
      this.s = this.updateText()
    },

    drp (obj) {
      // Delete from old
      var index = obj.index // this.years[obj.oldYear].semesters[obj.oldSemester].indexOf(obj.subject)
      this.years[obj.oldYear].semesters[obj.oldSemester].subjects.splice(index, 1)

      // Add to new
      this.years[obj.newYear].semesters[obj.newSemester].subjects.push(obj.obj)
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
//          alert(JSON.stringify(response))
        }, response => {
//          alert(JSON.stringify(response))
        })

      this.refreshData()
    },

    refreshData () {
      var headers = {
        'authorization': 'Basic dXNlcjphZG1pbjEyMw==',
        'accept': 'application/json'
      }
//      alert('refreshing')
      this.$http.get('http://127.0.0.1:8000/users/juanfajardo/', {headers: headers})
        .then(response => {
//          alert(JSON.stringify(response.body.years))
          this.years = response.body.years
        }, response => {
//          alert(response.status)
        })
    }
  },

  created: function () {
//    var headers = {
//      'authorization': 'Basic dXNlcjphZG1pbjEyMw==',
//      'accept': 'application/json'
//    }
//    alert('creating')
//    this.$http.get('http://127.0.0.1:8000/users/juanfajardo/', {headers: headers})
//      .then(response => {
//        alert(JSON.stringify(response.body.years))
//        this.years = response.body.years
//      }, response => {
//        alert(response.status)
//      })
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
