<script setup lang="ts">
import Button from 'primevue/button'
import { ref, computed } from 'vue'

const initialVal =
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
const darkMode = ref(initialVal)

const iconType = computed(() => (darkMode.value ? 'pi pi-moon' : 'pi pi-sun'))

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  const mode = darkMode.value ? 'dark' : 'light'
  localStorage.setItem('theme', mode)
  document.documentElement.classList.toggle('dark', darkMode.value)
}
</script>

<template>
  <Button type="button" :icon="iconType" @click="toggleDarkMode" size="small" />
</template>
