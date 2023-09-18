<template>
    <v-container>
        <v-row>
            <v-col cols="8" md="8" sm="12" xs="12" order-sm="12">
                <v-sheet class="py-8">
                    <div class="bg-formbg pa-10 rounded-lg">
                        <div class="">
                            <form class="text-apptext">
                                <div class="d-flex justify-lg-space-between">
                                    <div class="w-50 mr-2">
                                        <div class="">First Name</div>
                                        <v-text-field
                                            v-model="state.firstName"
                                            variant="outlined"
                                            class=""
                                        ></v-text-field>
                                    </div>
                                    <div class="w-50 ml-2">
                                        <div>Last Name</div>
                                        <v-text-field
                                            v-model="state.firstName"
                                            variant="outlined"
                                        ></v-text-field>
                                        </div>
                                    </div>

                                <div >Phone Nummber</div>
                                <v-text-field
                                    v-model="state.firstName"
                                    variant="outlined"
                                ></v-text-field> 
                                <div >Email Address</div>
                                <v-text-field
                                    v-model="state.firstName"
                                    variant="outlined"
                                ></v-text-field> 
                                <div >Password</div>
                                <v-text-field
                                    v-model="state.firstName"
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
            <v-col cols="4" md="4" sm="12" xs="12" order-sm="1" order-md="12">
                <v-sheet class="py-8">
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
                        <!-- <v-divider/> -->
                        <!-- <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100"   size="x-large" variant="text"> Change Email</v-btn>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100" variant="text" size="x-large"> Reset Password</v-btn>
                        </div>
                        <v-divider/>
                        <div class="text-center">
                            <v-btn  class="text-red text-subtitle-1 w-100" variant="text" size="x-large"> Delete Account</v-btn>
                        </div> -->
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
