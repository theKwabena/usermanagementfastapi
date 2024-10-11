import axios from 'axios'
import {ref} from 'vue'


import { createRole, deleteRole, editRole } from '../useAPI';


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;


export async function useCreateRole(payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const role = ref(null);

    try {
        loading.value = true;
        const response = await createRole(payload);
        role.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : e;
    } finally {
        loading.value = false;
    }
    return { error, success, loading, role };
}


export async function useDeleteRole(group_id) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);

    try {
        loading.value = true;
        await deleteRole(group_id);
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading };
}

export async function useEditRole(group_id, payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const role = ref(null);

    try {
        loading.value = true;
        const response = await editRole(group_id, payload);
        role.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, role };
}


export async function useAddRoleToGroup(group_id, role_id) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const group = ref(null);

    try {
        loading.value = true;
        const response = await addRoleToGroup(group_id, role_id);
        group.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, user };
}


export async function useRemoveRoleFromGroup(group_id, role_id) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const group = ref(null);

    try {
        loading.value = true;
        const response = await removeRoleFromGroup(group_id, role_id);
        group.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, user };
}









