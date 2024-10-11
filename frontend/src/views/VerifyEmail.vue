<template>
    <v-container class="h-100">
        <v-row align="center" class="h-100">
            <v-col cols="12">
                <v-card class="mx-auto" elevation=10 max-width="500" height="400">
                    <v-card-text class="d-flex justify-center align-center h-100">
                        <div class="d-flex justify-center align-center flex-column" v-if="status.loading">
                            <v-progress-circular :size="80" :width="3" indeterminate color="primary"></v-progress-circular>
                            <p class="py-5 text-body-1" > Verifying Email Address</p>
                        </div>
                        <div class="d-flex justify-center align-center flex-column" v-if="status.success">  
                            <img src="@/assets/success.svg"/>
                            <v-alert variant="tonal" type="success" class="my-4" text="Success! Your email has been verified" color="primary"></v-alert>
                            <v-btn class="mt-5" color="primary" variant="flat" :to="{'name' : 'home'}">Go to Dashboard</v-btn>
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

import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth.store';


const authStore = useAuthStore()
const route = useRoute()

const status = ref({
    loading : false,
    error : '',
    success : false
})



onMounted( async ()=>{
    status.value.loading = true

    const token = route.params.email_token
    await authStore.verifyEmali(token)

    if(authStore.ready){
        status.value.loading = false
        status.value.success = true  
    } 
    
    if (authStore.error){
        console.log(authStore.error)
        status.value.loading = false
        status.value.success = false
        status.value.error =  authStore.error
    }


})

</script>

<style lang="scss" scoped>

</style>