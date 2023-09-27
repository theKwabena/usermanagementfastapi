<template>
    <v-navigation-drawer color="primary" :width="325">
      <v-list>
        <v-list nav class="mt-10">
          <v-list-item prepend-icon="mdi-account" title="Users" value="Users" :to="{'name' : 'admin-users'}"></v-list-item>
          
          <v-list-item v-if="user.is_superuser" prepend-icon="mdi-account-supervisor-circle" title="Permissions" value="Permissions" :to="{'name' : 'admin-permissions'}"></v-list-item>
        </v-list>
      </v-list>
    </v-navigation-drawer>

</template>

<script setup>

import { useAuthStore } from '@/store/auth.store';
const authStore = useAuthStore()
const user = authStore.user


</script>

<style>

</style>