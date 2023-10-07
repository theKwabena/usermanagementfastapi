<template>
    <v-container class="h-100">
        <v-row align="center" class="h-100">
            <v-col cols="12">
                <v-card class="mx-auto" elevation=10 max-width="500" height="320">
                    <v-card-text class="py-10 h-100">
                        <div class="" v-if="!status.success">
                            <v-row>
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                    New Password</h6>
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
                                    Confirm New Password</h6>
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

                            <v-row class="mb-4">
                                <v-col>
                                    <v-btn class="w-100 bg-primary mb-4" @click="resetPassword" > Reset Password</v-btn>
                                </v-col>
                            </v-row>
                            <!-- <v-progress-circular :size="80" :width="3" indeterminate color="primary"></v-progress-circular>
                            <p class="py-5 text-body-1" > Verifying Email Address</p> -->
                        </div>
                        <div class="d-flex justify-center align-center flex-column" v-if="status.success">  
                            <img src="@/assets/success.svg"/>
                            <v-alert variant="tonal" type="success" class="my-4" text="Success! Your password has been changed" color="primary"></v-alert>
                            <v-btn class="mt-5" color="primary" variant="flat" :to="{'name' : 'login'}">Go to Login</v-btn>
                        </div>

                        <div class="d-flex justify-center align-center flex-column" v-if="status.error">
                            <img src="@/assets/error.svg"/>
                            <v-alert variant="tonal" type="error" class="my-n5" :text="status.error"></v-alert>
                            <!-- <v-btn class="mt-5" color="primary" variant="flat">{{ status.error }}</v-btn> -->
                        </div>
                    </v-card-text>
                 
                </v-card>
            </v-col>
        </v-row>
    </v-container>


    <!-- <v-container
      class="bg-surface-variant mb-6 h-100"
    >
      <v-row
        align="center"
        no-gutters
        class="h-100"
      >
        <v-col
          v-for="n in 3"
          :key="n"
        >
          <v-sheet class="pa-2 ma-2">
            .align-center
          </v-sheet>
        </v-col>
      </v-row>
    </v-container> -->
    <div>

        
    </div>
</template>

<script setup>

import { ref, onMounted, reactive, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth.store';
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers, sameAs, minLength } from '@vuelidate/validators'


const authStore = useAuthStore()
const route = useRoute()
const visible = ref(false)



const status = ref({
    loading : false,
    error : '',
    success : false
})

const user = reactive({
    password : '',
    confirm_password : ''
})

const password1Ref = computed(() => user.password);
const password2Ref = computed(() => user.confirm_password);

const rules = {
    password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password2Ref)
        ),
    },
    confirm_password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password1Ref)
        ),
    }
}

const v$ = useVuelidate(rules, user)

async function resetPassword(){
    console.log('clicked')
    // loading.value = true
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect){
        // loading.value = false
        return
    }
    const token = route.params.email_token
    await authStore.resetPassword({'token' : token, 'new_password' : user.password})

    if (authStore.ready){
        status.value.loading  = false
        status.value.success = true
        
    }

    if(authStore.error){
      error.value = authStore.error
      loading.value = false

    }


}

onMounted( async ()=>{
    // status.value.loading = true

    // const token = route.params.email_token
    // await authStore.verifyEmali(token)

    // if(authStore.ready){
    //     status.value.loading = false
    //     status.value.success = true  
    // } 
    
    // if (authStore.error){
    //     console.log(authStore.error)
    //     status.value.loading = false
    //     status.value.success = false
    //     status.value.error =  authStore.error
    // }


})

</script>

<style lang="scss" scoped>

</style>