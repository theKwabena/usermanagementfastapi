import { defineStore } from 'pinia';
import axios from "axios"


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

export const useGroupStore = defineStore('group', {
  state : ()=>({
    isLoading:false, 
    isReady:false,  
    on_error:null,
    all_groups : null
  }),
  
  getters: {
    loading : (state) => state.isLoading,
    ready : (state) => state.isReady,
    groups : (state) => state.all_groups,
    error :(state) => state.on_error,
   
  },
actions : {
    async getGroups(){
        this.isLoading = true
        await axios.get(`${baseUrl}/admin/groups/`, {withCredentials: true, credentials: 'include'})
        .then(response => {
            this.all_groups = response.data
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

