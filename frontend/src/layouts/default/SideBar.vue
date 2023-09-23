<template>
    <v-navigation-drawer color="primary" :width="325">
      <v-list>
        <v-list nav class="mt-10">
          <v-list-item prepend-icon="mdi-account" title="Users" value="Users" :to="{'name' : 'admin-home'}"></v-list-item>
          
          <v-list-item prepend-icon="mdi-account-supervisor-circle" title="Permissions" value="Permissions" :to="{'name' : 'admin-groups'}"></v-list-item>
          <!-- <v-list-item prepend-icon="mdi-account" title="Roles" value="Roles" :to="{'name' :  'admin-roles'}"></v-list-item> -->
          <!-- <v-list-item prepend-icon="mdi-account-supervisor-circle" title="Names" value="Names" :to="{'name' : 'admin-groups'}"> </v-list-item> -->
        </v-list>
      </v-list>
    </v-navigation-drawer>

</template>

<script setup>

</script>

<style>

</style>