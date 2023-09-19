<template>
      <v-layout class="">
        <v-sheet
            class="d-flex rounded-0 align-center justify-center"
            elevation="1"
            
            height="100vh"
            rounded
            width="100%"
        > 
        <div class="h-100 w-50 bg-primary">
            
        </div>

        <div class="h-100 w-75 d-flex justify-center">
            <div class="w-75 d-flex flex-column justify-center align-center">
                <div class="mb-12">
                    <h4 class="letter-spacing text-primary">Login to your account</h4> 
                    <p class="text-secondary mt--2 text-h6">Don't have an account? <span class="font-weight-bold">Sign up</span></p> 
                </div>

                <div class="log-width mb-12 d-flex flex-column">
                    <v-btn variant="outlined" size="large" class="mb-4">
                    Sign in with Google
                    </v-btn>
                    <v-btn variant="outlined" size="large" class="">
                    Sign in with Facebook
                    </v-btn>
                </div>
                <div class="mb-12 log-width">
                    <form>

                    </form>
                    <h6 class="text-subtitle-1 text-medium-emphasis">Email</h6>
                    <v-text-field 
                        density="compact"  
                        placeholder="Email address" 
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
                    <div class="log-width w-100">
                        <v-btn  elevation="0" class="bg-primary w-100" size="large" @click="login">
                            Login
                        </v-btn>
                    </div>
                </div>
            </div>
           
        </div>

        </v-sheet>

      </v-layout>
</template>

<script setup>
import {ref, reactive} from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers } from '@vuelidate/validators'
import { useAuthStore } from '@/store/auth.store';

const visible = ref(false)

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

const get_user = useAuthStore()
console.log(get_user)
async function login(){
    console.log('logins')
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return
    get_user.execute(0, {email: user.email, password:user.password})
}



</script>

<style scoped>
.letter-spacing {
  /* Define your desired letter spacing */
    color: #3AAF9F;
    font-size: 45px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    letter-spacing: -2.7px;
}
.log-width{
    width: 50%
}
</style>