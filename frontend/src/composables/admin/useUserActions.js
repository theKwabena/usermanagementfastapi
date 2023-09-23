import axios from 'axios'
import {ref} from 'vue'


import { createUser, deleteUser, editUser } from '../useAPI';


const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;


export async function useCreateUser(payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const user = ref(null);

    try {
        loading.value = true;
        const response = await createUser(payload);
        user.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, user };
}


export async function useDeleteUser(user_id) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);

    try {
        loading.value = true;
        await deleteUser(user_id);
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading };
}

export async function useEditUser(user_id, payload) {
    const error = ref(null);
    const success = ref(null);
    const loading = ref(false);
    const user = ref(null);

    try {
        loading.value = true;
        const response = await editUser(user_id, payload);
        user.value = response.data;
        success.value = true;
    } catch (e) {
        error.value = e.response ? e.response.data.detail : 'Network error';
    } finally {
        loading.value = false;
    }

    return { error, success, loading, user };
}








