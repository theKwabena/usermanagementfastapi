<template>
    <v-data-table    
        :hide-default-footer="true"
        :headers="headers"
        :items="groups"
        :loading="isLoading"
        class="px-8 pb-4 border-sm rounded-lg text-subtle text-apptext">
        <template v-slot:top>
            <v-toolbar flat class="bg-white pt-4">
                
            <!-- <v-toolbar-title class="">Groups</v-toolbar-title> -->
            <!-- <v-spacer></v-spacer> -->
            <v-dialog v-model="dialog" max-width="500px" persistent>
                <template v-slot:activator="{ props }">
                    <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props" size="small">
                        <v-icon icon="mdi-plus"></v-icon> 
                        Add New Group
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
                        <h6 class="text-subtitle-1 text-medium-emphasis pl-3"> Group Name</h6>
                        <v-col cols="12" sm="6" md="12">
                        <v-text-field
                            v-model="editedItem.name"
                            variant="outlined"
                        ></v-text-field>
                        </v-col>
                        <v-col v-if="rolesList">
                        <h6 class="text-subtitle-1 text-medium-emphasis pl-1"> Roles</h6>
                            <div class="d-flex flex-column ml-n1">
                            <v-checkbox
                                v-for="role in rolesList"
                                :key="role.id" 
                                v-model="editedItem.roles"
                                :label="role.name"
                                hide-details
                                :value=role
                                class="my-checkbox"
                            ></v-checkbox> 
                            </div>
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
                <v-card-title class="text-h6 text-wrap pl-4 pt-4"> Delete Group</v-card-title>
                <v-divider />
                <v-card-text class="">
                    <v-container>
                    <v-row>
                        <v-col cols="12" sm="6" md="12">
                        <h6 class="text-subtitle-1 text-medium-emphasis text-center"> Are you sure you want to delete group <strong> {{editedItem.name}} </strong>? </h6>
                        </v-col>
                    </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions class="pb-10 mt-n5">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" class="mr-2" variant="outlined" @click="closeDelete">Cancel</v-btn>
                    <v-btn elevation="0" rounded="md" class="bg-red"  @click="deleteItemConfirm(editedItem.id)">
                        Delete
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
            <v-btn
            color="primary"
            @click="initialize"
            >
            Reset
            </v-btn>
        </template>
        <template #bottom></template>
    </v-data-table>
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import { useGroupStore } from '@/store/group.store';
import {useRoleStore} from "@/store/role.store";
import cloneDeep from 'lodash/cloneDeep';
import {
  useAddRoleToGroup,
  useCreateGroup,
  useDeleteGroup,
  useEditGroup,
  useRemoveRoleFromGroup,
} from "@/composables/admin/useGroupActions.js";



const roleStore = useRoleStore()
const groupStore = useGroupStore()
const dialog = ref(false)
const dialogDelete = ref(false)
const rolesList=ref([])
const isLoading = ref(false)
const headers = ref([
  {
    title: 'Group Name',
    align: 'start',
    sortable: false,
    key: 'name',
    width : "35%"
  },
  { title: 'Roles', key: 'role',  sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, width:"" },
])

const groups = ref([])
const editedIndex = ref(-1)

const editedItem = ref({
  name: '',
  roles: [],
})
const defaultItem = ref({
  name: '',
  roles : [],
})
const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Create New  Group' : 'Edit Item'
})
async function initialize () {
  isLoading.value=true
  await roleStore.getRoles()
  await groupStore.getGroups()
  rolesList.value = roleStore.roles
  groups.value =groupStore.groups
  isLoading.value=false
}

function editItem (item) {
  editedIndex.value = groups.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

function deleteItem (item) {

  editedIndex.value = groups.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

async function deleteItemConfirm (group_id) { 
  const {error, success, loading } = await useDeleteGroup(group_id)

  if(loading.value){
    isLoading.value = loading
  }

  if(success.value){
    groups.value.splice(editedIndex.value, 1)
    isLoading.value = loading.value
    closeDelete()
  }
}

function close () {
  dialog.value = false
  nextTick(() => {
    editedItem.value = Object.assign({}, defaultItem.value)
    editedIndex.value = -1
  })
}

async function closeDelete () {
  dialogDelete.value = false
  await nextTick()
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

async function save () {
  const isEditing = editedIndex.value > -1;
  const apiFunction = isEditing ? useEditGroup : useCreateGroup;
  const apiPayload = editedItem.value;

 
    let apiResponse;
    if(isEditing){

    //   if(roles.value[editedIndex.value].name !== editItem.value.name){
    //     apiResponse = await apiFunction(editedItem.value.id, payload)
    //   }
      isLoading.value = true
      const removedRoles = groups.value[editedIndex.value].roles.filter((role) => !editedItem.value.roles.includes(role));
      const addedRoles = editedItem.value.roles.filter((role) => !groups.value[editedIndex.value].roles.includes(role));

      
      // if(removedRoles){
      //   removedRoles.forEach(async (role) =>{
      //     console.log('counting')
      //     const {group, loading, success, error } =  await useRemoveRoleFromGroup(editedItem.value.id, role.id);
      //     if(error){
      //       isLoading.value= false
      //     }
      //   })
      // }

      // if(addedRoles){
      //   addedRoles.forEach(async (role)=>{
      //     console.log('counting')
      //     const {group, loading, success, error } =  await useAddRoleToGroup(editedItem.value.id, role.id);
      //     if(error){
      //       loading.value = false
      //     }
      //   })
      // }

      const removeRolePromises = removedRoles.map(async (role) => {
      const { group, loading, success, error } = await useRemoveRoleFromGroup(
        editedItem.value.id,
        role.id
      );
      if (error) {
        isLoading.value = false;
      }
      return { group, loading, success, error };
    });

    // Create an array of promises for added roles
    const addRolePromises = addedRoles.map(async (role) => {
      const { group, loading, success, error } = await useAddRoleToGroup(
        editedItem.value.id,
        role.id
      );
      if (error) {
        isLoading.value = false;
      }
      return { group, loading, success, error };
    });

    // Wait for all removeRolePromises and addRolePromises to complete
    const [removeRoleResults, addRoleResults] = await Promise.all([
      Promise.all(removeRolePromises),
      Promise.all(addRolePromises),
    ]);

      apiResponse = await apiFunction(editedItem.value.id, apiPayload)
      


    } else {
      apiResponse = await apiFunction(apiPayload);
    }

    const { group, loading, success, error } = apiResponse;
      loading.value && (isLoading.value = loading.value);
      const deepCopiedGroup = cloneDeep(group.value);

      if (success.value) {
          if (isEditing) {
           console.log(group.value)
              Object.assign(groups.value[editedIndex.value], deepCopiedGroup);
              isLoading.value=false
          } else {
              group.value.push(group.value);
              isLoading.value=false
          }
          close();
          // location.reload()
          
          console.log(groups.value[editedIndex.value])
      }
  
  

//   if (editedIndex.value > -1) {
    

//     removedRoles.forEach((role)=>{
//       console.log(role.id)
//     })
//     console.log(removedRoles)
//     console.log(addedRoles)
//     Object.assign(roles.value[editedIndex.value], editedItem.value)
//   } else {
//     roles.value.push(editedItem.value)
//   }
//   close()
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