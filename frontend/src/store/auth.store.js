import { defineStore } from 'pinia';
import axios from "axios"
import Cookies from 'js-cookie';

const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

export const useAuthStore = defineStore('authoptions', {
  state : ()=>({
    isLoading:false, 
    isReady:false, 
    data:null, 
    on_error:null,
  }),
  getters: {
    loading : (state) => state.isLoading,
    ready : (state) => state.isReady,
    user : (state) => state.data,
    error :(state) => state.on_error,
   
  },
  actions : {
    async login(payload){
      this.isLoading = true
      this.on_error = false;
      this.isReady = false
  
      const params = new URLSearchParams();
      params.append('username', payload.username)
      params.append('password', payload.password)
  
      try {
          await axios.post(`${baseUrl}/login/access-token`, params, {withCredentials: true, credentials:'include'})
          .then(response => {
            this.isReady  = true
            this.data = response.data.user
            Cookies.set('is_Authenticated', true, {expires: 8})
          }).catch(err => {
            console.log(err)
            this.isReady = false
            this.on_error = err.response ? err.response.data.detail : 'Network error';
          }).finally(resp => {
            this.isLoading = false
         })
        } catch (e){
          this.isReady = false
          this.isLoading = false
          this.on_error = e 
        }
    },

    async register(payload){
      this.isLoading = true
      this.on_error = false
      this.isReady = false

      try {
        await axios.post(`${baseUrl}/sign-up`, payload, {withCredentials: true, credentials:'include'})
        .then(response => {
          this.isReady  = true
          this.data = response.data
          // Cookies.set('is_Authenticated', true, {expires: 8})
        }).catch(err => {
          console.log(err.response.data.detail)
          this.isReady = false
          this.on_error = err.response ? err.response.data.detail :err.response;
        }).finally(resp => {
          this.isLoading = false
       })

      } catch (e){
        this.isReady = false
        this.isLoading = false
        this.on_error = e 
      }
    },

    async getUserProfile(){
      console.log("Something will")
      await axios.get(`${baseUrl}/profile`,  {withCredentials: true, credentials:'include'})
      .then(response => {
        this.data = response.data
      })
    },

    async logout(){
      this.isReady= false
      this.isLoading = true
      this.on_error = true
  
      try{
        await axios.get(`${baseUrl}/logout`)
      .then(response => {
        Cookies.remove('is_Authenticated')
        this.data = '' //storage is persisted in session. Alternatively clear session
        this.isLoading = false
        this.isReady = true
      }).catch((err)=>{
        this.on_error = err
      })
      } catch (e) {
      this.isLoading = false
      }
    },


    async editUser(payload){
      try{
        await axios.put(`${baseUrl}/profile`, payload, {withCredentials: true, credentials:'include'})
        .then(response=>{
          this.isReady = true
          this.data = response.data
        }).catch(err=>{
          console.log(err)
          this.isReady = false
          this.on_error = err.response? err.response.data.detail : 'An error occured, please try again'
        }).finally(resp=>{
          this.isLoading = false
        })
      } catch (e){
        this.isReady = false
        this.isLoading = false
        this.on_error = 'An error occurred, please try again' 
      }
    },

    async updateProfilePicture(payload){
      this.isLoading = true
      this.on_error = false
      this.isReady = false
      try{
        await axios.post(`${baseUrl}/profile`, payload, 
        { 
          headers: {
          'Content-Type': 'multipart/form-data', // Ensure the correct content type for file uploads
          },
          withCredentials: true, credentials:'include'})
        .then(response=>{
          this.isReady=true
          this.data = response.data
        }).catch(err=>{
          console.log(err)
          this.isReady = false
          this.on_error = err.response? err.response.data.detail : 'An error occured, please try again'
        }).finally(resp=>{
          this.isLoading = false
        })
      } catch (e){
        this.isReady = false
        this.isLoading = false
        this.on_error = 'An error occurred, please try again' 
      }
    }
  
  },

  persist: {
    storage: sessionStorage,
  }
})






// export const useAuthStore = defineStore('auth', ()=>{
 
//   const loading = ref(false)
//   const ready = ref(false)
//   const user = ref(null)
//   const error = ref(null)

//   async function login(payload){

//     loading.value =true
//     error.value = false;

//     const params = new URLSearchParams();

//     params.append('username', payload.username)
//     params.append('password', payload.password)

//     try {
//         await axios.post(`${baseUrl}/login/access-token`, params, {withCredentials: true, credentials:'include'})
//         .then(response => {
//           console.log(ready)
//           ready.value  = true
//           user.value = response.data.user
//           console.log(user)
//         }).catch(err => {
//           error.value = err.message
//         }).finally(resp => {
//           loading.value = false
//        })
//       } catch (e){
//         loading.value = false
//         error.value = e 
//       }
//   }

 
  
//   return {user, loading, ready, error, login}

  
// })