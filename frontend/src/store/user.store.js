import { defineStore } from 'pinia';
import axios from "axios"


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

export const useUserStore = defineStore('user', {
  state : ()=>({
    isLoading:false, 
    isReady:false, 
    current_user:null, 
    on_error:null,
    all_users : null
  }),
  getters: {
    loading : (state) => state.isLoading,
    ready : (state) => state.isReady,
    users : (state) => state.all_users,
    error :(state) => state.on_error,
   
  },
  actions : {
    async getCurrentUser(){
        this.isLoading = true
        await axios.get(`${baseUrl}/profile`,  {withCredentials: true, credentials:'include'})
        .then(response => {
            this.data = response.data
        })
        .catch((err)=>{
            this.error = err
        })
        .finally(()=>{
            this.isLoading = false
        })
    },

    async getUsers(){
        this.isLoading = true
        await axios.get(`${baseUrl}/users/`, {withCredentials: true, credentials: 'include'})
        .then(response => {
            this.all_users = response.data
        })
        .catch((err)=>{
            this.err= err
        })
        .finally(()=>{
            this.isLoading = false
        })
    }
  },
})

