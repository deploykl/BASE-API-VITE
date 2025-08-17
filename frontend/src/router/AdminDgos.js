import ComisionView from "../views/dgos/administracion/ComisionView.vue";

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
];

export default AdminDgos;
