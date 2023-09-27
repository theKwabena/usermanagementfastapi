<template>
    <v-data-table
        :headers="headers"
        :items="roles"
        :loading="isLoading"
        class="px-8 pb-4 border-sm rounded-lg text-apptext">
        
        <template v-slot:top>
        <v-toolbar flat class="bg-white pt-4">
            <!-- <v-toolbar-title class="">Roles</v-toolbar-title> -->
            <!-- <v-spacer></v-spacer> -->
            <v-dialog v-model="dialog" max-width="500px" persistent>
            <template v-slot:activator="{ props }">
                <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props" size="small">
                    <v-icon icon="mdi-plus"></v-icon> 
                    Add New Role
                </v-btn>
            </template>
            <v-card>
                <v-card-title class="pl-10 pt-4">
                <span class="text-h6">{{ formTitle }}</span>
                </v-card-title>
                <v-divider/>
                <v-card-text class="">
                <v-container>
                    <v-row>
                    <h6 class="text-subtitle-1 text-medium-emphasis pl-3"> Role Name</h6>
                    <v-col cols="12" sm="6" md="12">
                        <v-text-field
                        :error-messages="v$.name.$errors.map(e => e.$message)"
                        @input="v$.name.$touch"
                        @blur="v$.name.$touch"
                        v-model="editedRole.name"
                        variant="outlined"
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
                <v-btn elevation="0" rounded="md" class="bg-primary mr-4"  @click="save">
                    Save Changes
                </v-btn>
                </v-card-actions>
            </v-card>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px" persistent>
            <v-card>
                <v-card-title class="text-h6 text-wrap pl-4 pt-4">Confirm Delete Group</v-card-title>
                <v-divider />
                <v-card-text class="">
                    <v-container>
                        <v-row>
                        <v-col cols="12" sm="6" md="12">
                            <h6 class="text-subtitle-1 text-medium-emphasis text-center"> Are you sure you want to delete group <strong> {{editedRole.name}} </strong>? </h6>
                        </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions class="pb-10 mt-n5">
                    <v-spacer></v-spacer>
                    <v-btn elevation="0" rounded="md" class="bg-red  px-4"  @click="deleteItemConfirm(editedRole.id)">
                        Delete Role
                    </v-btn>
                    <v-btn color="primary" class="mr-2" variant="outlined" @click="closeDelete">
                        Cancel
                    </v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
            </v-dialog>
        </v-toolbar>
        </template>
        <template v-slot:item.role="{ item }">
        <div class="py-2">
            <div v-for="role in item.raw.roles" :key="role.id">
            <p> {{role.name}}</p>
            </div>
        </div>
        </template>
        <template v-slot:item.actions="{ item }">
        <div class="d-flex">
            <v-icon
            size="small"
            class="me-4"
            @click="editItem(item.raw)"
        >
        mdi-square-edit-outline
        </v-icon>

        <v-icon
            size="small"
            @click="deleteItem(item.raw)"
        >
            mdi-delete
        </v-icon>
        </div>
       
        </template>
        <template v-slot:no-data>
        <p> No Roles Available, Create New Role</p>
        </template>

        <template v-slot:bottom>
        <!-- <div class="text-center ml-n16 mr-16 pt-10">
        <v-pagination
            v-model="page"
            :length="pageCount"
        ></v-pagination>
        </div> -->
        </template> 
    </v-data-table>
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import {useRoleStore} from "@/store/role.store";
import { useCreateRole, useEditRole, useDeleteRole } from '@/composables/admin/useRoleActions';
import { useVuelidate } from '@vuelidate/core'
import { helpers, minLength, required} from '@vuelidate/validators';


const roleStore = useRoleStore()
const dialog = ref(false)
const dialogDelete = ref(false)
const isLoading = ref(true)
const on_error = ref('')
const $externalResults = ref({})
const headers = ref([
  {
    title: 'Roles',
    align: 'start',
    sortable: false,
    key: 'name',
    // width : "35%"
  },

  { title: 'Actions', key: 'actions', sortable: false, width:"25%" },
])

const roles = ref([])

const editedIndex = ref(-1)

const editedRole = ref({
  name: '',
})
const defaultRole = ref({
  name: '',
})

const rules = {
    name : {
        required : helpers.withMessage('Role name cannot be empty', required),
        minLength : minLength(2)
    }
}

const v$ = useVuelidate(rules, editedRole, {$externalResults})

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Create Role' : 'Edit Role'
})



async function initialize () {
    isLoading.value=true
    await roleStore.getRoles()
    roles.value = roleStore.roles
    isLoading.value=false
}

function editItem (item) {
  editedIndex.value = roles.value.indexOf(item)
  editedRole.value = Object.assign({}, item)
  console.log(editedRole.value)
  dialog.value = true
}

function deleteItem (item) {
  editedIndex.value = roles.value.indexOf(item)
  editedRole.value = Object.assign({}, item)
  dialogDelete.value = true
}

async function deleteItemConfirm (group_id) { 
  const {error, success, loading } = await useDeleteRole(group_id)
  if(loading.value){
    isLoading.value = loading
  }

  if(success.value){
    location.reload()
    // roles.value.splice(editedIndex.value, 1)
    // isLoading.value = loading.value
    // closeDelete()
  }
}

function close () {
    v$.value.$reset()
    v$.value.$clearExternalResults();

    dialog.value = false
    nextTick(() => {
    editedRole.value = Object.assign({}, defaultRole.value)
    editedIndex.value = -1
    })
}

async function closeDelete () {
    
  dialogDelete.value = false
  await nextTick()
  editedRole.value = Object.assign({}, defaultRole.value)
  editedIndex.value = -1
}

async function save() {
    v$.value.$clearExternalResults();

    if (!(await v$.value.$validate())) return;

    const isEditing = editedIndex.value > -1;
    const apiFunction = isEditing ?  useEditRole : useCreateRole;
    const apiPayload = editedRole.value;

    isEditing ? undefined : delete apiPayload.id
    
    try {

      let apiResponse;
      if (isEditing) {
            // Send the request without the 'id' when editing
            apiResponse = await apiFunction(editedRole.value.id, apiPayload);
        } else {
            // Send the request with the complete payload when creating
            apiResponse = await apiFunction(apiPayload);
        }


        const { role, loading, success, error } = apiResponse;
       

        loading.value && (isLoading.value = loading.value);

        if (success.value) {
            // if (isEditing) {
            //     Object.assign(roles.value[editedIndex.value], role.value);
            // } else {
            //     roles.value.push(role.value);
            // }
            location.reload()
            // close();
        }

        if (error.value ) {
            $externalResults.value = { name: [error.value] };
           on_error.value = error.value
        }
    } catch (e) {
        // Handle any unexpected errors here
        console.error(e);
    }
}


watch(dialog, val => {
  val || close()
})
watch(dialogDelete, val => {
  val || closeDelete()
})

onMounted(()=>{

  initialize()
})

</script>

<style lang="scss" scoped>

</style>