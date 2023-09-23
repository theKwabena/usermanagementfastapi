// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'

import { AdminRoute  } from './permissions'
import { loadGroup } from './fetchData'
import Cookies from 'js-cookie'
import { useUserStore } from '@/store/user.store'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/oldlayour/Default.vue'),
    children: [
      {
        path: '',
        name: 'home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
        meta : {
          requiresAuth : true
        }
      },
      {
        path : '/edit-profile',
        name : 'edit-profile',
        component : ()=> import("@/views/EditProfile.vue")
      },
      {
        path : '/login',
        name : 'login',
        component : ()=> import("@/views/LoginView.vue")


      },
      {
        path : '/register',
        name : 'register',
        component : ()=> import("@/views/RegisterView.vue")


      }
    ],
  },

  {
    path : "/admin",
    name: 'admin', 
    component :  () => import('@/layouts/default/AdminView.vue'),
    children : [
      {
        path : 'users',
        name : 'admin-home',
        component: ()=> import("@/views/Admin/AdminDashboard.vue"),
        beforeEnter : [AdminRoute]
      },
      {
        path :'edit',
        name : 'admin-edit',
        component: ()=> import ("@/views/Admin/EditUser.vue"),
        beforeEnter : [AdminRoute ]
      },
      {
        path : "groups",
        name : 'admin-groups',
        component: ()=> import ("@/views/Admin/GroupsView.vue"),
        // beforeEnter : [loadGroup]
      },
      {
        path : 'roles',
        name : 'admin-roles',
        component : ()=>import("@/views/Admin/RolesView.vue")
      }
    ],
    beforeEnter: [AdminRoute]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

// router.beforeResolve(async (to) => {
//   console.log('goung ssome')
//   if (to.name === 'admin-groups') {
//     console.log('coming in')
//     loadGroup()
//   }
//   if (to.name === 'admin-home') {
//     const user = useUserStore()
//     await user.getUsers()
//   }
// })

router.beforeEach(async (to, from, next)=>{
  if (to.meta.requiresAuth){

    const user = useAuthStore().user
    const authenticated = Cookies.get('is_Authenticated')

    if (!authenticated){
      return next({path : '/login'})
    } 
    else {
      if(!user){
        await auth.getUserProfile()
        if (!user){
          return next({path: '/login'})
        }
       
      }
    }
  }

  return next();
})
export default router
