import { createApp } from 'vue'
import App from './App.vue'
import router from './router'          // Importa el router
import { createPinia } from 'pinia'    // Importa Pinia
import ErrorMessage from '@/components/utils/ErrorMessage.vue'
import PrimeVue from 'primevue/config'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Tooltip from 'primevue/tooltip';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import OverlayBadge from 'primevue/overlaybadge';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';
import Aura from '@primeuix/themes/aura';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice' // Añade esta importación
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dropdown from 'primevue/dropdown';
import Tag from 'primevue/Tag';
import ToggleSwitch from 'primevue/toggleswitch';
import ProgressBar from 'primevue/ProgressBar';
import Card from 'primevue/Card';
import Divider from 'primevue/Divider';
import Password from 'primevue/Password';
import Sidebar from 'primevue/sidebar';

// LIBRERÍAS
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import 'vue-sonner/style.css'

import '@/assets/lib/fontawesome-v6.5.2/css/all.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-light.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-regular.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-solid.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-thin.css'

import 'primeicons/primeicons.css'

// PERSONALIZADO
import '@/assets/css/font.css'
import '@/assets/css/main.css'

const app = createApp(App)
const pinia = createPinia()

// Configure and use PrimeVue once
app.use(PrimeVue, {
    // Default theme configuration
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'false',
            cssLayer: false
        }
    }
 });

// Use other plugins
app.use(router)
app.use(pinia)
app.use(ToastService)

// Registra componentes globales
app.component('ErrorMessage', ErrorMessage)
app.component('FloatLabel', FloatLabel)
app.component('InputText', InputText)
app.directive('tooltip', Tooltip);
app.component('Dialog', Dialog);
app.component('Button', Button);
app.component('Badge', Badge);
app.component('OverlayBadge', OverlayBadge);
app.component('Message', Message);
app.component('ProgressSpinner', ProgressSpinner);
app.component('ProgressBar', ProgressBar);
app.component('Toast', Toast);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Dropdown', Dropdown);
app.component('Tag', Tag);
app.component('ToggleSwitch', ToggleSwitch);
app.component('Card', Card);
app.component('Divider', Divider);
app.component('Password', Password);
app.component('Sidebar', Sidebar);

// Monta la aplicación
app.mount('#app')