<template>
   
    <v-layout class="h-100">
      <v-row>
          <v-col cols="12" md="5" class="d-none d-lg-block d-md-block d-xl-block d-xxl-block">
              <div class="h-100 bg-primary">
              </div>
          </v-col>
          <v-col cols="12" md="7" class="d-flex justify-center align-center">
          <div class="w-50">
              <div class="mb-10">
                  <h4 class="letter-spacing text-primary" >Reset Password</h4> 
                  <p class="text-secondary mt--2" style="font-size: 22px; font-weight: 300;">Please enter the <span class="font-weight-bold">
                  email</span> address associated with your account</p> 
              </div>

              <!-- <v-divider/>  -->
              <v-alert variant="tonal" type="success" v-if="success" class="my-4" text="A password reset link has been sent to your email account. Please follow to reset your password" color="primary"></v-alert>

              <p class="text-center mt-4 mb-n4 text-error" v-if="error"> {{ error }}</p>
              <div class="mb-12 mt-6">
                  <!-- <h6 class="text-subtitle-1 text-medium-emphasis">Email</h6> -->
                  <v-text-field 
                      density="compact"  
                      placeholder="Email address" 
                      prepend-inner-icon="mdi-email"
                      variant="outlined"
                      v-model="user.email"
                      :error-messages="v$.email.$errors.map(e => e.$message)"
                      >
                  </v-text-field>
                  <div class="w-100">
                      <v-btn  elevation="0" class="bg-primary w-100" size="large" @click="resetPassword" :loading="loading">
                          Send Password Reset Link
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
const success = ref(false)



const user = reactive({
    email : '',
   
})

const rules = {
  email : {
      required : helpers.withMessage("Please enter email", required), email
    }
  
}

// console.log(loginData)
const v$ = useVuelidate(rules, user)

const authStore = useAuthStore()


async function resetPassword(){
  error.value = ''
  loading.value = true
  const isFormCorrect = await v$.value.$validate()
  if (!isFormCorrect){
      loading.value=false
      return

  } 

  await authStore.requestPasswordReset({ email: user.email })


  if(authStore.error){
      error.value = authStore.error
      loading.value = false
  }

  if(authStore.ready){
    loading.value= false
    success.value = true
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