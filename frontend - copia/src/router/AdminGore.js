import PresupuestoView from "../views/gore/PresupuestoView.vue";
import LoginView from "../views/gore/LoginView.vue";


const AdminGore = [
   {
      path: "/presupuesto",
      name: "presupuesto",
      component: PresupuestoView,
      meta: {
        title: "PRESUPUESTO",
      },
    },
    {
        path: "/gore/login",
        name: "gore-login",
        component: LoginView,
        meta: {
          title: "Login",
          requiresUnauth: true,
        },
      },
];

export default AdminGore;