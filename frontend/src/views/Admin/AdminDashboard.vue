<template>
    <div class="pa-16">
        <v-row class="d-flex align-center justify-center">
          <v-col cols="12">
              <v-data-table
                :headers="headers"
                :items="users"
                :sort-by="[{ key: 'name', order: 'asc' }]"
                class="pa-8"
              >

                <template v-slot:top>
                  <v-toolbar flat class="bg-white">
                      
                    <v-toolbar-title class="">Users</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="800px" persistent>
                      <template v-slot:activator="{ props }">
                          <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props">
                              <v-icon icon="mdi-plus"></v-icon> 
                              Add New User
                          </v-btn>
                      </template>
                      <v-card>
                        <form>
                            <v-card-title class="pl-10 pt-4">
                          <span class="text-h6">{{ formTitle }}</span>
                        </v-card-title>
                        <v-divider />
                        <v-card-text class="mt-n4">
                          <v-container>
                            <v-row>
                                <v-col cols="12" sm="12" md="12">
                                <h6 class="text-subtitle-1 text-medium-emphasis"> First Name</h6>
                                <v-text-field
                                  :error-messages="v$.first_name.$errors.map(e => e.$message)"
                                  v-model="editedUser.first_name"
                                  variant="outlined"
                                  
                                ></v-text-field>
                                </v-col> 
                            </v-row>
                            <v-row class="">
                                <v-col cols="12" sm="12" md="12">
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Last Name</h6>
                                <v-text-field
                                  v-model="editedUser.last_name"
                                  :error-messages="v$.last_name.$errors.map(e => e.$message)"
                                  variant="outlined"
                                  required
                                ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row class="">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Email</h6>
                                <v-text-field
                                  v-model="editedUser.email"
                                  :error-messages="v$.email.$errors.map(e => e.$message)"
                                  @input="v$.email.$touch"
                                  @blur="v$.email.$touch"
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>

                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Phone Number</h6>
                                <v-text-field
                                  v-model="editedUser.phone_number"
                                  
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>
                                
                            </v-row>
                            
                          </v-container>
                        </v-card-text>
            
                        <v-card-actions class="mt-n6 pb-6">
                          <v-spacer></v-spacer>
                          <v-btn  variant="outlined" elevation="0" rounded="md" @click="close">
                              Cancel
                          </v-btn>  
                          <v-btn elevation="0" rounded="md" class="bg-primary mr-4"
                            @click="save">
                              Save Changes
                          </v-btn>
                        </v-card-actions>
                        </form>
                        
                      </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialogDelete" max-width="500px" persistent>
                      <v-card>
                        <v-card-title class="text-wrap pl-4 pt-4"> Confirm Delete</v-card-title>
                        <v-divider />
                        <v-card-text class="">
                          <v-container>
                            <v-row>
                              <v-col cols="12" sm="6" md="12">
                                <h6 class="text-subtitle-1 text-medium-emphasis text-center"> Are you sure you want to  delete user <strong> {{editedUser.first_name}} </strong>? </h6>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card-text>
                        <v-card-actions class="pb-10 mt-n5">
                          <v-spacer></v-spacer>
                          <v-btn elevation="0" rounded="md" class="bg-red px-4"  @click="deleteUserConfirm">
                              Delete User
                          </v-btn>
                          <v-btn color="primary" class="mr-2" variant="outlined" @click="closeDelete">Cancel</v-btn>
                          <v-spacer></v-spacer>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-toolbar>
                </template>
                <template v-slot:item.name="{ item }">
                  <div class="py-2">
                    <!-- {{item}} -->
                    {{ formattedNames }}
                    <!-- <div v-for="role in item.raw.roles" :key="role.id">
                      <p> {{role.name}}</p>
                    </div> -->
                  </div>
                </template>
                <template v-slot:item.actions="{ item }">
                  
                  <v-icon
                    size="small"
                    class="me-4"
                    @click="editUser(item.raw)"
                  >
                  mdi-square-edit-outline
                  </v-icon>

                  <v-icon
                    size="small"
                    @click="deleteUser(item.raw)"
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
  import { useVuelidate } from '@vuelidate/core'
  import { email, required, helpers, minLength } from '@vuelidate/validators'

  const dialog = ref(false)
  const dialogDelete = ref(false)
  
  const rules = {
    first_name: { 
        required: helpers.withMessage('First name cannot be empty', required),
        minLength : minLength(2)
     },
    last_name: { 
        required : helpers.withMessage('Last name cannot be empty', required),
        minLength : minLength(2)
    },
    email: { required, email },
    
  }

  
 
  const headers = ref([
    {
      title: 'User',
      align: 'start',
      key: 'first_name',
      width : "30%"
    },
    { title: 'Email', key: 'email' },
    { title: 'Phone Number', key: 'phone',  width:"30%" },
    { title: 'Actions', key: 'actions', sortable: false, width:"140px" },
  ])
  const users = ref([])
  const editedIndex = ref(-1)

  const editedUser = ref({
    first_name : '',
    last_name : '',
    email : '',
    phone_number : ''
  })
  const defaultItem = ref({
    irst_name : '',
    last_name : '',
    email : '',
    phone_number : ''
  })

  const v$ = useVuelidate(rules, editedUser)
  const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Add New  User' : 'Edit User'
  })
  function initialize () {
    users.value = [
      {
        
        first_name: 'Emmanuel',
        last_name: 'Abbey',
       
        email : 'abbey@user.com',
        phone_number : "+233546649873"
      },
      {
        first_name: 'Mike',
        last_name: 'Abbey',
        email : 'abbey@user.com',
        phone_number : "+233546649873"
      },
      
    ]
  }

  
  const formattedNames = computed(()=>{
    return users.value;
  })

  function clear () {
    v$.value.$reset()

    for (const [key, value] of Object.entries(editedUser)) {
      editedUser[key] = value
    }
  }



  function editUser (user) {
    editedIndex.value = users.value.indexOf(user)
    editedUser.value = Object.assign({}, user)
    console.log(editedUser.value.roles)
    dialog.value = true
  }
  function deleteUser (user) {
    editedIndex.value = users.value.indexOf(user)
    editedUser.value = Object.assign({}, user)
    dialogDelete.value = true
  }
  function deleteUserConfirm () {
    users.value.splice(editedIndex.value, 1)
    closeDelete()
  }
  async function close () {
    clear()
    dialog.value = false
    await nextTick()
    editedUser.value = Object.assign({}, defaultItem.value)
    editedIndex.value = -1
  }
  async function closeDelete () {
    dialogDelete.value = false
    await nextTick()
    editedUser.value = Object.assign({}, defaultItem.value)
    editedIndex.value = -1
  
  }
 async function save () {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return
      // submit form
    if (editedIndex.value > -1) {
      Object.assign(users.value[editedIndex.value], editedUser.value)
    } else {
      users.value.push(editedUser.value)
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

  console.log(editedUser.value.roles)
</script>

<style scoped lang="scss">
 
</style>