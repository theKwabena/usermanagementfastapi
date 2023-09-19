import { defineStore } from 'pinia';
import axios from "axios"
import {ref, reactive} from 'vue'
import { useAsyncState } from '@vueuse/core'

const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

// export const useAuthStore = defineStore({
//     id: 'auth',
//     state: () => ({
//         // initialize state from local storage to enable user to stay logged in
//         user: JSON.parse(localStorage.getItem('user')),
//         returnUrl: null
//     }),
//     actions: {
//         async login(username, password) {
//             const user = await fetchWrapper.post(`${baseUrl}/authenticate`, { username, password });

//             // update pinia state
//             this.user = user;

//             // store user details and jwt in local storage to keep user logged in between page refreshes
//             localStorage.setItem('user', JSON.stringify(user));

//             // redirect to previous url or default to home page
//             router.push(this.returnUrl || '/');
//         },
//         logout() {
//             this.user = null;
//             localStorage.removeItem('user');
//             router.push('/login');
//         }
//     }
// });



export const useAuthStore = defineStore('auth', ()=>{
  const loading = ref(false)
  const ready = ref(false)
  const user = ref(null)
  const error = ref(null)

  async function login(payload){

    loading.value =true
    error.value = false;

    const params = new URLSearchParams();

    params.append('username', payload.username)
    params.append('password', payload.password)

    try {
        await axios.post(`${baseUrl}/login/access-token`, params, {withCredentials: true, credentials:'include'})
        .then(response => {
          console.log(ready)
          ready.value  = true
          user.value = response.data.user
          console.log(user)
        }).catch(err => {
          error.value = err.message
        }).finally(resp => {
          loading.value = false
       })
      } catch (e){
        loading.value = false
        error.value = e 
      }
  }

  return {user, loading, ready, error, login}
})