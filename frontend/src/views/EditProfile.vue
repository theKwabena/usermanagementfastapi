<template>
    <v-container>
        <v-row class="d-flex justify-center py-10">
            <v-col cols="12" md="6" sm="12" xs="12" order="12">
                <v-sheet class="py-8 bg-formbg">
                    <div class="pa-10 rounded-lg">
                        <div class="">
                            <form class="text-apptext">
                                <div class="d-flex justify-lg-space-between">
                                    <div class="w-50 mr-2">
                                        <div class="">First Name</div>
                                        <v-text-field
                                        
                                            v-model="editUserForm.first_name"
                                            variant="outlined"
                                            class=""
                                        ></v-text-field>
                                    </div>
                                    <div class="w-50 ml-2">
                                        <div>Last Name</div>
                                        <v-text-field
                                            v-model="editUserForm.last_name"
                                            variant="outlined"
                                        ></v-text-field>
                                        </div>
                                    </div>

                                <div >Phone Number</div>
                                <vue-tel-input  v-model="editUserForm.phone_number" mode="international" @validate="handleValidation" :class="inputClass" @on-input="handleInput" class="my-4 py-2"></vue-tel-input>
                                <div >Email Address</div>
                                <v-text-field
                                    disabled
                                    v-model="editUserForm.email"
                                    variant="outlined"
                                ></v-text-field> 

                                <div class="mt-4">
                                <v-btn elevation="0" rounded="md" class="bg-primary px-12">
                                    Save Changes
                                </v-btn>                               
                                 </div>
                            </form>
                        </div>
                    </div>
                </v-sheet>
            </v-col>
            <v-col cols="12" md="4" lg="4" xl="4" order-sm="1" order-md="12">
                <v-sheet class="bg-formbg">
                    <div class=" rounded-lg pb-0 position-relative">
                        <div class="d-flex flex-column align-center pt-10">
                            <v-avatar color="grey" size="150" class="d-flex flex-column justify-center align-center position-relative">
                                <v-img cover :src="userProfilePicture"></v-img>
                                <v-file-input
                                    class="position-absolute overlay px-16 text-center"
                                    style="bottom:0%; top:72%; left:1%"
                                    v-model="editUserForm.profile_picture"
                                   
                                    accept="image/png, image/jpeg, image/bmp"
                                    prepend-icon="mdi-camera"
                                    variant="plain"
                               ></v-file-input>
                            </v-avatar>
                           
                            <div class="overlay">
                               
                            </div>
                        </div>
                        <div class="mb-8 mt-4 text-center">
                                <p> {{ full_name }}</p>
                                <p>{{ user.email }}</p>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100"   size="x-large" variant="text"> Change Email</v-btn>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100 rounded-b-lg" variant="text" size="x-large"> Reset Password</v-btn>
                        </div>
                      
                        
                    </div>
                </v-sheet>
            </v-col>
        </v-row>
          
    </v-container>
    
</template>

<script setup>
    import { reactive,ref, computed } from 'vue' // "from '@vue/composition-api'" if you are using Vue <2.7
    import { useVuelidate } from '@vuelidate/core'
    import { required, email } from '@vuelidate/validators'
    import { useAuthStore } from '@/store/auth.store';
    import { VueTelInput } from 'vue-tel-input';
    import 'vue-tel-input/vue-tel-input.css';

    const user = useAuthStore().user
    // const user = auth.user
    const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;
    const full_name = computed(()=>{
        return `${user.first_name} ${user.last_name}`
    })

   
    const editUserForm = ref({
        id : '',
        first_name : '',
        last_name : '',
        phone_number : '',
        profile_picture : ''
    })

    editUserForm.value = Object.assign({}, user)

    const userProfilePicture = computed(()=>{
        if (editUserForm.value.profile_picture){
            console(editUserForm.value.profile_picture);
            return  URL.createObjectURL(editUserForm.value.profile_picture);
        } else {
            return `${baseUrl}/${user.profile_img}`
        }
    })
   
    const rules = {
        firstName: { required }, // Matches state.firstName
        lastName: { required }, // Matches state.lastName
        contact: {
            email: { required, email } // Matches state.contact.email
        }
        }

    const v$ = useVuelidate(rules, user)
    console.log(user)
</script>


<style lang="scss">
.my-checkbox .v-label  {
  font-size: 16px;
  color : #353434
 
} 

.mdi-checkbox-blank-outline{
    color: #d7d7d7
}

.v-field__input{
    // background-color: red;
    // border: 1px solid #ECECEC;
    outline: none;
    padding: 2;
  
}

.v-input--density-default {
    --v-input-control-height: 46px !important;
    --v-input-padding-top: 8px !important;
}

.vue-tel-input {
    border-radius: 3px;
    display: flex;
    border: 1px solid #bbb;
    text-align: left;
    padding: 4px 0px 4px 0px;
}

.vue-tel-input:focus-within {
    box-shadow: none;
    border-color: rgb(156, 153, 153);
    border-width:2px;
}

.overlay{
    background-color: rgba(22, 22, 22, 0.8);
}


</style>
