import { computed } from 'vue';
import { useAuthStore } from '@/store/auth.store';
// Replace 'currentUser' with your actual user data
const currentUser = useAuthStore().user

// Composable function to check permissions
export const usePermissions = (permission) => {
   
    const hasRoleInRoles = currentUser.roles.some((role) => role.name === permission);
    const hasRoleInGroups = currentUser.groups.some((group) =>
        group.roles.some((role) => role.name === permission)
    );
    const isSuperUser = currentUser.is_superuser;

    return hasRoleInRoles || hasRoleInGroups || isSuperUser;
};


export const useSuperUser = ()=>{
    return currentUser.is_superuser
}
// Usage of composable functions

