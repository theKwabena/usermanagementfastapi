<template>
    <div class="pa-16">
        <v-row class="d-flex align-center justify-center">
          <v-col cols="12" class="border-sm rounded-lg" v-if="is_superuser">
              <v-data-table
                :headers="_headers"
                :loading="isLoading"
                :items="users"
                :sort-by="[{ key: 'name', order: 'asc' }]"
                class="px-8 text-apptext"
              >

                <template v-slot:top>
                  <v-toolbar flat class="bg-white">
                      
                    <!-- <v-toolbar-title class="">Users</v-toolbar-title> -->
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="800px" persistent v-if="canCreate">
                      <template v-slot:activator="{ props }">
                          <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props">
                              <v-icon icon="mdi-plus"></v-icon> 
                              Add New User
                          </v-btn>
                      </template>

                      <v-card>
                        <form>
                            <v-card-title class="pl-10">
                          <span class="text-h6">{{ formTitle }}</span>
                        </v-card-title>
                        <v-divider />
                        <!-- <v-card-subtitle class="text-center pt-4 text-red" v-show="create_error" >{{ create_error }}</v-card-subtitle> -->
                        <v-card-text class="mt-n4">
                          <v-container>
                            <v-row>
                                <v-col cols="12" sm="12" md="6">
                                <h6 class="text-subtitle-1 text-medium-emphasis"> First Name</h6>
                                <v-text-field
                                  :error-messages="v$.first_name.$errors.map(e => e.$message)"
                                  v-model="editedUser.first_name"
                                  variant="outlined"
                                  
                                ></v-text-field>
                                </v-col> 
                                <v-col cols="6" sm="12" md="6">
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
                                
                            </v-row>
                            <v-row class="">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Email</h6>
                                <v-text-field
                                  v-model="editedUser.email"
                                  :error-messages="v$.email.$errors.map(e => e.$message)"
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
                            <v-row v-if="password_input">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Password</h6>
                                <v-text-field
                                  v-model="editedUser.password"
                                  :error-messages="v$.password.$errors.map(e => e.$message)"
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>

                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Confirm Password</h6>
                                <v-text-field
                                  v-model="editedUser.confirm_password"
                                  :error-messages="v$.confirm_password.$errors.map(e => e.$message)"
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row v-show="is_superuser">
                              <v-col v-if="rolesList">
                                <v-divider class="w-100"/>
                                <h6 class="text-subtitle-1 text-medium-emphasis pl-1 py-2"> Roles</h6>
                                <v-divider/>
                                  <div class="d-flex justify-lg-space-around ml-n1">
                                  <v-checkbox
                                      v-for="role in rolesList"
                                      :key="role.id" 
                                      v-model="editedUser.roles"
                                      :label="role.name"
                                      hide-details
                                      :value=role
                                      class="my-checkbox"
                                  ></v-checkbox> 
                                  </div>
                              </v-col>
                            </v-row>
                            <v-row v-show="is_superuser">
                              <v-col v-if="groupsList">
                                <v-divider />
                                <h6 class="text-subtitle-1 text-medium-emphasis pl-1 py-2"> Groups</h6>
                                <v-divider />
                                  <div class="d-flex flex-column ml-n1">
                                        <v-checkbox
                                            v-for="group in groupsList"
                                            :key="group.id" 
                                            v-model="editedUser.groups"
                                            :label="group.name"
                                            hide-details
                                            :value=group
                                            class=""
                                        ></v-checkbox>
                                  </div>
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
                          <v-btn elevation="0" rounded="md" class="bg-red px-4" :loading="isLoading"  @click="deleteUserConfirm(editedUser.id)">
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
                <template v-slot:item.roles="{ item }">
                          <div class="py-2">
                          <div v-for="role in item.raw.roles" :key="role.id">
                              <p> {{role.name}}mmm</p>
                          </div>
                          </div>
                </template>
                <template v-slot:item.groups="{ item }">   
                    <div class="py-2">
                    <div v-for="group in item.raw.groups" :key="group.id">
                        <p> {{group.name}}</p>
                    </div>
                    </div>
                </template>
                <template v-slot:item.actions="{ item }">
                  <p v-if="!canCreate && !canEdit && !canDelete"> None</p>
                  <v-icon
                  v-show="canEdit"
                    size="small"
                    class="me-4"
                    @click="editUser(item.raw)"
                  >
                  mdi-square-edit-outline
                  </v-icon>

                  <v-icon
                  v-show="canDelete"
                    size="small"
                    @click="deleteUser(item.raw)"
                  >
                    mdi-delete
                  </v-icon>
                </template>
                <!-- <template v-slot:no-data>
                  <v-btn
                    color="primary"
                    @click="initialize"
                  >
                    Reset
                  </v-btn>
                </template> -->

                <template v-slot:bottom>
                <div class="text-center ml-n16 mr-16 pt-10">
                  <!-- <v-pagination
                    v-model="page"
                    :length="pageCount"
                  ></v-pagination> -->
                </div>
                </template>
              </v-data-table>
          </v-col>
          <v-col cols="12" class="border-sm rounded-lg" v-if="!is_superuser">
              <v-data-table
                
                :headers="headers"
                :items="users"
                :sort-by="[{ key: 'name', order: 'asc' }]"
                class="px-8 text-apptext"
              >

                <template v-slot:top>
                  <v-toolbar flat class="bg-white">
                      
                    <!-- <v-toolbar-title class="">Users</v-toolbar-title> -->
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="800px" persistent v-if="canCreate || canEdit">
                      <template v-slot:activator="{ props }">
                          <v-btn elevation="0" rounded="xs" class="bg-primary" v-bind="props">
                              <v-icon icon="mdi-plus"></v-icon> 
                              Add New User
                          </v-btn>
                      </template>

                      <v-card>
                        <form>
                            <v-card-title class="pl-10">
                          <span class="text-h6">{{ formTitle }}</span>
                        </v-card-title>
                        <v-divider />
                        <!-- <v-card-subtitle class="text-center pt-4 text-red" v-show="create_error" >{{ create_error }}</v-card-subtitle> -->
                        <v-card-text class="mt-n4">
                          <v-container>
                            <v-row>
                                <v-col cols="12" sm="12" md="6">
                                <h6 class="text-subtitle-1 text-medium-emphasis"> First Name</h6>
                                <v-text-field
                                  :error-messages="v$.first_name.$errors.map(e => e.$message)"
                                  v-model="editedUser.first_name"
                                  variant="outlined"
                                  
                                ></v-text-field>
                                </v-col> 
                                <v-col cols="6" sm="12" md="6">
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
                                
                            </v-row>
                            <v-row class="">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Email</h6>
                                <v-text-field
                                  v-model="editedUser.email"
                                  :error-messages="v$.email.$errors.map(e => e.$message)"
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
                            <v-row v-if="password_input" class="">
                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Password</h6>
                                <v-text-field
                                  v-model="editedUser.password"
                                  :error-messages="v$.password.$errors.map(e => e.$message)"
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>

                                <v-col>
                                    <h6 class="text-subtitle-1 text-medium-emphasis"> Confirm Password</h6>
                                <v-text-field
                                  v-model="editedUser.confirm_password"
                                  
                                  variant="outlined"
                                ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row v-show="is_superuser">
                              <v-col v-if="rolesList">
                                <v-divider class="w-100"/>
                                <h6 class="text-subtitle-1 text-medium-emphasis pl-1 py-2"> Roles</h6>
                                <v-divider/>
                                  <div class="d-flex justify-lg-space-around ml-n1">
                                  <v-checkbox
                                      v-for="role in rolesList"
                                      :key="role.id" 
                                      v-model="editedUser.roles"
                                      :label="role.name"
                                      hide-details
                                      :value=role
                                      class="my-checkbox"
                                  ></v-checkbox> 
                                  </div>
                              </v-col>
                            </v-row>
                            <v-row v-show="is_superuser">
                              <v-col v-if="groupsList">
                                <v-divider />
                                <h6 class="text-subtitle-1 text-medium-emphasis pl-1 py-2"> Groups</h6>
                                <v-divider />
                                  <div class="d-flex flex-column ml-n1">
                                        <v-checkbox
                                            v-for="group in groupsList"
                                            :key="group.id" 
                                            v-model="editedUser.groups"
                                            :label="group.name"
                                            hide-details
                                            :value=group
                                            class=""
                                        ></v-checkbox>
                                  </div>
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
                          <v-btn elevation="0" rounded="md" class="bg-red px-4" :loading="isLoading"  @click="deleteUserConfirm(editedUser.id)">
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
                <template v-slot:item.roles="{ item }">
                          <div class="py-2">
                          <div v-for="role in item.raw.roles" :key="role.id">
                              <p> {{role.name}}</p>
                          </div>
                          </div>
                </template>
                <template v-slot:item.groups="{ item }">   
                    <div class="py-2">
                    <div v-for="group in item.raw.groups" :key="group.id">
                        <p> {{group.name}}</p>
                    </div>
                    </div>
                </template>
                <template v-slot:item.actions="{ item }">
                  <p v-if=" !canEdit && !canDelete"> None</p>
                  <v-icon
                  v-show="canEdit"
                    size="small"
                    class="me-4"
                    @click="editUser(item.raw)"
                  >
                  mdi-square-edit-outline
                  </v-icon>

                  <v-icon
                  v-show="canDelete"
                    size="small"
                    @click="deleteUser(item.raw)"
                  >
                    mdi-delete
                  </v-icon>
                </template>
              

                <template v-slot:bottom>
                <div class="text-center ml-n16 mr-16 pt-10">
                  <!-- <v-pagination
                    v-model="page"
                    :length="pageCount"
                  ></v-pagination> -->
                </div>
                </template>
              </v-data-table>
          </v-col>
        </v-row>
     </div>
  </template>
  <script setup>
  import { computed, onMounted, ref, watch, nextTick } from 'vue'
  import { useVuelidate } from '@vuelidate/core'
  import { email, required, helpers, minLength, sameAs } from '@vuelidate/validators'
  import { useUserStore } from '@/store/user.store';
  import {useDeleteUser, useCreateUser,
     useEditUser, useAddUserToGroup, 
     useAddRoleToUser, useRemoveUserFromGroup,
     useRemoveRoleFromUser} from "@/composables/admin/useUserActions.js"

  import {usePermissions, useSuperUser} from "@/composables/admin/usePermissions"
  import { useGroupStore } from '@/store/group.store';
  import {useRoleStore} from "@/store/role.store";
  
 
  const is_superuser = useSuperUser()
  // console.log(is_superuser)
  const user = useUserStore()
  const roleStore = useRoleStore()
  const groupStore = useGroupStore()
  const dialog = ref(false)
  const dialogDelete = ref(false)
  const $externalResults = ref({})

  const canCreate = usePermissions('admin_create_users');
  const canDelete = usePermissions('admin_delete_users');
  const canEdit = usePermissions('admin_edit_users');
  

  const isLoading = ref(false)

  const users = ref([])
  const rolesList=ref([])
  const groupsList=ref([])

  const headers = ref([
    {
      title: 'User',
      align: 'start',
      key: 'first_name',
      width : "50%"
    },
    { title: 'Email', key: 'email',width:"50%"},
    { title: 'Actions', key: 'actions', sortable: false, width:"140px" },
  ])

  //headers for superusertable
  const _headers = ref([
    {
      title: 'User',
      align: 'start',
      key: 'first_name',
      width : "25%"
    },
    { title: 'Email', key: 'email',width:"25%"},
    { title: 'Roles', key: 'roles', width:"20%", show : is_superuser},
    { title: 'Groups', key: 'groups', width: "20%", show : is_superuser },
    { title: 'Actions', key: 'actions', sortable: false, width:"140px" },
  ])

  const editedIndex = ref(-1)

  const editedUser = ref({
    id : '',
    first_name : '',
    last_name : '',
    email : '',
    phone_number : '',
    groups : [],
    roles: [],
    password : '',
    confirm_password : '',
  })

  const defaultItem = ref({
    id: '',
    irst_name : '',
    last_name : '',
    email : '',
    phone_number : '',
    groups : [],
    roles : [],
  })

  const password1Ref = computed(() => editedUser.value.password);
  const password2Ref = computed(() => editedUser.value.confirm_password);

  const rules = {
    first_name: { 
        required: helpers.withMessage('First name cannot be empty', required),
        minLength : minLength(2)
     },
    last_name: { 
        required : helpers.withMessage('Last name cannot be empty', required),
        minLength : minLength(2)
    },

    email : {required : helpers.withMessage("Please enter email", required), 
          email},

    password : {
        required : helpers.withMessage("Please enter password", required),
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password2Ref)
        ),
    },
    confirm_password : {
        sameAsPassword: helpers.withMessage(
        "The two fields do not match.",
        sameAs(password1Ref)
        ),
    }
    
  }

  const v$ = useVuelidate(rules, editedUser, {$externalResults})

  const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Add New  User' : 'Edit User'
  })

  const password_input = computed(()=>{
    return editedIndex.value === -1? true : false
  })

  async function initialize () {
    isLoading.value = true
    await roleStore.getRoles()
    await groupStore.getGroups()
    rolesList.value = roleStore.roles
    groupsList.value = groupStore.groups
    users.value = user.users
    isLoading.value= false
  }


  function clear () {
    v$.value.$reset()

    for (const [key, value] of Object.entries(editedUser)) {
      editedUser[key] = value
    }
  }

  function editUser (user) {
    editedIndex.value = users.value.indexOf(user)
    editedUser.value = Object.assign({}, user)
    dialog.value = true
  }

  async function deleteUser (user) {
    editedIndex.value = users.value.indexOf(user)
    editedUser.value = Object.assign({}, user)
    dialogDelete.value = true
  }

  async function deleteUserConfirm (user_id) {
    const {error, success, loading } = await useDeleteUser(user_id)

    if(loading.value){
      isLoading.value = loading
    }

    if(success.value){
      users.value.splice(editedIndex.value, 1)
      isLoading.value = loading.value
      closeDelete()
    }

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

  async function save() {
    console.log('saving')
    v$.value.$clearExternalResults();

    // if (!(await v$.value.$validate())) return;

    const isEditing = editedIndex.value > -1;
    const apiFunction = isEditing ? useEditUser : useCreateUser;
    const apiPayload = editedUser.value;

    isEditing ? undefined : delete apiPayload.id
    
    try {

      let apiResponse;
      if (isEditing) {
        console.log('saving')
            // Get added and removed roles
            const removedRoles = users.value[editedIndex.value].roles.filter((role) => !editedUser.value.roles.includes(role));
            const addedRoles = editedUser.value.roles.filter((role) => !users.value[editedIndex.value].roles.includes(role));

            //Get added and removed groups and added them to the user
            const removedGroups = users.value[editedIndex.value].groups.filter((group) => !editedUser.value.groups.includes(group));
            const addedGroups = editedUser.value.groups.filter((group) => !users.value[editedIndex.value].groups.includes(group));


            const addRolePromises = addedRoles.map(async (role) => {
              const {user, loading, success, error } = await useAddRoleToUser(editedUser.value.id, role.id)
              if (error) {
                isLoading.value = false;
              }
            })

            const removeRolePromises = removedRoles.map(async (role) => {
              const {user, loading, success, error } = await useRemoveRoleFromUser(editedUser.value.id, role.id)
              if (error) {
                isLoading.value = false;
              }
            })


            const addGroupPromises = addedGroups.map(async (group) => {
              console.log("adding")
              const {user, loading, success, error } = await useAddUserToGroup(editedUser.value.id, group.id)
              if (error) {
                isLoading.value = false;
              }
            })

            const removeGroupPromises = removedGroups.map(async (group) => {
              const {user, loading, success, error } = await useRemoveUserFromGroup(editedUser.value.id, group.id)
              if (error) {
                isLoading.value = false;
              }
            })

            const [removeRoleResults, addRoleResults, removeGroupResults, addGroupResults] = await Promise.all([
              Promise.all(removeRolePromises),
              Promise.all(addRolePromises),
              Promise.all(addGroupPromises),
              Promise.all(removeGroupPromises),
            ]);

            console.log('here')
            apiResponse = await apiFunction(editedUser.value.id, apiPayload);

        } else {
            // Send the request with the complete payload when creating
            apiResponse = await apiFunction(apiPayload);

            //Create added roles and groups


        }


        const { user, loading, success, error } = apiResponse;
       

        loading.value && (isLoading.value = loading.value);

        if (success.value) {
            if (isEditing) {
                Object.assign(users.value[editedIndex.value], user.value);
            } else {
                apiPayload.roles.forEach(async (role)=>{
                  await useAddRoleToUser(user.value.id, role.id)
                })

                apiPayload.groups.forEach(async (group)=>{
                  await useAddUserToGroup(user.value.id, group.id)
                })
                users.value.push(user.value);
                location.reload()
            }
            close()
        }

        if (error.value && error.value.includes('email')) {
            $externalResults.value = { email: [error.value] };
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

  onMounted(async ()=>{
    await user.getUsers()
    initialize()
    console.log(users.value)
  })
</script>

<style scoped lang="scss">
 
</style>