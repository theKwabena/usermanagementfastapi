<template>
    <v-layout class="h-100">
      <v-row>
          <v-col cols="12" md="5" class="d-none d-lg-block d-md-block d-xl-block d-xxl-block">
              <div class="h-100 bg-primary">
              </div>
          </v-col>
          <v-col cols="12" md="7" class="d-flex justify-center align-center">
          <div class="">
              <div class="mb-4 px-16 mx-8">
                  <h4 class="letter-spacing text-primary " >Register an  account</h4> 
              </div>

              <div class="mb-6 w-100 d-flex flex-column justify-center align-center">
                <GoogleLogin
                 :callback="externalAuth" 
                 :buttonConfig="btn_cnfig"
                 />
              </div>
              <p class="text-center mt-n3 mb-4 text-error" v-if="error"> {{ error }}</p>
              <div class="w-100 d-flex align-center justify-center">
                  <p class="text-center mb-n3 bg-white px-8" style="z-index: 200;">OR</p>
              </div>
              <v-divider/> 

              <div class="mb-12 mt-6">
                <v-row>
                    <v-col cols="6">
                        <h6 class="text-subtitle-1 text-medium-emphasis">First name</h6>
                        <v-text-field 
                            density="compact"  
                            variant="outlined"
                            placeholder="Enter first name"
                            v-model="user.first_name"
                            :error-messages="v$.first_name.$errors.map(e => e.$message)"
                            >
                        </v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <h6 class="text-subtitle-1 text-medium-emphasis">Last name</h6>
                        <v-text-field 
                            density="compact"  
                            variant="outlined"
                            placeholder="Enter last name"
                            v-model="user.last_name"
                            :error-messages="v$.last_name.$errors.map(e => e.$message)"
                            >
                        </v-text-field>
                    </v-col>
                </v-row>
                <v-row class="mt-n4 mb-n4">
                    <v-col>
                        <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                        Email Address</h6>
                        <v-text-field
                            v-model ="user.email"
                            density="compact"
                            placeholder="Enter an email"
                            prepend-inner-icon="mdi-email"
                            variant="outlined"
                            :error-messages="v$.email.$errors.map(e => e.$message)"
                            
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-row class="mt-n4">
                    <v-col cols="12">
                        <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                        Phone Number</h6>
                        <vue-tel-input v-model="user.phone_number" mode="international" @validate="handleValidation" :class="inputClass" @on-input="handleInput" class="text-apptext"></vue-tel-input>
                        <p class="px-4 text-caption text-error " v-if="phone_error">Enter a valid phone number</p>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
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
                    </v-col>
                </v-row>

                <v-row class="mt-n4">
                    <v-col>
                        <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                        Confirm Password</h6>
                        <v-text-field
                            v-model ="user.confirm_password"
                            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                            :type="visible ? 'text' : 'password'"
                            density="compact"
                            placeholder="Confirm password"
                            prepend-inner-icon="mdi-lock-outline"
                            variant="outlined"
                            :error-messages="v$.confirm_password.$errors.map(e => e.$message)"
                            @click:append-inner="visible = !visible"
                        ></v-text-field>
                    </v-col>
                </v-row>

                

                 
                  <p class="text-center text-apptext text-decoration-underline py-4"> Forgot your password?</p>
                  <div class="w-100">
                      <v-btn  elevation="0" class="bg-primary w-100" size="large" @click="register" :loading="loading">
                          Register
                      </v-btn>
                  </div>

                  
              </div>
          </div>
      
          </v-col>

          
      </v-row>
      

    </v-layout>
</template>

<script setup>
import {ref, reactive,computed} from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers, sameAs, minLength } from '@vuelidate/validators'
import { useAuthStore } from '@/store/auth.store';
import { useRouter, useRoute } from 'vue-router'
import { VueTelInput } from 'vue-tel-input';
import 'vue-tel-input/vue-tel-input.css';
import { GoogleLogin, decodeCredential } from 'vue3-google-login';


const router = useRouter()
const visible = ref(false)
const $externalResults = ref({})
const loading = ref(false)
const error = ref('')

const btn_cnfig = {
    size: "large",
    width  : "700",
    text : 'signup_with',
    logo_alignment : 'center'   
}
const user = reactive({
    first_name : '',
    last_name : '',
    email : '',
    phone_number: '',
    password : '',
    confirm_password : ''
})


//Meethods and variables for phone Number Field
const phone_is_valid=ref(null)
const phone_error = ref(false)
const inputClass = ref('')

const handleInput = ()=> {
    phone_error.value = false
    inputClass.value = ''
}
const handleValidation = (phoneObject) => {
      phone_is_valid.value =  phoneObject.valid;
    };


const password1Ref = computed(() => user.password);
const password2Ref = computed(() => user.confirm_password);
const rules = {
    first_name: { 
        required: helpers.withMessage('First name cannot be empty', required),
        minLength : minLength(2)
     },
    last_name: { 
        required : helpers.withMessage('Last name cannot be empty', required),
        minLength : minLength(2)
    },
    email : {
        required : helpers.withMessage("Please enter email", required), 
        email},
    password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password2Ref)
        ),
    },
    confirm_password : {
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password1Ref)
        ),
    }
}

const v$ = useVuelidate(rules, user, {$externalResults})

const authStore = useAuthStore()




async function register(){
    loading.value = true
    v$.value.$clearExternalResults();
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect){
        loading.value = false
        if (!phone_is_valid.value){
            phone_error.value = true
            inputClass.value =  'invalid-input';
            return
        }
        return
    }  else if (!phone_is_valid.value){
        loading.value = false
        inputClass.value = phone_error.value = 'invalid-input';
        phone_error.value = true
        return
    }

    await authStore.register(user)
    if (authStore.ready){
        loading.value = false
        router.push({name : 'home'})
    }

    //Handle the errors when there is a registration error
    if(authStore.error){
        loading.value = false
        $externalResults.value ={ email : authStore.error}
    }
}

const externalAuth = async (response)=>{
    const userData = decodeCredential(response.credential)
    console.log(userData)
    const last_name = userData.family_name ? userData.family_name : userData.given_name
    
    const payload = {
        first_name : userData.given_name,
        last_name : last_name,
        email : userData.email,
        password : userData.sub,
        email_verified : userData.email_verified,
        auth_identity_provider : 'google' 
    }

    await authStore.register(payload)
    if(authStore.ready){
        //Login user after sign up
        await authStore.login({'username' : payload.email, 'password' : payload.password})
        if(authStore.ready){
            loading.value = false
            router.push({name : 'home'})
        }
        
    }

    if(authStore.error){
        error.value = authStore.error
        loading.value = false

    }

    
}


</script>

<style>

.letter-spacing {
/* Define your desired letter spacing */
  color: #3AAF9F;
  font-size: 38px;
  font-style: black;
  font-weight: 300;
  line-height: normal;
  letter-spacing: -2.9px;
}
.log-width{
  width: 50%
}

.vue-tel-input {
    border-radius: 3px;
    display: flex;
    border: 1px solid #bbb;
    text-align: left;
    padding: 4px 0px 4px 0px;
}

.vue-tel-input:focus-within {
    box-shadow: none;
    border-color: black;
    border-width:2px;
}


.invalid-input {
  border: 1px solid red; /* Change to your desired invalid input style */
}

.v-field__outline {
  --v-field-border-width: 0.5px;
  --v-field-border-opacity: 0.38;
  
}


</style>