import Cookies from 'js-cookie';

export async function deleteSession(){
    sessionStorage.clear()
    Cookies.remove('is_Authenticated')
    return true
}