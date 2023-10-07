<template>
 <v-container class="position-relative">
  <v-row style="height: 200px;" class="d-flex justify-center">
    <v-col cols="10" class="bg-formbg h- d-inline-flex">
    </v-col>
  </v-row>
  <v-row class="position-absolute w-100" style="top: 40%; left:15%">
    <v-col cols="8">
      <div class="d-flex justify-space-between align-center pt-10 flex-column flex-md-row flex-lg-row">
        <div class="d-flex align-center">
          <v-avatar color="grey" size="150" >
              <v-img cover :src="profile_image"></v-img>
          </v-avatar>
          <div class="px-4 pt-6 d-flex">
            <div>
              <h6 class="text-h6 w-25 text-no-wrap"> {{ user.first_name }} {{ user.last_name }}</h6>
              <p class="text-h6 w-25 mt-n2 text-subtitle-1 text-no-wrap"> {{ user.email }}</p>
            </div>
            <div class="flex">
              <v-menu  :close-on-content-click="false" transition="none">
              <template v-slot:activator="{ props }">
                <v-btn icon="mdi-dots-vertical" v-bind="props" variant="plain" color="black"></v-btn>
              </template>

              <v-list class="elevation-0 border-sm py-0 text-center">
                    <v-btn variant="plain" :ripple="false" class="px-10 text-subtitle-1" :to="{name: 'edit-profile'}">Edit Profile</v-btn>
                    <v-divider/>
                    
                    <v-dialog v-model="dialog" persistent width="500px">
                      <template v-slot:activator="{ props }">
                        <v-btn variant="plain" :ripple="false" v-bind="props" class="text-subtitle-1 text-red">Delete Profile</v-btn>
                      </template>
                      <v-card>
                        <v-card-title class="text-h6">
                          Confirm Account Deletion
                        </v-card-title>
                        <v-divider/>
                        <p class="text-center text-red" v-if="on_error">{{ on_error }}</p>
                        <v-card-text>Are you sure you want to delete your account? You cannot undo this action</v-card-text>
                      
                        <v-card-actions class="pb-10 mt-5">
                          <v-spacer></v-spacer>
                          
                          <v-btn color="" class="mr-2" variant="outlined" @click="dialog=false">Cancel</v-btn>
                          <v-btn elevation="0" rounded="md" class="bg-red"  @click="deleteUser">
                              Delete Account
                          </v-btn>
                          <v-spacer></v-spacer>
                        </v-card-actions>
                      </v-card>
                  </v-dialog>
               
              </v-list>
            </v-menu>
            </div>
          </div>
        </div>
       
        <v-divider class="d-md-none" />
        <div class="mt-md-4 mt-10 mt-lg-10 d-flex align-center">
          <v-btn elevation="0" rounded="xs" class="bg-primary mr-2" :to="{'name' : 'admin'}" v-if="canList || canEdit || canDelete || canCreate">
            Admin
          </v-btn>
          <!-- <v-btn elevation="0" rounded="xs" class="mr-2" variant="outlined" :to="{name: 'edit-profile'}">
            Edit Profile
          </v-btn> -->
          <v-btn color="red" variant="outlined" @click="logout">
              Log out
            </v-btn>
          <!-- <v-dialog v-model="dialog" persistent width="500px">
          <template v-slot:activator="{ props }">
            <v-btn color="red" variant="outlined" v-bind="props">
              Log out
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h6">
              Confirm Account Deletion
            </v-card-title>
            <v-divider/>
            <p class="text-center text-red" v-if="on_error">{{ on_error }}</p>
            <v-card-text>Are you sure you want to delete your account? You cannot undo this action</v-card-text>
           
            <v-card-actions class="pb-10 mt-5">
              <v-spacer></v-spacer>
              <v-btn elevation="0" rounded="md" class="bg-red"  @click="deleteUser">
                  Delete Account
              </v-btn>
              <v-btn color="" class="mr-2" variant="outlined" @click="dialog=false">Cancel</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog> -->
        </div>

       
          
      </div>
    </v-col>
    <v-col cols="4">
      <div class="d-flex align-baseline">
       
      </div>
    </v-col>
  </v-row>
    

    <v-col cols="4">

    </v-col>
  <v-row>

  </v-row>
 </v-container>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import { useAuthStore } from '@/store/auth.store';
import {useDeleteCurrentUser} from "@/composables/admin/useUserActions.js"
import {deleteSession} from "@/composables/useSession.js"
import { useRouter, useRoute } from 'vue-router'
import {usePermissions} from "@/composables/admin/usePermissions"


const canCreate = usePermissions('admin_create_users');
const canDelete = usePermissions('admin_delete_users');
const canEdit = usePermissions('admin_edit_users');
const canList = usePermissions('admin_list_users');


const dialog = ref(false)

const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;
const authStore = useAuthStore()
const user = authStore.user

const isLoading = ref()
const on_error = ref('')
const router = useRouter()

const  profile_image = computed(()=>{
  if(user.profile_img){

    return `${baseUrl}/${user.profile_img}`
  }
})
const deleteUser = async () => {
  const {error, success, loading } = await useDeleteCurrentUser(user.id)

  if(loading.value){
    isLoading.value = loading
  }

  if(success.value){
    isLoading.value = loading.value
    dialog.value = false

    const deletedSession = deleteSession()
    if (deletedSession){
      router.push({name : 'login'})
    }
  } else if(error){
    on_error.value = error
  }

}


const logout = async () =>{
  isLoading.value = user.loading
  console.log('Logging in')
  await authStore.logout()
  if(authStore.ready){
    sessionStorage.clear()
    router.push({'name' : 'login'})
  }
}


// const permissions = computed(()=>{

// })
onMounted(()=>{
  
})

</script>

<style>
/* .v-btn:before {
  opacity: 0 !important;
} */

.v-btn{
  opacity: 1;
}

/* .v-ripple__container {
  opacity: 0 !important;
} */


</style>