<script setup>
import ChatWindow from '@/components/ChatWindow.vue'
import { ref } from 'vue'

const darkMode = ref(false)
const toggleTheme = () => darkMode.value = !darkMode.value
</script>

<template>
  <div :class="['app-container', { 'dark': darkMode }]">
    <header class="app-header">
      <div class="header-content">
        <h1>
          <span class="gradient-text">OTIC</span> AI Buddy
          <button @click="toggleTheme" class="theme-toggle">
            {{ darkMode ? '☀️' : '🌙' }}
          </button>
        </h1>
        <p class="subtitle">Your intelligent business companion</p>
      </div>
    </header>

    <main class="app-main">
      <ChatWindow />
    </main>

    <footer class="app-footer">
      <p>© 2023 Company Inc. • <a href="#" class="footer-link">Privacy</a> • <a href="#" class="footer-link">Terms</a></p>
    </footer>
  </div>
</template>

<style>
@import '@/assets/base.css';
</style>

<style scoped>
.app-container {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --accent: #4f46e5;
  --border: #e2e8f0;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  min-height: 100vh;
  transition: all 0.3s ease;
}

.dark .app-container {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --accent: #818cf8;
  --border: #334155;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

.app-header {
  background: var(--bg-primary);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.gradient-text {
  background: linear-gradient(90deg, #4f46e5, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.subtitle {
  color: var(--text-secondary);
  margin: 0.5rem 0 0;
  font-size: 1rem;
}

.theme-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
  margin-left: 0.5rem;
}

.app-main {
  flex: 1;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  text-align: center;
  padding: 1.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  border-top: 1px solid var(--border);
}

.footer-link {
  color: var(--accent);
  text-decoration: none;
  margin: 0 0.5rem;
}

.footer-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  h1 {
    font-size: 1.5rem;
  }
  
  .app-main {
    padding: 1rem;
  }
}
</style>