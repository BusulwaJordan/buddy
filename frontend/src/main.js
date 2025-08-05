import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

// Create and mount the app
const app = createApp(App)
app.mount('#app')

// Optional: Add global error handler
app.config.errorHandler = (err) => {
  console.error('Vue error:', err)
  // You could show a user-friendly error message here
}