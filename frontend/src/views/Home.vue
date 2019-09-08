<template>
  <div class="home">
    <div class="content">
      <div class="title">
        <img src="~@/assets/images/glass.png" />
        一张照片看透你
      </div>
      <!-- 上传文件 -->
      <div class="upload">
        <van-uploader
          capture
          :max-count="1"
          :after-read="afterRead"
          @delete="handlerDelete"
          :upload-text="text"
          v-model="fileList"
        />
      </div>
      <!-- 确认 -->
      <div class="sub-btn" @click="getAnswer" v-if="!showAnswer">查看分析结果</div>
      <div class="sub-btn2" @click="reset" v-else>重新开始</div>
      <van-popup v-model="pop">
        <img src="~@/assets/images/maploading.gif" alt />
      </van-popup>

      <transition name="van-slide-up">
        <div class="answer" v-if="showAnswer">
          <div class="answer_content">
            <p>{{response.address}}</p>
            <table v-if="response.ok">
              <tr>
                <td>拍摄时间</td>
                <td>{{response.shut_time}}</td>
              </tr>
              <tr>
                <td>是否今日</td>
                <td>{{response.is_today ? '是': '否'}}</td>
              </tr>
            </table>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      text: '上传图片',
      showAnswer: false,
      imageName: '',
      pop: false,
      response: {
        address: '',
        is_today: '',
        shut_time: ''
      },
      fileList: []
    }
  },
  methods: {
    reset () {
      this.showAnswer = false
      this.fileList = []
      this.deletefile(this.imageName)
    },
    afterRead (file) {
      event.preventDefault()
      let fd = new FormData()
      fd.append('file', file.file)
      let headers = {
        'Content-Type': 'multipart/form-data'
      }
      this.$api.post('/upload', fd, headers).then(res => {
        if (res.data.code === 0) {
          this.imageName = res.data.name
          this.$notify({
            type: 'success',
            message: res.data.msg
          })
        } else {
          this.$notify({
            type: 'warning',
            message: res.data.msg
          })
        }
      }).catch(err => {
        this.$notify({
          type: 'danger',
          message: err
        })
      })
    },
    getAnswer () {
      let headers = {
        'Content-Type': 'multipart/form-data'
      }
      let fd = new FormData()
      if (this.imageName) {
        this.pop = true
        fd.append('filename', this.imageName)
        this.$api.post('/finder', fd, headers).then(res => {
          if (res.data.code === 0) {
            setTimeout(() => {
              this.$notify({
                type: 'success',
                message: '解析成功'
              })
              this.response = res.data.data
              this.pop = false
              this.showAnswer = true
            }, 1000)
          } else {
            this.$notify({
              type: 'warning',
              message: res.data.msg
            })
          }
        }).catch(err => {
          this.$notify({
            type: 'danger',
            message: err
          })
        })
      } else {
        this.$notify({
          type: 'warning',
          message: '请先上传照片'
        })
      }
    },
    deletefile (name) {
      let fd = new FormData()
      fd.append('filename', name)
      let headers = {
        'Content-Type': 'multipart/form-data'
      }
      this.$api.post('/delete', fd, headers).then(res => {
        if (res.data.code === 0) {
          this.$notify({
            type: 'success',
            message: res.data.msg
          })
          this.showAnswer = false
          this.imageName = ''
        } else {
          this.$notify({
            type: 'warning',
            message: res.data.msg
          })
        }
      }).catch(err => {
        this.$notify({
          type: 'danger',
          message: err
        })
      })
    },
    handlerDelete (file) {
      let filename = file.file.name
      this.deletefile(filename)
    }
  }
}
</script>

<style scoped>
.home {
  background-image: url("~@/assets/images/bk.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  min-width: 375px;
  width: 100%;
  overflow: hidden;
  height: 100%;
  position: absolute;
  left: 0px;
  top: 50%;
  transform: translateY(-50%);
}

.content {
  width: 100%;
  height: 100%;
  position: relative;
}

.content .title {
  position: relative;
  width: 100%;
  height: 80px;
  color: #b75b5b;
  line-height: 80px;
  text-align: center;
  font-size: 20px;
}

.content .title img {
  position: absolute;
  width: 34px;
  height: 34px;
  left: 84px;
  top: 24px;
}

.content .upload {
  position: absolute;
  left: 40%;
  top: 18%;
}

.content .sub-btn {
  top: 40%;
  left: 22%;
  position: absolute;
  width: 200px;
  background-color: #e8a270;
  height: 50px;
  line-height: 50px;
  color: #fff;
  border-radius: 50px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.content .sub-btn:active {
  background-color: #f1dac9;
}

.content .sub-btn2 {
  top: 40%;
  left: 22%;
  position: absolute;
  width: 200px;
  background-color: #ea9298;
  height: 50px;
  line-height: 50px;
  color: #fff;
  border-radius: 50px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.content .sub-btn2:active {
  background-color: #ebc6d9;
}

.content .answer {
  position: absolute;
  top: 52%;
  background-image: url("~@/assets/images/bg.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  width: 100%;
  min-height: 300px;
}

.content .answer .answer_content {
  position: absolute;
  max-width: 210px;
  top: 24%;
  left: 28%;
  color: #000000b8;
}

.van-popup.van-popup--center img {
  width: 100%;
}

.van-popup {
  background-color: #fff0;
}
</style>
