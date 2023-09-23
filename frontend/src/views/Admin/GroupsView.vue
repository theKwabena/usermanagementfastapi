<template>
    <div class="pa-16">
        <v-row class="d-flex justify-center">
          <v-col cols="12" md="7" sm="12" xs="12">
              <groups-table/>
          </v-col>

          <v-col cols="12" class="5" md="5" sm="12" xs="12">
             <roles-table/>
          </v-col>
        </v-row>
     </div>

     
  </template>
  <script setup>
  import RolesTable from "@/components/RolesTable.vue"
  import GroupsTable from "@/components/GroupsTable.vue"


</script>

<style scoped lang="scss">
 
</style>