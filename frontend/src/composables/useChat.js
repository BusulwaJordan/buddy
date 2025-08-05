import { ref } from 'vue'

export function useChat() {
  const messages = ref([
    {
      type: 'bot',
      text: 'Hello! I can answer questions about our company based on our website content. How can I help you today?'
    }
  ])
  const loading = ref(false)
  const userInput = ref('')

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const sendMessage = async () => {
    if (!userInput.value.trim()) return

    const question = userInput.value
    messages.value.push({
      type: 'user',
      text: question
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
        sources: data.sources || []
      })
    } catch (error) {
      console.error('Error:', error)
      messages.value.push({
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again later.'
      })
    } finally {
      loading.value = false
    }
  }

  return { messages, loading, userInput, sendMessage }
}