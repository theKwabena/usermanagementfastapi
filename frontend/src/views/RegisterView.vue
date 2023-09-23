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

              <div class="mb-6 d-flex flex-column">
                  <v-btn variant="outlined" size="large" class="mb-4 text-apptext text-subtitle" prepend-icon="mdi-google">
                  Continue with Google
                  </v-btn>
              </div>
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
                        <vue-tel-input v-model="user.phone_number" mode="international" @validate="handleValidation" :class="inputClass" @on-input="handleInput"></vue-tel-input>
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

const router = useRouter()
const visible = ref(false)
const $externalResults = ref({})
const loading = ref(false)

const user = reactive({
    first_name : '',
    last_name : '',
    email : '',
    phone_number: '',
    password : '',
    confirm_password : ''
})


//Methods and vars for phone Number Field
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
        if (!phone_is_valid.value){
            phone_error.value = true
            inputClass.value =  'invalid-input';
            return
        }
        return
    }  else if (!phone_is_valid.value){
        inputClass.value = phone_error.value = 'invalid-input';
        phone_error.value = true
        return
    }

    await authStore.register(user)
    if (authStore.ready){
        loading.value = false
        router.push({name : 'home'})
    }

    if(authStore.error){
        $externalResults.value ={ email : authStore.error}
    }
}



</script>

<style scoped>
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



.invalid-input {
  border: 1px solid red; /* Change to your desired invalid input style */
}
</style>