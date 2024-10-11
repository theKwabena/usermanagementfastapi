import { defineStore } from 'pinia';
import axios from "axios"


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

export const useRoleStore = defineStore('role', {
  state : ()=>({
    isLoading:false, 
    isReady:false,  
    on_error:null,
    all_roles : null
  }),
  
  getters: {
    loading : (state) => state.isLoading,
    ready : (state) => state.isReady,
    roles : (state) => state.all_roles,
    error :(state) => state.on_error,
   
  },
actions : {
    async getRoles(){
        this.isLoading = true
        await axios.get(`${baseUrl}/admin/roles/`, {withCredentials: true, credentials: 'include'})
        .then(response => {
            this.all_roles = response.data
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

