// api.js
import axios from 'axios';

const baseUrl = `${import.meta.env.VITE_BACKEND_API_URL}`;

const config = {
    withCredentials : true,
    credentials : 'include'
}

//Users
export async function createUser(payload) {
    return axios.post(`${baseUrl}/users/`, payload, config);
}

export async function deleteUser(user_id) {
    return axios.delete(`${baseUrl}/users/${user_id}`,config);
}

export async function editUser(user_id, payload) {
    return axios.put(`${baseUrl}/users/${user_id}`, payload, config);
}

//Permissions-Role
export async function createRole(payload){
    return axios.post(`${baseUrl}/admin/roles`, payload, config)
}

export async function getRoleById(role_id){
    return axios.get(`${baseUrl}/roles/${role_id}`, config)
}

export async function deleteRole(role_id){
    return axios.delete(`${baseUrl}/admin/roles/${role_id}/`, config)
}

export async function editRole(payload){
    return axios.put(`${baseUrl}/admin/roles`, payload, config)
}

//Permissions - Group
export async function createGroup(payload){
    return axios.post(`${baseUrl}/admin/groups`, payload, config)
}

export async function deleteGroup(group_id) {
    return axios.delete(`${baseUrl}/admin/groups/${group_id}`, config);
}

export async function editGroup(group_id, payload) {
    return axios.put(`${baseUrl}/admin/groups/${group_id}`, payload, config);
}


export async function AddUserToGroup(user_id, group_id) {
    return axios.post(`${baseUrl}/users/${user_id}/groups?group_id=${group_id}`, config);
}

export async function removeUserFromGroup(user_id, group_id) {
    return axios.delete(`${baseUrl}/users/${user_id}/${user_id}/groups?group_id=${group_id}`,  config);
}


export async function addRoleToGroup(group_id, role_id) {
    return axios.post(`${baseUrl}/admin/groups/${group_id}/roles?role_id=${role_id}`, config);
}

export async function removeRoleFromGroup(group_id, role_id) {
    return axios.delete(`${baseUrl}/admin/groups/${group_id}/roles?role_id=${role_id}`, config);
}


