import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

// Views
import TempleDonation from '../views/TempleDonation.vue'
import Book_aarti_Tatkal from '../views/Book_aarti_Tatkal.vue'
import Book_Darshan_Tatkal from '../views/Book_Darshan_Tatkal.vue'
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
import MobileLogin from '../views/mobile-login.vue'
import BookAarti from '../views/Book_aarti.vue'

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
     },
    {
        path:'dashboard',
        name: 'user-dashboard',
        component: UserDashboardnew,
    },
    {
    path: 'accomodation',
    name: 'AccomodationFinder',
    component: AccomodationFinder
    },
    {
        path: 'book_darshannew',
        name: 'book_darshannew',
        component: BookDarshanNew,
    },
    {
        path: '/user/editnew',
        name: 'user-editnew',
        component: UserEditnew,
    },
    {
        path: 'book-aarti',
        name: 'book-aarti',
        component: BookAarti,
    },
    {
        path: 'book-seva',
        name: 'book-seva',
        component: Bookseva,
    },
    {
        path: 'book-spot',
        name: 'book-spot',
        component: Bookspot,
    },
    {
        path:'book_darshan_tatkal',
        name:'book_darshan_tatkal',
        component:Book_Darshan_Tatkal,
    },
    // NEW ROUTE ADDED FOR TEMPLE DONATION (Fixes the link from the Dashboard)
    {
        path: 'donation',
        name: 'temple-donation',
        component: TempleDonation,
    },
    {
        path:'book_aarti_tatkal',
        name:'book_aarti_tatkal',
        component:Book_aarti_Tatkal
    },
]
},
    // Public routes
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/mobile-login', name: 'mobile-login', component: MobileLogin },


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
