<template>
  <div id="app" v-bind:style="{ backgroundColor: color}">
    <loading :active.sync="isLoading" 
        :can-cancel="false" 
        :on-cancel="onCancel"
        :is-full-page="fullPage"></loading>

  <v-container style="padding:1rem 13.8rem 0 13.8rem;" fluid class="catalogue-tab-container" v-bind:class="{'top': toggleShowResults, 'middle': !toggleShowResults}">
    <div class="justify"><span style="color: #061926;font-size: 36px;">Search DT Support Issues</span></div>    
    <div class="description">
      <v-layout row wrap class="justify" >
        <v-flex lg9 md7>
          <v-text-field clearable flat 
           style="box-sizing: border-box; height: 36px; border: 1px solid #B8CBD9; border-radius: 3px;"
           v-model="searchText" class="" solo placeholder="Hello, how may i help you?"
           prepend-inner-icon="mdi-magnify" @keyup.enter="showResult()"></v-text-field>
        </v-flex>
        <v-flex lg3 md5> 
          <v-btn class="primary" @click="showResult()" style="margin-left:0.5rem;">Search</v-btn>
          <v-btn class="secondary" @click="toggleAddResults=true" style="margin-left:0.5rem;">Add Issue</v-btn>
        </v-flex>
      </v-layout>
    </div>
    <div v-show="toggleAddResults" style="padding:0 0 0 1rem;">
      <v-layout row wrap class="justify">
        <v-flex lg10 md8 style="display: flex;">  
          <v-textarea flat no-resize solo placeholder="Add issue here" rows="2" cols="100" v-model="issueText"></v-textarea>   
        </v-flex>
        <v-flex lg2 md2 style="display: flex;">  
        </v-flex>
      </v-layout>
      <v-layout row wrap style="align-items:flex-end;" class="justify"  >
        <v-flex lg10 md8 style="">  
          <v-textarea flat no-resize  solo placeholder="Add closure note here" rows="4" cols="100" v-model="closureNote"></v-textarea>   
        </v-flex>
        <v-flex lg1 md2 style="">  
          <v-btn class="primary" size="lg" @click="addTicket()">Save</v-btn>
        </v-flex>
        <v-flex lg1 md2 style="">  
          <v-btn class="secondary"   size="lg" @click="toggleAddResults=false">Cancel</v-btn>
        </v-flex>
      </v-layout>
    </div>
    <div variant="success" v-show="toggleShowResults">
      <v-layout row  class="justify">
        <v-flex v-for="(item,i) in items" :key="i" style="padding:0 0 1rem 0;">
          <v-layout row wrap>
            <v-layout>
              <v-flex lg2 md2 class="headingBold">
                <label >Issue Type</label>
              </v-flex>  
              <v-flex lg7 md7 class="description" style="text-transform:capitalize;"> 
                {{item.category.join()}} type
              </v-flex>
              <v-flex lg3 md3 class="">
                <v-icon class="icons float-left mr-4"   @click="freez(item)">mdi-thumb-up-outline </v-icon>
                <v-icon class="icons float-left mr-4"   @click="item.editEnabled=true">mdi-pencil-outline</v-icon>
                <v-icon class="icons float-left"   @click="removeTicket(item)">mdi-trash-can-outline </v-icon>
                <v-btn class="secondary float-right" style="margin-right:1.2rem;"  @click="item.detailsShowing = !item.detailsShowing">{{ item.detailsShowing ? 'Hide' : 'Show' }} Details</v-btn>
              </v-flex>
            </v-layout>
            <v-layout style="width:100%;"> 
              <v-flex lg2 md2 class="headingBold" v-show="!item.editEnabled"> 
                <label >Solution</label>
              </v-flex>
              <v-flex lg8 md8 class="description" v-show="!item.editEnabled"> 
                <span >{{item.closure_note.trim()}}</span>
              </v-flex>
              <v-flex lg2 md2></v-flex>
            </v-layout>  
              <v-layout style="margin-bottom:1rem;padding:0 0 0 2rem;align-items:flex-end;width:100%;">
                <v-flex lg6 md6>
                  <textarea class="form-control form-control-sm" style="resize: none; " placeholder="Edit Closure notes" rows="3" v-show="item.editEnabled" v-model="item.closure_note_modified"></textarea>   
                </v-flex>
                <v-flex lg3 md3>
                  <v-btn class="secondary"   v-show="item.editEnabled" @click="editClosure(item)">
                    Submit
                  </v-btn>
                  <v-btn class="secondary" style="margin-left: 1rem; " v-show="item.editEnabled" @click="item.editEnabled=false">
                    Cancel
                  </v-btn>
                </v-flex>  
              </v-layout>
              <v-layout row v-show="item.detailsShowing" style="padding:0 0 0 .8rem;">
                <v-layout style="width:100%">
                  <v-flex lg2 md2 class="headingBold">
                    App
                  </v-flex>
                  <v-flex lg8 md8 class="description"> 
                    <span style="text-transform:capitalize;">{{item.app.join()}}</span>
                  </v-flex>
                  <v-flex lg2 md2></v-flex>
                </v-layout>
                <v-layout style="width:100%">
                  <v-flex lg2 md2 class="headingBold">  
                    Category
                  </v-flex>
                  <v-flex lg8 md8 class="description"> 
                    <span style="text-transform:capitalize;">{{item.category.join()}}</span>
                  </v-flex>
                  <v-flex lg2 md2></v-flex>
                </v-layout>
                <v-flex lg2 md2 class="headingBold"> 
                  <label >Description</label>
                </v-flex>
                <v-flex lg8 md8 class="description"> 
                  <span v-show="!item.editEnabled">{{item.desc.trim()}}</span>
                </v-flex>
                <v-flex lg2 md2></v-flex>
                <v-flex v-show="Object.keys(item.notes).length > 0" lg2 md2 class="headingBold"> Notes </v-flex>
                <ul lg8 md8>
                  <v-flex v-for="(note_item, i) in item.notes.NOTE_TEXT" :key="i"  class="description"> 
                      <li >  
                        {{note_item}}
                      </li>
                  </v-flex>
                </ul>  
                <v-flex lg2 md2></v-flex>
              <v-layout  style="align-items:flex-end;width:100%" >
                <v-flex lg2 md2>
                </v-flex>
                <v-flex lg8 md8>
                  <v-textarea flat solo no-resize placeholder="Add Notes" rows="2" cols="100"   v-model="item.comment"></v-textarea> 
                </v-flex>
                <v-flex lg2 md2>  
                  <v-btn class="secondary" @click="addComment(item)"  >
                    Save Notes
                  </v-btn>
                </v-flex>
              </v-layout>
              <v-layout style="width:100%;align-items:flex-end;">
                <v-flex lg2 md2>
                </v-flex>            
                <v-flex lg8 md8>
                  <v-file-input 
                    prepend-icon=""
                    show-size
                    class="fileInput"
                    placeholder="Select attachment"
                    outlined
                    prepend-inner-icon="$file"
                    v-model="item.file2"
                    style="margin-top: 1rem;  margin-bottom:1rem;font-family:font-family:'GE Inspira Sans';font-size: 16px;background: #ffffff;">
                  </v-file-input>
                <v-flex lg1 md1>  
                  <v-btn @click="addFile(item, item.file2)" class="primary"  >Upload</v-btn>
                </v-flex>
                <v-flex lg3>
                    <p class="description"  style="margin-top:.4rem;">Selected file: <b>{{item.file2 ? item.file2.name : '' }}</b></p>
                </v-flex>  
                  <ul v-show="Object.keys(item.attachments).length > 0" class="description">
                    <h3>Attachments</h3>
                    <li v-for="(atc_item, i) in item.attachments.ATC_NAME" :key="i" style="margin-left: 2rem;">
                      {{atc_item}} 
                      <a style="cursor:pointer;" @click="downloadFile(item.attachments.UUID[i])" download>
                        <v-icon class="icons"  >mdi-download</v-icon>
                      </a>
                    </li>
                  </ul>
                </v-flex> 
                </v-layout>
              </v-layout>
            </v-layout>    
          <div class="line"></div>
        </v-flex>
      </v-layout>
    </div>   
  </v-container>
  <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="6000" :top="true" :right="true">
    {{ snackbarText }}
    <v-btn dark text @click="snackbar = false">Close</v-btn>
  </v-snackbar>     
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'
import FileSaver from 'file-saver'
export default {
  name: 'app',
  components: {
  },
  data () {
    return {
      isLoading: false,
      fullPage: true,
      flag: false,
      selected: '',
      searchText: '',
      color: '#f5f5f5',
      toggleShowResults: false,
      hoverIcon: true,
      items: [],
      issueText: '',
      closureNote: '',
      toggleAddResults: false,
      snackbar: false,
      snackbarText: '',
      snackbarColor: '#80D8FF'
    }
  },
  methods: {
    freez (data) {
      this.isLoading = true
      var self = this
      this.isLoading = true
      this.upVoteSuggestion(data, this.searchText).then(function () {
        self.flag = true
        self.isLoading = false
      }, function () {
        self.isLoading = false
      })
    },
    upVoteSuggestion (data, searchText) {
      return new Promise((resolve, reject) => {
        axios.post('/upsuggestions', {desc: searchText, close_note: data.closure_note})
      .then((response) => {
        this.snackbarText = 'Successfully upvoted!!!'
        this.snackbarColor = 'primary'
        this.snackbar = true
        resolve(response)
      }, (err) => {
        this.snackbarText = 'Upvoting failed!!!'
        this.snackbarColor = '#E53935'
        this.snackbar = true
        resolve(reject)
        return err
      })
      })
    },
    addTicket () {
      if (this.issueText.length > 0) {
        if (this.closureNote.length > 0) {
          this.isLoading = true
          var self = this
          this.addTicketPost(this.issueText, this.closureNote).then(function () {
            self.isLoading = false
            self.issueText = ''
            self.closureNote = ''
            self.toggleAddResults = false
            this.snackbarText = 'Successfully added!!!'
            this.snackbarColor = 'primary'
            this.snackbar = true
          }, function () {
            self.isLoading = false
            this.snackbarText = 'Adding failed!!!'
            this.snackbarColor = '#E53935'
            this.snackbar = true
          })
        } else {
          this.snackbarText = 'Closure note empty.'
          this.snackbarColor = '#E53935'
          this.snackbar = true
        }
      } else {
        this.snackbarText = 'Issue text empty.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      }
    },
    addTicketPost (issueText, closureNote) {
      return new Promise((resolve, reject) => {
        axios.post('/upsuggestions/addticket', {issue: issueText, closureNote: closureNote})
      .then((response) => {
        resolve(response)
      }, error => {
        reject(error)
      })
      })
    },
    addComment (data) {
      if (data.comment.length > 0) {
        this.isLoading = true
        var self = this
        this.addCommentPost(data, this.searchText).then(response => {
          self.isLoading = false
          data.notes.NOTE_ID.push(response)
          data.notes.NOTE_TEXT.push(data.comment)
          data.notes.DOC_ID.push(data.id)
          data.comment = ''
        }, function () {
          self.isLoading = false
        })
      } else {
        this.snackbarText = 'Empty note, fill in info.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      }
    },
    addCommentPost (data, searchText) {
      return new Promise((resolve, reject) => {
        axios.post('/upsuggestions/addnote', {desc: searchText, id: data.id, note: data.comment})
      .then((response) => {
        this.snackbarText = 'Note saved successfully.'
        this.snackbarColor = 'primary'
        this.snackbar = true
        resolve(response)
      }, error => {
        reject(error)
        this.snackbarText = 'Some error occured, try again.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      })
      })
    },
    addFile (data, file) {
      if (file.name) {
        this.isLoading = true
        var self = this
        this.addCmsUploadData(data, file).then(cmsresponse => {
          this.addFmsUploadData(data, file, cmsresponse.data).then(function () {
            self.addFilePost(data, file, cmsresponse.data).then(fileResponse => {
              data.attachments.ATC_ID.push(fileResponse)
              data.attachments.ATC_NAME.push(file.fileName)
              data.attachments.DOC_ID.push(data.id)
              data.attachments.UUID.push(cmsresponse.data.uuid)
              self.isLoading = false
            }, function () {
              self.isLoading = false
            })
          },
          function () {
            self.isLoading = false
          })
        },
        function () {
          self.isLoading = false
        })
      } else {
        this.snackbarText = 'No attachment selected'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      }
    },
    addFilePost (data, file, cmsData) {
      var fileData = {}
      fileData.fileName = file.name
      fileData.uuid = cmsData.uuid
      fileData.id = data.id
      return new Promise((resolve, reject) => {
        axios.post('/upsuggestions/addfile', fileData)
        .then((response) => {
          resolve(response)
          this.snackbarText = 'Attachment saved successfully.'
          this.snackbarColor = 'primary'
          this.snackbar = true
          this.showResult()
        }, error => {
          reject(error)
          this.snackbarText = 'Some error occured, try again.'
          this.snackbarColor = '#E53935'
          this.snackbar = true
        })
      })
    },
    addCmsUploadData (data, file) {
      var cmsUploadData = {}
      cmsUploadData.appid = 'DTSupport'
      cmsUploadData.apptype = 'SupportingDocuments'
      cmsUploadData.objectid = 'US'
      cmsUploadData.filename = file.name
      return new Promise((resolve, reject) => {
        axios.post('/api/data/cms/v2/documents', cmsUploadData)
        .then((response) => {
          resolve(response)
        }, error => {
          reject(error)
          this.snackbarText = 'Some error with file upload occured, try again.'
          this.snackbarColor = '#E53935'
          this.snackbar = true
        })
      })
    },
    addFmsUploadData (data, file, cmsresponse) {
      var formData = new FormData()
      formData.append('file', file)
      formData.append('flowChunkSize', file.size)
      formData.append('flowChunkNumber', 1)
      formData.append('flowCurrentChunkSize', file.size)
      formData.append('flowTotalSize', file.size * 64)
      formData.append('flowIdentifier', file.name.split('.')[0])
      formData.append('flowRelativePath', file.name)
      formData.append('flowFilename', file.name)
      formData.append('flowTotalChunks', 1)
      var fmsUploadHeader = {
        'Content-Type': 'multipart/form-data; boundary=' + formData._boundary
      }
      fmsUploadHeader.token = cmsresponse.token
      return new Promise((resolve, reject) => {
        axios.post('/dt-api/v1/cmsfiles?token=' + cmsresponse.token, formData, {headers: fmsUploadHeader})
        .then((response) => {
          resolve(response)
        }, error => {
          reject(error)
          this.snackbarText = 'Some error with file upload occured, try again.'
          this.snackbarColor = '#E53935'
          this.snackbar = true
        })
      })
    },
    downloadFile (uuid) {
      this.isLoading = true
      var self = this
      this.cmsDownload(uuid).then(response => {
        this.fmsDownload(response.data.token).then(function () {
          self.isLoading = false
          self.snackbarText = 'Attachment downloaded successfully.'
          self.snackbarColor = 'primary'
          self.snackbar = true
        }, function () {
          self.isLoading = false
          self.snackbarText = 'Some error with file download occured, try again.'
          self.snackbarColor = '#E53935'
          self.snackbar = true
        })
      }, function () {
        self.isLoading = false
        self.snackbarText = 'Some error with file download occured, try again.'
        self.snackbarColor = '#E53935'
        self.snackbar = true
      })
    },
    cmsDownload (uuid) {
      return new Promise((resolve, reject) => {
        axios.get(`/api/data/cms/v2/documents/${uuid}/file?rev=0`)
        .then((response) => {
          resolve(response)
        }, (err) => {
          reject(err)
        })
      })
    },
    fmsDownload (token) {
      return new Promise((resolve, reject) => {
        axios.get(`/dt-api/v1/cmsfiles?token=${token}`, {responseType: 'blob'})
        .then(response => {
          let blob = new Blob([response.data], {type: response.headers['content-type']})
          let fileName = _.split(response.headers['content-disposition'], '"')
          FileSaver.saveAs(blob, fileName[1])
          resolve('Attachment(s) downloaded successfully!')
        }, error => {
          reject(error.message)
        })
      })
    },
    removeTicket (data) {
      var result = confirm('Want to delete this Ticket?')
      if (result) {
        this.isLoading = true
        return new Promise((resolve, reject) => {
          axios.post('/upsuggestions/removeticket', {id: data.id})
      .then((response) => {
        resolve(response)
        this.snackbarText = 'Ticket removed successfully.'
        this.snackbarColor = 'primary'
        this.snackbar = true
        this.showResult()
      }, error => {
        reject(error)
        this.isLoading = false
        this.snackbarText = 'Some error occured, try again.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      })
        })
      }
    },
    editClosure (data) {
      if (data.closure_note_modified.length > 0) {
        if (this.searchText.length > 0) {
          this.isLoading = true
          var self = this
          this.editClosurePost(data, this.searchText).then(function () {
            self.isLoading = false
          }, function () {
            self.isLoading = false
          })
        } else {
          this.snackbarText = 'Text to be searched not provided.'
          this.snackbarColor = '#E53935'
          this.snackbar = true
        }
      } else {
        this.snackbarText = 'Closure note is empty.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      }
    },
    editClosurePost (data, searchText) {
      return new Promise((resolve, reject) => {
        axios.post('/upsuggestions/updateclousurenote', {desc: searchText, id: data.id, close_note: data.closure_note_modified})
      .then((response) => {
        resolve(response)
        this.showResult()
        this.snackbarText = 'Editing successful.'
        this.snackbarColor = 'primary'
        this.snackbar = true
      }, error => {
        reject(error)
        this.snackbarText = 'Some error occured, try again.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
      })
      })
    },
    fetchSuggestions () {
      return new Promise((resolve, reject) => {
        axios.post('/suggestions/get', {'desc': this.searchText}).then((response) => {
          resolve(response)
        }, (err) => {
          resolve(reject)
          return err
        })
      })
    },
    showResult () {
      if (this.searchText.length < 1) {
        this.snackbarText = 'Please enter some text.'
        this.snackbarColor = '#E53935'
        this.snackbar = true
        return
      }
      this.isLoading = true
      this.flag = false
      this.item = []
      this.selected = ''
      var self = this
      this.fetchSuggestions().then(function (response) {
        // Uncomment when deploying in dev
        // const result = response.data
        const result = response
        result.data.data.forEach(element => {
          element.closure_note = element.closure_note.split('↵').join('\n')
          element.comment = ''
          element.closure_note_modified = element.closure_note
          element.editEnabled = false
          element.file2 = {}
          element.detailsShowing = false
        })
        self.items = result.data.data
        self.toggleShowResults = true
        self.isLoading = false
      }, function () {
        self.toggleShowResults = false
        self.isLoading = false
      })
    },
    mouseOver (items) {
      if (!this.selected.color && this.selected.color !== 'danger') {
        this.selected = items
      }
      // this.hoverIcon = !this.hoverIcon
    },
    mouseOut () {
      if (!this.selected.color && this.selected.color !== 'danger') {
        this.selected = ''
      }
      // this.hoverIcon = !this.hoverIcon
    },
    onCancel () {
      this.isLoading = false
    }
  }
}
</script>

<style>
#app {
  font-family: 'GE Inspira Sans' !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100vh;
}
.line{
  box-sizing: border-box;
  height: 1px;
  width: 1071px;
  border: 1px solid #CFDCE6;
}

.headingBold {
  padding-left: 2rem;
  color: #3F5D73;
  font-family: "GE Inspira Sans";
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 0;
  line-height: 24px;
  text-align: initial;
  margin-bottom: 1rem;
}

.description {
  text-align: initial;
  color: #061926;
  font-family: "GE Inspira Sans";
  font-size: 16px;
  letter-spacing: 0;
  line-height: 24px;
  margin-bottom: 1rem;
}

.v-input__control{
  min-height: 34px !important;
}
.v-input__slot {
  margin-bottom: 0 !important;
}
.v-btn {
  box-shadow: none !important;
}

.hidden_header {
  display: none;
}
@keyframes rotationUp {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(180deg);
  }
}
@keyframes rotationDown {
  from {
    transform: rotate(180deg);
  }
  to {
    transform: rotate(0deg);
  }
}
.up-rotate {
  animation: rotationUp .2s linear;
  animation-fill-mode: forwards;
}
.down-rotate {
  animation: rotationDown .2s linear;
  animation-fill-mode: forwards;
}
.icons {
  background: transparent !important;
  font-size: 1.2rem !important;
  border: none !important;
  color: #0077cc !important;
   
}
.icon-arrange {
  margin-bottom: -1rem;
  margin-top: 1rem;
}
td {
  text-align: left !important;
  font-size: 1.3rem;
  color: #636567;
}

.sol-text{
  white-space: pre-wrap;
}

.result_body > tr > td:first-child{
  white-space: pre-wrap;
  width: 95%;
}

.primary {
  border-radius: 3px;
  background-color: #0077CC !important;
  color: #FFFFFF !important;
  font-family: "GE Inspira Sans";
  font-size: 16px;
  letter-spacing: 0;
  line-height: 24px;
  text-align: center;
  text-transform: none !important;
  cursor: pointer;
}

.secondary {
  color: #0072C3 !important;
  font-family: "GE Inspira Sans";
  font-size: 14px;
  letter-spacing: 0;
  line-height: 24px;
  text-align: center;
  box-sizing: border-box;
  border: 1px solid #B8CBD9 !important;
  border-radius: 3px;
  text-transform: none !important;
  cursor: pointer;
}

.v-text-field__details {
  display: none !important;
}

.shadow{
  box-shadow: .5rem .5rem;
}
.top {
  top : 0rem !important;
}
.middle {
  top : 30% !important;
  position: absolute;
}
.justify {
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 2rem;
  transition: .5s;
}
.aux-btn-white {
    background-color: #f5f5f5 !important;
    border: 1px solid #b8cbd9;
    border-radius: 10px;
    color: #07c !important;
    display: inline-block;
    font-size: 1.2rem;
    padding: .5rem;
    text-transform: none;
    text-align: center;
    transition: all .3s ease-in-out;
}
.table td, .table th {
    padding: 1.75rem;
}  
.fade-enter-active, .fade-leave-active {
  transition: opacity 2s;
}
.fade-enter, .fade-leave-active /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.trans {
  transition: .5s;
}
.fileInput fieldset {
  border: 0px !important;
}
.v-btn__content {
  cursor: pointer;
}
</style>
