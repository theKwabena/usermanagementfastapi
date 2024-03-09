import axios from 'axios'
import {ref} from 'vue'


import { createGroup, deleteGroup, editGroup, addRoleToGroup, removeRoleFromGroup } from '../useAPI';


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

 
export async function useCreateGroup(payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const group = ref(null);

    try {
        loading.value = true;
        const response = await createGroup(payload);
        group.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : e;
    } finally {
        loading.value = false;
    }
    return { error, success, loading, group };
}


export async function useDeleteGroup(group_id) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);

    try {
        loading.value = true;
        await deleteGroup(group_id);
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading };
}

export async function useEditGroup(group_id, payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const group = ref(null);

    try {
        loading.value = true;
        const response = await editGroup(group_id, payload);
        group.value = response.data;
        console.log(group.value, response.data)
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, group };
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

    return { error, success, loading, group };
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

    return { error, success, loading, group };
}









