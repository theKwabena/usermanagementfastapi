import { useAuthStore } from "@/store/auth.store"

 

function AdminRoute(to, from,next){
    const user = useAuthStore().user
    const  admin = user.groups.find((group) => group.name == 'admin')

    if(admin){
        next()
    } else {
        return 
    }
}


export {
    AdminRoute
}