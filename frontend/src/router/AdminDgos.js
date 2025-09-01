import ComisionView from "../views/dgos/administracion/ComisionView.vue";
import PersonalView from "../views/dgos/administracion/PersonalView.vue";

const AdminDgos = [
  {
    path: "/dgos/administracion/comision",
    name: "Comisión",
    component: ComisionView,
    meta: {
      title: "COMISIÓN",
      requiresAuth: true,
    },
  },
  {
    path: "/dgos/personal",
    name: "Personal",
    component: PersonalView,
    meta: {
      title: "PERSONAL",
      requiresAuth: true,
      requiredModule: "Personal" // ← Añade esta propiedad

    },
  },
];

export default AdminDgos;
