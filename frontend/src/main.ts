import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './app.css'
import './assets/tailwind.css'
import PrimeVue from 'primevue/config'

const app = createApp(App)

app.use(router)
app.use(PrimeVue, { theme: 'none' })

app.mount('#app')
