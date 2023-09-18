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
                      
                    <v-toolbar-title class="">Groups</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="500px" persistent>
                      <template v-slot:activator="{ props }">
                          <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props">
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
                              <v-col>
                                <h6 class="text-subtitle-1 text-medium-emphasis pl-1"> Roles</h6>
                                  <div class="d-flex ml-n1">
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
                          <v-btn elevation="0" rounded="md" class="bg-red"  @click="deleteItemConfirm">
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
  import { computed, nextTick, ref, watch } from 'vue'

  const dialog = ref(false)
  const dialogDelete = ref(false)
  const rolesList=ref([
    {
    name : "Admin Create",
    id : 2,
    },
    {
    name : "Admin Edit",
    id : 3,
    },
  {
    name : "Admin Delete",
    id : 4,
    }
  ])
  const headers = ref([
    {
      title: 'Group Name',
      align: 'start',
      sortable: false,
      key: 'name',
      width : "35%"
    },
    { title: 'Roles', key: 'role' },
    { title: 'Actions', key: 'actions', sortable: false, width:"" },
  ])
  const desserts = ref([])
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
  function initialize () {
    desserts.value = [
      {
        name: 'Admin',
        roles : [
        {
          name : "Admin Create",
          id : 2,
        },
        {
          name : "Admin Edit",
          id : 3,
        },
        {
          name : "Admin Delete",
          id : 4,
        }
        ]
      },

      {
        name: 'Admin',
        roles : [
        {
          name : "Admin Create",
          id : 2,
        },
        {
          name : "Admin Edit",
          id : 3,
        },
        {
          name : "Admin Delete",
          id : 4,
        }
        ]
      },
      
    ]
  }
  function editItem (item) {
    console.log(item.roles)
    editedIndex.value = desserts.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    console.log(editedItem.value.roles)
    dialog.value = true
  }
  function deleteItem (item) {
    editedIndex.value = desserts.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    dialogDelete.value = true
  }
  function deleteItemConfirm () {
    desserts.value.splice(editedIndex.value, 1)
    closeDelete()
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
    await this.$nextTick();
    editedItem.value = Object.assign({}, defaultItem.value)
    editedIndex.value = -1
  
  }
  function save () {
    if (editedIndex.value > -1) {
      Object.assign(desserts.value[editedIndex.value], editedItem.value)
    } else {
      desserts.value.push(editedItem.value)
    }
    close()
  }
  watch(dialog, val => {
    val || close()
  })
  watch(dialogDelete, val => {
    val || closeDelete()
  })
  initialize()

  console.log(editedItem.value.roles)
</script>

<style scoped lang="scss">
 
</style>