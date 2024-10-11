<template>
    <v-container>
        <v-snackbar v-model="success" color="primary" location="top" timeout="2000"> 
        Password changed successful
        </v-snackbar>
        <v-row class="d-flex justify-center py-10">
            <v-col cols="12" md="6" sm="12" xs="12" order="12">
                <v-sheet class="py-8 bg-formbg border-sm rounded-lg">
                    <div class="pa-10 rounded-lg">
                        <div class="">
                            <div class="text-apptext">
                                <v-row>
                                    <v-col cols="6">
                                        <h6 class="text-subtitle-1 text-medium-emphasis">First name</h6>
                                        <v-text-field 
                                            density="compact"  
                                            variant="outlined"
                                            placeholder="Enter first name"
                                            v-model="editUserForm.first_name"
                                            :error-messages="v$.first_name.$errors.map(e => e.$message)"
                                            >
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <h6 class="text-subtitle-1 text-medium-emphasis">Last name</h6>
                                        <v-text-field 
                                            density="compact"  
                                            variant="outlined"
                                            placeholder="Enter last name"
                                            v-model="editUserForm.last_name"
                                            :error-messages="v$.last_name.$errors.map(e => e.$message)"
                                            >
                                        </v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row class="mt-n4 mb-n4">
                                    <v-col>
                                        <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                        Email Address</h6>
                                        <v-text-field
                                            v-model ="editUserForm.email"
                                            density="compact"
                                            placeholder="Enter an email"
                                            prepend-inner-icon="mdi-email"
                                            variant="outlined"
                                            disabled                                            
                                        ></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row class="mt-n4">
                                    <v-col cols="12">
                                        <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                        Phone Number</h6>
                                        <vue-tel-input v-model="editUserForm.phone_number" :validCharactersOnly="true" mode="international" @validate="handleValidation" :class="inputClass" @on-input="handleInput" class="text-apptext"></vue-tel-input>
                                        <p class="px-4 text-caption text-error " v-if="phone_error">Enter a valid phone number</p>
                                    </v-col>
                                </v-row>

                                <div class="mt-4">
                                <v-btn elevation="0" :disabled="!hasFormChanged && !preview_image" rounded="md" class="bg-primary px-12" @click="save" :loading="loading">
                                    Save Changes
                                </v-btn>                               
                                 </div>
                            </div>
                        </div>
                    </div>
                </v-sheet>
            </v-col>
            <v-col cols="12" md="4" lg="4" xl="4" order-sm="1" order-md="12">
                <v-sheet class="bg-formbg border-sm rounded-lg">
                    <div class=" rounded-lg pb-0 position-relative">
                        <v-btn variant="plain" :ripple="false" size="x-large" @click="remove_image" v-if="preview_image" class="position-absolute move-up" id="profile-input" style="top:8%; right:15%">
                            <v-icon icon="mdi-close-circle-outline" color="black" size="large" ></v-icon>
                        </v-btn>
                        <div class="d-flex flex-column align-center pt-10">
                            
                            <v-avatar color="grey" size="150" class="d-flex flex-column justify-center align-center position-relative">
                                <v-img cover :src="userProfilePicture"></v-img>
                                <div class="overlay position-absolute px-16 pb-10" style="top:80%">
                                    <div class="image-upload">
                                        <label for="profile-input">
                                            <v-icon icon="mdi-camera" color="white"></v-icon>
                                        </label>
                                        <input type="file" @change="onFileChange" accept="image/png" id="profile-input" class="d-none"  @click="$event.target.value=''" />
                                    </div>
                                </div>
                            </v-avatar>
                        </div>
                        <div class="mb-8 mt-4 text-center">
                                <p> {{ full_name }}</p>
                                <p>{{ user.email }}</p>
                        </div>
                        <v-divider/>
                        <!-- <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100"   size="x-large" variant="text"> Change Email</v-btn>
                        </div> -->
                        <change-password @success="success=true"/>
                        <!-- <v-divider/> -->
                        <!-- <div class="text-center">
                            <v-btn  class="text-apptext text-subtitle-1 w-100 rounded-b-lg" variant="text" size="x-large"> Change Password</v-btn>
                        </div> -->
                      
                      
                        
                    </div>
                </v-sheet>
            </v-col>
        </v-row>
          
    </v-container>
    
</template>

<script setup>
    import { reactive,ref, computed } from 'vue' // "from '@vue/composition-api'" if you are using Vue <2.7
    import { useVuelidate } from '@vuelidate/core'
    import { required, email, helpers, minLength } from '@vuelidate/validators'
    import { useAuthStore } from '@/store/auth.store';
    import { VueTelInput } from 'vue-tel-input';
    import 'vue-tel-input/vue-tel-input.css';

    import ChangePassword from "@/components/ChangePassword.vue"

    const success  = ref(false)
    const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;
    const loading = ref(null)
    const authStore = useAuthStore()
    
    const user = authStore.user

    const full_name = computed(()=>{
        return `${user.first_name} ${user.last_name}`
    })

    const profile_picture = ref('')
   const preview_image = ref('')

    const editUserForm = ref({
        first_name : '',
        last_name : '',
        phone_number : '',
        profile_picture : ''
    })

    editUserForm.value = Object.assign({}, user)

    function onFileChange(e) {
        if(e){
            console.log('changing')
            const file = e.target.files[0];
            profile_picture.value = file
            preview_image.value = URL.createObjectURL(file)
        }
    }
  
    function remove_image(){
        preview_image.value = ''
    }
   
    
    const userProfilePicture = computed(()=>{
        if (preview_image.value){
            return preview_image.value
        } else {
            if(user.profile_img){
                return `${baseUrl}/${user.profile_img}`
            }
        }
    })

    //Check if form has changed 
    const hasFormChanged = computed(() => {
        const formValues = editUserForm.value;
        for (const key in formValues) {
            if (formValues.hasOwnProperty(key)) {
            if (formValues[key] !== user[key]) {
                return true; // There's a change
            }
            }
        }
        return false; // No changes detected
    });
    //Validations

    const rules = {
        first_name: { 
            required: helpers.withMessage('First name cannot be empty', required),
            minLength : minLength(2)
        },
        last_name: { 
            required : helpers.withMessage('Last name cannot be empty', required),
            minLength : minLength(2)
        },
    }

    const phone_is_valid=ref(null)
    const phone_error = ref(false)
    const inputClass = ref('')

    const handleInput = ()=> {
        phone_error.value = false
        inputClass.value = ''
    }

    const handleValidation = (phoneObject) => {
        phone_is_valid.value =  phoneObject.valid;
        console.log(phoneObject.valid)
        };



    const v$ = useVuelidate(rules, editUserForm)
    

    async function save(){
        console.log(hasFormChanged.value)
        if(!hasFormChanged.value){
            //Form data hasn't changed but profile picture has
            console.log('saving image')
            let formData = new FormData()
            formData.append('file', profile_picture.value)
            await authStore.updateProfilePicture(formData)
            if(authStore.ready){
                location.reload()
                return
            }
        }

        loading.value = true
        const isFormCorrect = await v$.value.$validate()
        if(!isFormCorrect){
            loading.value = false
            if (!phone_is_valid.value){
                phone_error.value = true
                inputClass.value =  'invalid-input';
                return
            }
            return
        } else if (!phone_is_valid.value){
            loading.value = false
            inputClass.value = phone_error.value = 'invalid-input';
            phone_error.value = true
            return
        }

        await authStore.editUser(editUserForm.value)
        if(authStore.ready){
            loading.value = false
            location.reload()

        }
        loading.value=false
    }
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

.move-up{
    z-index: 1000;
}

</style>
