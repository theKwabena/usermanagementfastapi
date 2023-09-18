<template>
 <v-container class="position-relative">
  <v-row style="height: 200px;" class="d-flex justify-center">
    <v-col cols="10" class="bg-formbg h- d-inline-flex">
    </v-col>
  </v-row>
  <v-row class="position-absolute w-100" style="top: 40%; left:15%">
    <v-col cols="8">
      <div class="d-flex justify-space-between align-center pt-10 flex-sm-column flex-md-row">
        <div class="d-flex align-center">
          <v-avatar color="grey" size="150">
              <v-img cover src="https://cdn.vuetifyjs.com/images/profiles/marcus.jpg"></v-img>
          </v-avatar>
          <div class="px-4 pt-6">
            <h6 class="text-h6 w-25 text-no-wrap"> Geroge Andam</h6>
            <p class="text-h6 w-25 mt-n2 text-subtitle-1 text-no-wrap"> georgemills@gmail.com</p>
          </div>
        </div>
        <v-divider class="d-md-none" />
        <div class="mt-md-4 mt-sm-10">
          <v-btn elevation="0" rounded="xs" class="bg-primary mr-2" :to="{'name' : 'admin'}">
            Admin
          </v-btn>
          <v-btn elevation="0" rounded="xs" class="mr-2" variant="outlined" :to="{name: 'edit-profile'}">
            Edit Profile
          </v-btn>
          <v-dialog v-model="dialog" persistent width="500px">
          <template v-slot:activator="{ props }">
            <v-btn color="red" variant="outlined" v-bind="props">
              Delete Account
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h6">
              Confirm Account Deletion
            </v-card-title>
            <v-divider/>
            <v-card-text>Are you sure you want to delete your account? This action cannnot is permanent</v-card-text>
           
            <v-card-actions class="pb-10 mt-5">
              <v-spacer></v-spacer>
              <v-btn color="" class="mr-2" variant="outlined" @click="dialog=false">Cancel</v-btn>
              <v-btn elevation="0" rounded="md" class="bg-red"  @click="dialog=false">
                  Delete Account
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
import {ref} from 'vue'
const dialog = ref(false)
</script>

