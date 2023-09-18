// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/oldlayour/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
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
        component: ()=> import("@/views/Admin/AdminDashboard.vue")
      },
      {
        path :'edit',
        name : 'admin-edit',
        component: ()=> import ("@/views/Admin/EditUser.vue")
      },
      {
        path : "groups",
        name : 'admin-groups',
        component: ()=> import ("@/views/Admin/GroupsView.vue")
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
