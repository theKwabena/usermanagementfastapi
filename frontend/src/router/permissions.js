import { useAuthStore } from "@/store/auth.store"

 

function AdminRoute(to, from,next){
    const user = useAuthStore().user
    if (!user){
        return {path: '/login'}
    }

    const  admin = user.groups.find((group) => group.name == 'admin')

    if(admin){
        next()
    } else {
        return {path: from.path}
    }
}


export {
    AdminRoute
}