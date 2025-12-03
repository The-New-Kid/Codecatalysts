// import { createRouter, createWebHistory } from 'vue-router'

// // Views
// import HomeView from '../views/HomeView.vue'
// import LoginView from '../views/LoginView.vue'
// import RegisterView from '../views/RegisterView.vue'
// import UserDashboard from '../views/UserDashboard.vue'
// import UserEdit from '../views/UserEdit.vue'
// import BookDarshan from '../views/Book_Darshan.vue'
// import Calander from '../views/calander.vue'
// import MobileLogin from '../views/mobile-login.vue'

// import UserEditnew from '../views/UserEditnew.vue'
// import book_darshannew from '../views/book_darshannew.vue'
// import UserDashboardnew from '../views/Userdashboardnew.vue'
// import newcalender from '../views/newcalender.vue'

// import AdminSpotDetail from '../views/admin/AdminSpotDetail.vue'
// import AdminPrivateParking from '../views/admin/AdminPrivateParking.vue'
// import AdminScanTicket from '../views/admin/AdminScanTicket.vue'
// import AdminSummary from '../views/admin/AdminSummary.vue'
// import AdminUsers from '../views/admin/AdminUsers.vue'
// import AdminLayout from '../layouts/AdminLayout.vue'
// import AdminCalendar from '../views/admin/AdminCalendar.vue'
// import AdminDashboard from '../views/admin/AdminDashboard.vue'
// import AddParkingLot from '../views/admin/AddParkingLot.vue'
// import ParkingLotList from '@/views/admin/ParkingLotList.vue'; // Adjust path as necessary

// const routes = [
//   {
//     path: '/',
//     name: 'home',
//     component: HomeView
//   },
//   {
//     path: '/login',
//     name: 'login',
//     component: LoginView
//   },
//   {
//     path: '/register',
//     name: 'register',
//     component: RegisterView
//   },
//   {
//     path: '/user/dashboard',
//     name: 'user-dashboard',
//     component: UserDashboardnew
//   },
//   {path : '/newcalender',
//     name : 'newcalender',
//     component : newcalender
//   },

//   {
//     path : '/book_darshannew',
//     name : 'book_darshannew',
//     component : book_darshannew
//   },
//   {
//     path : '/user/editnew',
//     name : 'user-editnew',
//     component : UserEditnew
//   },
//   {
//     path : '/user/edit-profile',
//     name : 'user-edit',
//     component : UserEdit
//   },
//   {
//     path : '/book-darshan',
//     name : 'book-darshan',
//     component : BookDarshan
//   },
//   {
//     path : '/calander',
//     name : 'calander',
//     component : Calander
//   },
//   {
//     path : '/mobile-login',
//     name : 'mobile-login',
//     component : MobileLogin
//   },
// {
//   path: '/user/public/:id',
//   component: { template: '<div class="p-10 text-center">Public lots page (coming soon)</div>' }
// },
// {
//   path: '/user/private/:id',
//   component: { template: '<div class="p-10 text-center">Private lots page (coming soon)</div>' }
// },
// {
//   path: '/book/:id',
//   component: { template: '<div class="p-10 text-center">Booking page (coming soon)</div>' }
// },
// {
//   path: '/book-ticket/:id',
//   component: { template: '<div class="p-10 text-center">Ticket page (coming soon)</div>' }
// },

//  //added now admin
// {
//     path: '/admin',
//     component: AdminLayout,
//     children: [
//       {
//         path: '/admin/dashboard',
//         name: 'admin-dashboard',
//         component: AdminDashboard,
        
//       },
//       {
//         path: 'spots/:id', name: 'admin-spot-detail', component: AdminSpotDetail
//       },
//       { path: 'parking-lots/add', component: AddParkingLot, name: 'admin-add-lot' },
//       { path: 'calendar', name: 'admin-calendar', component: AdminCalendar },
//       { path: 'private-parking', name: 'admin-private-parking', component: AdminPrivateParking },
//       { path: 'scan-ticket', component: AdminScanTicket, name: 'admin-scan-ticket' },
//       { path: 'analytics', component: AdminSummary, name: 'admin-summary' },
//       { path: 'users', component: AdminUsers, name: 'admin-users' }
//     ]
//   }

// ]

// const router = createRouter({
//   history: createWebHistory(), // clean URLs
//   routes
// })

// export default router


import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

// Views
import Book_aarti_Tatkal from '../views/Book_aarti_Tatkal.vue'
import Book_Darshan_Tatkal from '../views/Book_Darshan_Tatkal.vue'
import UserLayout from '../layouts/Userlayoutnew.vue'
import UserLayoutforcalender from '../layouts/userlayoutforcalender.vue'
import AccomodationFinder from '../views/AccomodationFinder.vue'
import Bookspot from '../views/book-spot.vue'
import Bookseva from '../views/Bookseva.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import UserDashboardnew from '../views/Userdashboardnew.vue'
import UserEditnew from '../views/UserEditnew.vue'
import BookDarshanNew from '../views/book_darshannew.vue'
import NewCalender from '../views/newcalender.vue'
import BookDarshan from '../views/Book_Darshan.vue'
import MobileLogin from '../views/mobile-login.vue'
import UserEdit from '../views/UserEdit.vue'
import BookAarti from '../views/Book_Aarti.vue'

// Admin Views
import AdminDarshanDetails from '../views/admin/Admin_Darshan_details.vue'
import AdminDarshanslots from '../views/admin/AdminDarshanslots.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminPrivateParking from '../views/admin/AdminPrivateParking.vue'
import AdminScanTicket from '../views/admin/AdminScanTicket.vue'
import AdminSummary from '../views/admin/AdminSummary.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'
import AdminSpotDetail from '../views/admin/AdminSpotDetail.vue'
import AddParkingLot from '../views/admin/AddParkingLot.vue'
import ParkingLotList from '../views/admin/ParkingLotList.vue'

const routes = [
  {
  path: '/user',
  component: UserLayoutforcalender,
  meta:{requiresAuth:true},
  children: [
     { 
       path: 'newcalender',
       name: 'newcalender',
       component: NewCalender 
     }]
},
    // Public routes
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/mobile-login', name: 'mobile-login', component: MobileLogin },

    // USER PROTECTED ROUTES -----------------------------

    {
    path: '/accomodation',
    name: 'AccomodationFinder',
    component: AccomodationFinder
  },
    {
        path: '/user/dashboard',
        name: 'user-dashboard',
        component: UserDashboardnew,
        meta: { requiresAuth: true }
    },
    {
        path: '/book_darshannew',
        name: 'book_darshannew',
        component: BookDarshanNew,
        meta: { requiresAuth: true }
    },
    {
        path: '/user/editnew',
        name: 'user-editnew',
        component: UserEditnew,
        meta: { requiresAuth: true }
    },
    {
        path: '/user/edit-profile',
        name: 'user-edit',
        component: UserEdit,
        meta: { requiresAuth: true }
    },
    {
        path: '/book-darshan',
        name: 'book-darshan',
        component: BookDarshan,
        meta: { requiresAuth: true }
    },
    {
        path: '/book-aarti',
        name: 'book-aarti',
        component: BookAarti,
        meta: { requiresAuth: true }
    },
    {
        path: '/book-seva',
        name: 'book-seva',
        component: Bookseva,
        meta: { requiresAuth: true }
    },
    {
        path: '/book-spot',
        name: 'book-spot',
        component: Bookspot,
        meta: { requiresAuth: true }
    },
    {
        path:'/book_darshan_tatkal',
        name:'book_darshan_tatkal',
        component:Book_Darshan_Tatkal,
        meta:{requiresAuth:true}
    },{
        path:'/book_aarti_tatkal',
        name:'book_aarti_tatkal',
        component:Book_aarti_Tatkal
    },
    // Dynamic routes still require login
    { path: '/user/public/:id', meta: { requiresAuth: true }, component: { template: '<div class="p-10 text-center">Public lots page (coming soon)</div>' }},
    { path: '/user/private/:id', meta: { requiresAuth: true }, component: { template: '<div class="p-10 text-center">Private lots page (coming soon)</div>' }},
    { path: '/book/:id', meta: { requiresAuth: true }, component: { template: '<div class="p-10 text-center">Booking page (coming soon)</div>' }},
    { path: '/book-ticket/:id', meta: { requiresAuth: true }, component: { template: '<div class="p-10 text-center">Ticket page (coming soon)</div>' }},

    // ADMIN ROUTES -------------------------------------
    {
        path: '/admin',
        component: AdminLayout,
        meta: { requiresAuth: true, admin: true },
        children: [
            {path:'calender',name:'admincalender',component:NewCalender},
            {path: 'darshan-slots', name: 'admin-darshanslots', component: AdminDarshanslots },
            { path: 'dashboard', name: 'admin-dashboard', component: AdminDashboard },
            { path: 'parking-lots', name: 'admin-parking-lots', component: ParkingLotList },
            { path: 'parking-lots/add', name: 'admin-add-lot', component: AddParkingLot },
            { path: 'parking-lots/:id/edit', name: 'admin-edit-lot', component: AddParkingLot, props: true },
            { path: 'spots/:id', name: 'admin-spot-detail', component: AdminSpotDetail },
            { path: 'private-parking', name: 'admin-private-parking', component: AdminPrivateParking },
            { path: 'scan-ticket', name: 'admin-scan-ticket', component: AdminScanTicket },
            { path: 'analytics', name: 'admin-summary', component: AdminSummary },
            { path: 'users', name: 'admin-users', component: AdminUsers },
            {path:'all-tickets',name:'all-tickets',component:AdminDarshanDetails}
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})


// --------------------------------------------------------------
// GLOBAL ROUTE GUARD (Login + Admin Protection)
// --------------------------------------------------------------
router.beforeEach((to, from, next) => {
    const userStore = useUserStore()

    // Load user from session (important for page refresh)
    userStore.loadFromSession()

    const isLoggedIn = !!userStore.id
    const isAdmin = userStore.role === "admin"  // 0 = admin in your backend

    // 1. Protect all requiresAuth routes
    if (to.meta.requiresAuth && !isLoggedIn) {
        return next('/login')
    }

    // 2. Admin route protection
    if (to.meta.admin && !isAdmin) {
        return next('/login')
    }

    next()
})

export default router
