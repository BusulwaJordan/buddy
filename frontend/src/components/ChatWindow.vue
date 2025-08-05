<script setup>
import { ref, nextTick, onMounted } from 'vue'
import MessageBubble from '@/components/MessageBubble.vue'
import TypingIndicator from '@/components/TypingIndicator.vue'

const messages = ref([
  {
    type: 'bot',
    text: 'Hello! I can answer questions about our company based on our website content. How can I help you today?',
    timestamp: new Date()
  }
])
const loading = ref(false)
const userInput = ref('')
const messagesContainer = ref(null)

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  const question = userInput.value
  messages.value.push({
    type: 'user',
    text: question,
    timestamp: new Date()
  })
  userInput.value = ''
  loading.value = true
  
  try {
    const response = await fetch(`${apiUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    })
    
    if (!response.ok) throw new Error('Network response was not ok')
    
    const data = await response.json()
    messages.value.push({
      type: 'bot',
      text: data.answer,
      sources: data.sources || [],
      timestamp: new Date()
    })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({
      type: 'bot',
      text: 'Sorry, I encountered an error. Please try again later.',
      timestamp: new Date()
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  scrollToBottom()
})
</script>

<template>
  <div class="chat-window">
    <div class="messages-container" ref="messagesContainer">
      <TransitionGroup name="slide-up">
        <MessageBubble
          v-for="(message, index) in messages"
          :key="index"
          :type="message.type"
          :text="message.text"
          :sources="message.sources"
          :timestamp="message.timestamp"
        />
      </TransitionGroup>
      <TypingIndicator v-if="loading" />
    </div>
    
    <div class="input-container">
      <form @submit.prevent="sendMessage" class="message-form">
        <div class="input-wrapper">
          <input
            v-model="userInput"
            placeholder="Ask me anything about our company..."
            :disabled="loading"
            class="message-input"
          />
          <button type="submit" :disabled="!userInput || loading" class="send-button">
            <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="send-icon">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
            <div v-else class="spinner"></div>
          </button>
        </div>
        <div class="input-hint">
          Press Enter to send, Shift+Enter for new line
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 180px);
  max-width: 800px;
  margin: 0 auto;
  background: var(--bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow);
  overflow: hidden;
  border: 1px solid var(--border);
}

.messages-container {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.input-container {
  padding: 1rem;
  border-top: 1px solid var(--border);
  background: var(--bg-primary);
}

.message-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-wrapper {
  position: relative;
  display: flex;
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  padding-right: 3rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s;
  min-height: 50px;
  max-height: 150px;
  resize: none;
}

.message-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
}

.send-button {
  position: absolute;
  right: 0.5rem;
  bottom: 0.5rem;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  background: #4338ca;
  transform: scale(1.05);
}

.send-button:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

.send-icon {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.input-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
  padding: 0 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .chat-window {
    height: calc(100vh - 160px);
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
  
  .messages-container {
    padding: 1rem;
  }
}
</style>