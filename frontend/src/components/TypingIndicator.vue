<template>
  <div class="typing-indicator">
    <div class="avatar">
      <div class="bot-avatar">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M21.928 11.607c-.202-.488-.635-.605-.928-.633-.326-.034-.654-.042-.982-.034l-2.227 1.307a7.89 7.89 0 00-1.638-1.403l.837-2.647c.096-.303.05-.625-.125-.889C16.487 6.23 16.167 6 15.81 6H8.19c-.357 0-.677.23-.829.577-.175.264-.221.586-.125.889l.837 2.647a7.945 7.945 0 00-1.638 1.403l-2.227-1.307c-.328-.008-.656 0-.982.034-.293.028-.726.145-.928.633-.263.64-.404 1.337-.404 2.068v3c0 1.654 1.346 3 3 3h1.22l1.056 3.166c.099.297.38.5.69.5h1.24c.31 0 .591-.203.69-.5L10.78 19H13v3h8v-3h1.19c1.654 0 3-1.346 3-3v-3c0-.731-.141-1.428-.404-2.068h-.002zM5 14c-.552 0-1-.449-1-1v-1c0-.551.448-1 1-1s1 .449 1 1v1c0 .551-.448 1-1 1zm14 0c-.552 0-1-.449-1-1v-1c0-.551.448-1 1-1s1 .449 1 1v1c0 .551-.448 1-1 1z"/>
        </svg>
      </div>
    </div>
    <div class="dots-container">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  </div>
</template>

<script setup>
// No props needed
</script>

<style scoped>
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  animation: fadeIn 0.3s ease-out;
}

.avatar {
  flex-shrink: 0;
}

.bot-avatar {
  background: #4f46e5;
  color: white;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.bot-avatar svg {
  width: 20px;
  height: 20px;
}

.dots-container {
  display: flex;
  gap: 0.4rem;
  padding: 0.75rem 1rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  border-bottom-left-radius: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-secondary);
  animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.6;
  }
  30% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .typing-indicator {
    margin-bottom: 1rem;
  }
  
  .dots-container {
    padding: 0.6rem 0.8rem;
  }
  
  .dot {
    width: 6px;
    height: 6px;
  }
}
</style>