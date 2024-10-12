// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'

// import { AdminRoute  } from './permissions's
// import { loadGroup } from './fetchData'
import Cookies from 'js-cookie' 
// import { useUserStore } from '@/store/user.store'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/Default.vue'),
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
      },

      {
        path : '/verify-email/:email_token/',
        name : 'verify-email',
        component : ()=> import("@/views/VerifyEmail.vue")
      },

      {
        path : '/forgot-password',
        name : 'forgot-password',
        component : ()=> import("@/views/ForgotPasswordView.vue")
      },

      {
        path: '/reset-password/:email_token',
        name : 'reset-password',
        component : ()=> import("@/views/ResetPasswordView.vue")
      }
    ],
  },

  {
    path : "/admin",
    name: 'admin', 
    component :  () => import('@/layouts/default/AdminView.vue'),
    children : [
      // {
        
      //   path : '',
      //   name : 'admin-home',
      //   component: ()=> import("@/views/Admin/AdminDashboard.vue"),
        
      // },
      {
        
        path : '',
        name : 'admin-users',
        component: ()=> import("@/views/Admin/UsersView.vue"),
        
      },
      {
        path :'edit',
        name : 'admin-edit',
        component: ()=> import ("@/views/Admin/EditUser.vue"),
        // beforeEnter : [AdminRoute ]
      },
      {
        path : "permissions",
        name : 'admin-permissions',
        component: ()=> import ("@/views/Admin/GroupsView.vue"),
        // beforeEnter : [loadGroup]
      },
      {
        path : 'roles',
        name : 'admin-roles',
        component : ()=>import("@/views/Admin/RolesView.vue")
      }
    ],
    meta : {
      requiresAuth : true
    }
    // beforeEnter: [AdminRoute]
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
    const authStore = useAuthStore()
    const authenticated = Cookies.get('is_Authenticated')
    const user = authStore.user
    if (!authenticated){
      return next({path : '/login'})
    }

    else {
      if(!user){
        await authStore.getUserProfile()
        if(!authStore.ready){
          return next({path : '/login'})
        }
       
      }
    }
  }

  return next();
})
export default router
