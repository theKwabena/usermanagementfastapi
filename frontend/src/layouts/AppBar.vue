<template>
  <v-app-bar flat>
    <v-app-bar-title class="d-flex flex-row-reverse px-16">
      <v-btn variant="plain" class="p-0 m-0" :ripple="false" :to="{'name' : 'home'}">

        <v-avatar size="35" class="border-lg p-0 m-0 bg-transparent">
        <v-img cover :src="profile_img" ></v-img>
  </v-avatar>
</v-btn>
    </v-app-bar-title>
  </v-app-bar>
</template>

<script setup>
  import {useAuthStore} from "@/store/auth.store"

  const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;
  const user = useAuthStore().user

  const profile_img = `${baseUrl}/${user.profile_img}`

</script>

<style>

.v-btn{
  opacity: 1
}
</style>