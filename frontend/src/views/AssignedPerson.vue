<script setup lang="ts">
import { useRoute } from 'vue-router'
import { santaService } from '@/lib/api'
import { onMounted, ref } from 'vue'
import Skeleton from 'primevue/skeleton'

const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
const sender = ref('')
const receiver = ref('')
const linkOpenedTimes = ref(0)

const route = useRoute()
const santaId = route.params.sessionId as string
const senderId = route.params.senderName as string

onMounted(async () => {
  try {
    const { gift_sender, gift_receiver, times_viewed } =
      await santaService.getAssignment(santaId, senderId)
    sender.value = gift_sender
    receiver.value = gift_receiver
    linkOpenedTimes.value = times_viewed
    loading.value = false
  } catch (e) {
    console.error(e)
    error.value = true
    loading.value = false
    errorMessage.value = (e as Error).message || 'An error occurred'
  }
})
</script>

<template>
  <section
    v-if="loading"
    class="text-center grid grid-cols-1 gap-y-8 justify-items-center border-box lg:mx-32 md:mx-20 mx-8 mb-32"
  >
    <Skeleton width="100%" height="50px" />
    <Skeleton width="100%" height="50px" />
    <Skeleton width="100%" height="50px" />
  </section>
  <section v-if="error" class="text-center">
    <h1 class="text-6xl mb-20">An error occurred.</h1>
    <p class="text-xl">
      We're sorry, but we couldn't find who you need get a gift for. Please try
      again later.
    </p>
  </section>

  <section
    v-if="!loading && !error"
    class="text-center grid grid-cols-1 gap-y-8 justify-items-center border-box lg:mx-32 md:mx-20 mx-8 mb-32"
  >
    <h1 class="text-6xl">
      Hi, {{ sender }}! Your Secret Santa is
      <span class="text-primary-700 dark:text-primary-300"
        >{{ receiver }}!</span
      >
    </h1>
    <p class="text-3xl">
      You can now start preparing your gift for {{ receiver }}. Good luck and
      have fun! 🎁
    </p>
    <p v-if="linkOpenedTimes == 1">✨ You're the first to open this link. ✨</p>
    <p v-else>
      PS: this link has been opened
      <span class="text-primary-700 dark:text-primary-300">{{
        linkOpenedTimes
      }}</span>
      times.
    </p>
  </section>
</template>
