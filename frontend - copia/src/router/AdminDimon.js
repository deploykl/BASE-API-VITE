import ConsultaExternaView from "../views/dimon/ConsultaExternaView.vue";
import LoginView from "../views/gore/LoginView.vue";


const AdminDimon = [
   {
      path: "/consulta-externa",
      name: "presupuesto",
      component: ConsultaExternaView,
      meta: {
        title: "CONSULTA EXTERNA",
      },
    },
];

export default AdminDimon;