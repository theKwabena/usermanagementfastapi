<template>
    <div class="pa-16">
        <v-row class="d-flex align-center justify-center">
          <v-col cols="12">
              <v-data-table
                :headers="headers"
                :items="desserts"
                :sort-by="[{ key: 'calories', order: 'asc' }]"
                class="pa-8"
              >

                <template v-slot:top>
                  <v-toolbar flat class="bg-white">
                      
                    <v-toolbar-title class="">Roles</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="500px" persistent>
                      <template v-slot:activator="{ props }">
                          <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props">
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
                                  v-model="editedItem.name"
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
               
                <template v-slot:item.actions="{ item }">
                  
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
                </template>
                <template v-slot:no-data>
                  <v-btn
                    color="primary"
                    @click="initialize"
                  >
                    Reset
                  </v-btn>
                </template>

                <template v-slot:bottom>
                <div class="text-center ml-n16 mr-16 pt-10">
                  <v-pagination
                    v-model="page"
                    :length="pageCount"
                  ></v-pagination>
                </div>
                </template>
              </v-data-table>
          </v-col>
        </v-row>
     </div>

     
  </template>
  <script setup>
  import { computed, nextTick, ref, watch, onMounted } from 'vue'
  import { useGroupStore } from '@/store/group.store';
  import {useRoleStore} from "@/store/role.store";
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
  const isLoading = ref(null)
  const headers = ref([
    {
      title: 'Name',
      align: 'start',
      sortable: false,
      key: 'name',
      width : "35%"
    },
    // { title: 'Roles', key: 'role' },
    { title: 'Actions', key: 'actions', sortable: false, },
  ])

  const desserts = ref([])
  const editedIndex = ref(-1)

  const editedItem = ref({
    name: '',
    // roles: [],
  })
  const defaultItem = ref({
    name: '',
    // roles : [],
  })
  const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Create New  Role' : 'Edit Role'
  })
  async function initialize () {

  }

  function editItem (item) {
    editedIndex.value = desserts.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    dialog.value = true
  }

  function deleteItem (item) {
    editedIndex.value = desserts.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    dialogDelete.value = true
  }

  async function deleteItemConfirm (group_id) { 
    const {error, success, loading } = await useDeleteGroup(group_id)

    if(loading.value){
      isLoading.value = loading
    }

    if(success.value){
      desserts.value.splice(editedIndex.value, 1)
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

    try {
      let apiResponse;
      if(isEditing){
      apiResponse = await apiFunction(editedItem.value.id, apiPayload)
      
      } else {
        apiResponse = await apiFunction(apiPayload);
      }

      const { group, loading, success, error } = apiResponse;
      console.log(group.value, success.value, error.value)
        loading.value && (isLoading.value = loading.value);

        if (success.value) {
            if (isEditing) {
                Object.assign(desserts.value[editedIndex.value], group.value);
            } else {
                desserts.value.push(group.value);
            }
            close();
        }
    
    } catch (e){
      console.log(e);
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

<style scoped lang="scss">
 
</style>