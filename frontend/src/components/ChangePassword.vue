<template>

 <v-dialog v-model="dialog" max-width="500px" persistent>
                <template v-slot:activator="{ props }">
                    <v-btn elevation="0" variant="text"  rounded="xs" class="text-apptext text-subtitle-1 w-100 rounded-b-lg" v-bind="props" size="x-large">
                     Change Password
                    </v-btn>
                </template>
                <v-card>
                <v-card-title class="pl-10 pt-4">
                    <span class="text-h6">Change Password</span>
                </v-card-title>
                <v-divider/>
                <v-card-text class="">
                    <v-container>
                        <v-row>
                            <v-col>
                                <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                Old Password</h6>
                                <v-text-field
                                    v-model ="user.old_password"
                                    :append-inner-icon="password_visible.password1 ? 'mdi-eye-off' : 'mdi-eye'"
                                    :type="password_visible.password1 ? 'text' : 'password'"
                                    density="compact"
                                    placeholder="Enter your password"
                                    prepend-inner-icon="mdi-lock-outline"
                                    variant="outlined"
                                    :error-messages="v$.old_password.$errors.map(e => e.$message)"
                                    @click:append-inner="password_visible.password1 = !password_visible.password1"
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row class="mt-n4">
                            <v-col>
                                <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                New Password</h6>
                                <v-text-field
                                    v-model ="user.new_password"
                                    :append-inner-icon="password_visible.password2 ? 'mdi-eye-off' : 'mdi-eye'"
                                    :type="password_visible.password2 ? 'text' : 'password'"
                                    density="compact"
                                    placeholder="Confirm password"
                                    prepend-inner-icon="mdi-lock-outline"
                                    variant="outlined"
                                    :error-messages="v$.new_password.$errors.map(e => e.$message)"
                                    @click:append-inner="password_visible.password2 = !password_visible.password2"
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row class="mt-n4">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                    Confirm New Password</h6>
                                    <v-text-field
                                        v-model ="user.confirm_new_password"
                                        :append-inner-icon="password_visible.password3 ? 'mdi-eye-off' : 'mdi-eye'"
                                        :type="password_visible.password3 ? 'text' : 'password'"
                                        density="compact"
                                        placeholder="Confirm password"
                                        prepend-inner-icon="mdi-lock-outline"
                                        variant="outlined"
                                        :error-messages="v$.confirm_new_password.$errors.map(e => e.$message)"
                                        @click:append-inner="password_visible.password3 = !password_visible.password3"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                    </v-container>
                </v-card-text>
    
                <v-card-actions class="mt-n6 pb-6">
                    <v-spacer></v-spacer>
                    <v-btn border variant="plain" elevation="0" rounded="md" @click="close">
                        Cancel
                    </v-btn>  
                    <v-btn elevation="0" rounded="md" class="bg-primary mr-4"  @click="save" :loading="status.loading">
                        Save Changes
                    </v-btn>
                </v-card-actions>
                </v-card>
            </v-dialog>
</template>

<script setup>
import {ref, reactive, computed, defineEmits, watch} from "vue"
import { useVuelidate } from '@vuelidate/core'
import { required,helpers, sameAs} from '@vuelidate/validators'
import {useAuthStore} from "@/store/auth.store"

const authStore = useAuthStore()

const emit = defineEmits(['success'])
const dialog = ref(false)

const $externalResults = ref({})

const status = ref({
    loading : false,
    error : '',
    success : false
})
const password_visible = ref({
    password1 : false,
    password2 : false,
    password3: false,
})

const user = reactive({
    old_password : '',
    new_password : '',
    confirm_new_password : ''
})

const password1Ref = computed(() => user.new_password);
const password2Ref = computed(() => user.confirm_new_password);

const rules = {
    old_password : {
        required :  helpers.withMessage("Please enter password", required),
    },
    new_password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password2Ref)
        ),
    },
    confirm_new_password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password1Ref)
        ),
    }
}

const v$ = useVuelidate(rules, user, {$externalResults})

function close () {
    v$.value.$reset()
    v$.value.$clearExternalResults();
    dialog.value = false
}


async function save(){
    v$.value.$clearExternalResults();
    status.value.loading = true

    if (!(await v$.value.$validate())){
        status.value.loading =false
        return;

    } 

    status.value.error = '',
    await authStore.changePassword({old_password : user.old_password, new_password : user.new_password})

    if (authStore.ready){
        status.value.loading=false
        status.value.success = true
        emit('success')
        close()


    }

    if (authStore.error){
        status.value.error = authStore.error
        status.value.loading = false
        $externalResults.value ={ old_password : authStore.error}
    }

    status.value.loading = false
}

watch(dialog, val => {
  val || close()
})

</script>

<style lang="scss" scoped>

</style>