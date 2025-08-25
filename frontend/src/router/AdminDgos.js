import ComisionView from "../views/dgos/administracion/ComisionView.vue";
import PersonalManager from "../views/dgos/administracion/PersonalManager.vue";

const AdminDgos = [
  {
    path: '/dgos/administracion/comision',
    name: "Comisión",
    component: ComisionView,
    meta: {
      title: "COMISIÓN",
      requiresAuth: true,
    },
  },
   {
    path: '/dgos/personal',
    name: "Personal",
    component: PersonalManager,
    meta: {
      title: "PERSONAL",
      requiresAuth: true,
    },
  },
];

export default AdminDgos;
