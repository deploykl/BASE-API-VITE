import ConsultaExternaView from "../views/dimon/ConsultaExternaView.vue";
import TableroView from "../views/dimon/TableroView.vue";
import LoginView from "../views/gore/LoginView.vue";

const AdminDimon = [
  {
    path: "/dimon/tablero",
    name: "Tablero",
    component: TableroView,
    meta: {
      title: "TABLEROS",
      requiresAuth: true,
    },
  },
  {
    path: "/dimon/consulta-externa",
    name: "presupuesto",
    component: ConsultaExternaView,
    meta: {
      title: "CONSULTA EXTERNA",
    },
  },
];

export default AdminDimon;
