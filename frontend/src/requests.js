import axios from 'axios'

let BASEURL = 'http://127.0.0.1:5000'
if (process && process.env && process.env.NODE_ENV === 'production') {
  BASEURL = 'http://zhongdian.hanson365.com'
}

const service = axios.create({
  baseURL: '/api', // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

export default service
