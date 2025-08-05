<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'bot',
    validator: (value) => ['bot', 'user'].includes(value)
  },
  text: {
    type: String,
    required: true
  },
  sources: {
    type: Array,
    default: () => []
  },
  timestamp: {
    type: Date,
    required: true
  }
})

const formattedTime = computed(() => {
  return props.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
})
</script>

<template>
  <div :class="['message-bubble', type]">
    <div class="avatar">
      <div v-if="type === 'bot'" class="bot-avatar">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M21.928 11.607c-.202-.488-.635-.605-.928-.633-.326-.034-.654-.042-.982-.034l-2.227 1.307a7.89 7.89 0 00-1.638-1.403l.837-2.647c.096-.303.05-.625-.125-.889C16.487 6.23 16.167 6 15.81 6H8.19c-.357 0-.677.23-.829.577-.175.264-.221.586-.125.889l.837 2.647a7.945 7.945 0 00-1.638 1.403l-2.227-1.307c-.328-.008-.656 0-.982.034-.293.028-.726.145-.928.633-.263.64-.404 1.337-.404 2.068v3c0 1.654 1.346 3 3 3h1.22l1.056 3.166c.099.297.38.5.69.5h1.24c.31 0 .591-.203.69-.5L10.78 19H13v3h8v-3h1.19c1.654 0 3-1.346 3-3v-3c0-.731-.141-1.428-.404-2.068h-.002zM5 14c-.552 0-1-.449-1-1v-1c0-.551.448-1 1-1s1 .449 1 1v1c0 .551-.448 1-1 1zm14 0c-.552 0-1-.449-1-1v-1c0-.551.448-1 1-1s1 .449 1 1v1c0 .551-.448 1-1 1z"/>
        </svg>
      </div>
      <div v-else class="user-avatar">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
        </svg>
      </div>
    </div>
    <div class="content">
      <div class="message-header">
        <span class="sender-name">{{ type === 'bot' ? 'AI Assistant' : 'You' }}</span>
        <span class="message-time">{{ formattedTime }}</span>
      </div>
      <div class="text">{{ text }}</div>
      <div v-if="sources && sources.length" class="sources">
        <div class="sources-title">Sources</div>
        <ul>
          <li v-for="(source, idx) in sources" :key="idx">
            <a :href="source.url" target="_blank" rel="noopener noreferrer" class="source-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="link-icon">
                <path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/>
              </svg>
              {{ source.title || 'Learn more' }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-bubble {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  animation: fadeIn 0.3s ease-out;
}

.avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bot-avatar {
  background: #4f46e5;
  color: white;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.bot-avatar svg {
  width: 20px;
  height: 20px;
}

.user-avatar {
  background: #e2e8f0;
  color: #4f46e5;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.user-avatar svg {
  width: 20px;
  height: 20px;
}

.content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.25rem;
  gap: 0.5rem;
}

.sender-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.message-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.text {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  line-height: 1.5;
  word-break: break-word;
  white-space: pre-wrap;
}

.message-bubble.bot .text {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

.message-bubble.user .text {
  background: var(--accent);
  color: white;
  border-bottom-right-radius: 4px;
}

.sources {
  margin-top: 0.75rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  border-top: 1px solid var(--border);
  padding-top: 0.75rem;
}

.sources-title {
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.sources ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.source-link {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s;
}

.source-link:hover {
  color: #4338ca;
  text-decoration: underline;
}

.link-icon {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>