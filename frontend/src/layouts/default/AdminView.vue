<template>
    <v-app>
        <side-bar /> 
        <app-bar/>
        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script setup>
    import SideBar from "./SideBar.vue"
    import AppBar from "../AppBar.vue";
</script>
