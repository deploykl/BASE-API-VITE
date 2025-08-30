import LoginView from "../views/account/LoginView.vue";
import ProfileView from "../views/account/ProfileView.vue";
import UserView from "../views/account/UserView.vue";
import ChangePasswordView from "../views/account/ChangePasswordView.vue";

const AdminAuth = [
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {
      title: "Login",
      public: true,
      hideLayout: true
    },
  },
  {
    path: "/perfil",
    name: "perfil",
    component: ProfileView,
    meta: {
      title: "Perfil",
      requiresAuth: true,
    },
  },
   {
    path: "/user/create",
    name: "user-create",
    component: UserView,
    meta: {
      title: "Create User",
      requiresAuth: true,
      requiredModule: "Usuarios", // ← Añade esta propiedad

    },
  },
   {
    path: "/change-password",
    name: "change-password",
    component: ChangePasswordView,
    meta: {
      title: "Cambiar Contraseña",
      requiresAuth: true,
    },
  },
];

export default AdminAuth;
