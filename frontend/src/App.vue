<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import 'primeicons/primeicons.css'
import FooterComponent from '@/components/FooterComponent.vue'
import DarkModeToggle from '@/components/DarkModeToggle.vue'
import BrandLogo from './components/BrandLogo.vue'
</script>

<template>
  <header
    class="mb-12 flex justify-between flex-row place-items-end align-middle"
  >
    <BrandLogo class="mr-4" />
    <nav class="flex flex-row gap-x-8 align-middle">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/register">Register</RouterLink>
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
