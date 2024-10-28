<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import 'primeicons/primeicons.css'
import FooterComponent from '@/components/FooterComponent.vue'
import DarkModeToggle from '@/components/DarkModeToggle.vue'
import BrandLogo from './components/BrandLogo.vue'
</script>

<template>
  <header class="mb-2 flex justify-between flex-row place-items-end">
    <BrandLogo />
    <nav class="flex flex-row gap-x-8">
      <RouterLink to="/">Home</RouterLink>
      <div>
        <DarkModeToggle class="bg-surface-0 dark:bg-surface-900 text-color" />
      </div>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
  <FooterComponent />
</template>
