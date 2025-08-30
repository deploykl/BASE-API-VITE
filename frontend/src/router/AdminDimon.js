import ConsultaExternaView from "../views/dimon/ConsultaExternaView.vue";
import TableroListView from "../views/dimon/tablero/TableroListView.vue";
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
      requiredModule: "Sistemas" // ← Añade esta propiedad

    },
  },
    {
    path: "/dimon/tablero/list",
    name: "Tablero-list",
    component: TableroListView,
    meta: {
      title: "TABLEROS MONITOR",
      requiresAuth: true,
      requiredModule: "Monitor, Sistemas" // ← Añade esta propiedad

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
