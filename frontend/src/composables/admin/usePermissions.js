import { computed } from 'vue';
import { useAuthStore } from '@/store/auth.store';

const currentUser = useAuthStore().user

// Composable function to check permissions


export const usePermissions = (permission) => {
    const currentUser = useAuthStore().user;
  
    // Use computed properties to calculate the permission checks
    const hasRoleInRoles = computed(() =>
      currentUser.roles.some((role) => role.name === permission)
    );
  
    const hasRoleInGroups = computed(() =>
      currentUser.groups.some((group) =>
        group.roles.some((role) => role.name === permission)
      )
    );
  
    const isSuperUser = computed(() => currentUser.is_superuser);
  
    // Use another computed property to combine the checks
    const hasPermission = computed(() =>
      hasRoleInRoles.value || hasRoleInGroups.value || isSuperUser.value
    );
  
    return hasPermission;
  };

export const useSuperUser = ()=>{
    return currentUser.is_superuser
}
// Usage of composable functions

// export const usePermissions = (permission) => {
   
//     const hasRoleInRoles = currentUser.roles.some((role) => role.name === permission);
//     const hasRoleInGroups = currentUser.groups.some((group) =>
//         group.roles.some((role) => role.name === permission)
//     );
//     const isSuperUser = currentUser.is_superuser;

//     return hasRoleInRoles || hasRoleInGroups || isSuperUser;
// };