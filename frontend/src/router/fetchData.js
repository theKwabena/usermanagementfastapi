import { useGroupStore } from "@/store/group.store"

export async function loadGroup(to, from, next){
    console.log('loading groups')
    const groups = useGroupStore()

    await groups.getGroups()
    return true
}
