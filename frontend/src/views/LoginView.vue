<template>
      <v-layout class="h-100">
        <v-row>
            <v-col cols="12" md="5" class="d-none d-lg-block d-md-block d-xl-block d-xxl-block">
                <div class="h-100 bg-primary">
                </div>
            </v-col>
            <v-col cols="12" md="7" class="d-flex justify-center align-center">
            <div class="">
                <div class="mb-10">
                    <h4 class="letter-spacing text-primary" >Login to your account</h4> 
                    <p class="text-secondary mt--2" style="font-size: 22px; font-weight: 300;">Don't have an account? <span class="font-weight-bold">
                        <router-link :to="{name : 'register'}" class="text-none text-decoration-none text-apptext">
                            Sign up
                        </router-link>
                    </span></p> 
                </div>

                <div class="mb-6 d-flex flex-column">
                    <v-btn variant="outlined" size="large" class="mb-4" prepend-icon="mdi-google">
                    Sign in with Google
                    </v-btn>
                </div>
                <div class="w-100 d-flex align-center justify-center">
                    <p class="text-center mb-n3 bg-white px-8" style="z-index: 200;">OR</p>
                </div>
                <v-divider/> 
                <p class="text-center mt-4 mb-n4 text-error" v-if="error"> {{ error }}</p>
                <div class="mb-12 mt-6">
                    <h6 class="text-subtitle-1 text-medium-emphasis">Email</h6>
                    <v-text-field 
                        density="compact"  
                        placeholder="Email address" 
                        prepend-inner-icon="mdi-email"
                        variant="outlined"
                        v-model="user.email"
                        :error-messages="v$.email.$errors.map(e => e.$message)"
                        >
                    </v-text-field>

                    <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                        Password</h6>
                    <v-text-field
                        v-model ="user.password"
                        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                        :type="visible ? 'text' : 'password'"
                        density="compact"
                        placeholder="Enter your password"
                        prepend-inner-icon="mdi-lock-outline"
                        variant="outlined"
                        :error-messages="v$.password.$errors.map(e => e.$message)"
                        @click:append-inner="visible = !visible"
                    ></v-text-field>
                    <p class="text-center text-apptext text-decoration-underline py-4"> Forgot your password?</p>
                    <div class="w-100">
                        <v-btn  elevation="0" class="bg-primary w-100" size="large" @click="login" :loading="loading">
                            Login
                        </v-btn>
                    </div>

                    
                </div>
            </div>
        
            </v-col>

            
        </v-row>
        

      </v-layout>
</template>

<script setup>
import {ref, reactive} from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers } from '@vuelidate/validators'
import { useAuthStore } from '@/store/auth.store';
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const visible = ref(false)
const loading = ref(false)
const error = ref('')
const user = reactive({
    email : '',
    password : ''
})

const rules = {
    email : {
        required : helpers.withMessage("Please enter email", required), 
        email},
    password : {
        required : helpers.withMessage("Please enter password", required),
    }
}

// console.log(loginData)
const v$ = useVuelidate(rules, user)

const authStore = useAuthStore()


async function login(){
    error.value = ''
    loading.value = true
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    await authStore.login({ username: user.email, password:user.password })
    console.log(authStore.ready)

    if(authStore.error){
        error.value = authStore.error
        loading.value = false
    }

    if(authStore.ready){
        // localStorage.setItem('token', get_user.user.access_token)
        router.push(
            {
                name : 'home'
            }
        )
        loading.value = false
    } 
  
}



</script>

<style scoped>
.letter-spacing {
  /* Define your desired letter spacing */
    color: #3AAF9F;
    font-size: 48px;
    font-style: black;
    font-weight: 400;
    line-height: normal;
    letter-spacing: -2.9px;
}
.log-width{
    width: 50%
}
</style>