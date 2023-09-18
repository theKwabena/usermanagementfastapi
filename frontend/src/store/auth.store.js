import { defineStore } from 'pinia';

import {ref, reactive} from 'vue'
import { useAsyncState } from '@vueuse/core'

const baseUrl = `${import.meta.env.BACKEND_API_URL}/`;

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
    const { state, isReady, isLoading, execute,error } = useAsyncState(
        async (args) => {
          // Perform your asynchronous operation using the dynamic data passed in args
          // For example, you can make an Axios request with a dynamic URL
          const response = await axios[args.method](`${baseUrl}/${args.path}`,args.payload, {withCredentials: true, credentials: 'include'});
          return response.data;
        },
        null, // Set initial state if needed
        {
          immediate: false, // Do not execute immediately
        },
    );

    return state, isReady, isLoading, execute, error
})