<template>
    <v-container>
        <v-row no-gutters>
            <v-col cols="7">
                <v-sheet class="pa-8">
                    <div class="bg-formbg pa-10 rounded-lg">
                        <div class="pb-6">
                            <h6 class="text-h6 text-apptext mb-3">Edit user profile</h6>
                            <v-divider/>
                        </div>
                    <div class="">
                        <form class="text-apptext">
                            <div class="">First Name</div>
                                <v-text-field
                                    v-model="state.firstName"
                                    variant="outlined"
                                    class=""
                                ></v-text-field>

                            <div>Last Name</div>
                            <v-text-field
                                v-model="state.firstName"
                                variant="outlined"
                            ></v-text-field>

                            <div >Phone Nummber</div>
                            <v-text-field
                                v-model="state.firstName"
                                variant="outlined"
                            ></v-text-field> 

                            <div>Roles</div>
                            <div class="ml-n2">
                                <v-checkbox
                                    v-model="ex4"
                                    label="Create Users"
                                    color="primary"
                                    hide-details
                                    class="my-checkbox"
                                    
                                ></v-checkbox>
                            
                                <v-checkbox
                                    v-model="ex4"
                                    label="Edit Users"
                                    color="primary"
                                    value=""
                                    class="my-checkbox"
                                    hide-details
                                ></v-checkbox>
                                
                                <v-checkbox
                                    v-model="ex4"
                                    label="Delete Users"
                                    color="primary"
                                    value=""
                                    
                                    hide-details
                                    class="my-checkbox"
                                ></v-checkbox>
                            </div>

                            <div class="text-apptext mt-4">Groups</div>
                            <div class="ml-n2">
                                <v-checkbox
                                    v-model="ex4"
                                    label="Admin"
                                    color="primary"
                                    hide-details
                                    class="my-checkbox"
                                    
                                ></v-checkbox>
                            
                            </div>
                            <div class="mt-8">
                                <v-btn elevation="0" rounded="md" class="bg-primary mr-4">
                                    Save Changes
                                </v-btn>
                                <v-btn border variant="plain" elevation="0" rounded="md">
                                    Cancel
                                </v-btn>                                

                            </div>
                        </form>
                    </div>
                    </div>
                    
                </v-sheet>
            </v-col>
            <v-col cols="4">
                <v-sheet class="pa-8">
                    <div class="bg-formbg rounded-lg pb-4">
                        <div class="d-flex flex-column align-center pt-10">
                            <v-avatar color="grey" size="150">
                                <v-img cover src="https://cdn.vuetifyjs.com/images/profiles/marcus.jpg"></v-img>
                            </v-avatar>
                        </div>
                        <div class="mb-8 mt-4 text-center">
                                <p> Emmanuel Abbey</p>
                                <p>mail@test.com</p>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100"   size="x-large" variant="text"> Change Username</v-btn>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100" variant="text" size="x-large"> Reset Password</v-btn>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-red text-subtitle-1 w-100" variant="text" size="x-large"> Delete Account</v-btn>
                        </div>
                    </div>
                </v-sheet>
            </v-col>
        </v-row>
    </v-container>
    
</template>

<script setup>
    import { reactive } from 'vue' // "from '@vue/composition-api'" if you are using Vue <2.7
    import { useVuelidate } from '@vuelidate/core'
    import { required, email } from '@vuelidate/validators'

    const state = reactive({
      firstName: '',
      lastName: '',
      contact: {
        email: ''
      }
    })

    const rules = {
        firstName: { required }, // Matches state.firstName
        lastName: { required }, // Matches state.lastName
        contact: {
            email: { required, email } // Matches state.contact.email
        }
        }

    const v$ = useVuelidate(rules, state)

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
    outline: noen;
    padding: 0;
  
}

.v-input--density-default {
    --v-input-control-height: 46px !important;
    --v-input-padding-top: 8px !important;
}


</style>
