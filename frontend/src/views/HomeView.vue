<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
</script>

<template>
  <section
    class="text-center grid grid-cols-1 gap-y-8 justify-items-center border-box lg:mx-32 md:mx-20 mx-8 mb-32"
  >
    <h1 class="text-6xl">
      Organize Your
      <span class="text-primary-700 dark:text-primary-300">Secret Santa</span>
      Effortlessly.
    </h1>
    <p class="text-xl">
      The easiest way to organize a joyful gift exchange! No sign-up required.
      Create and share your Secret Santa event in just a few clicks.
    </p>
    <Button>Get Started Now</Button>
  </section>

  <section class="grid grid-cols-1 gap-y-4 mt-8 text-center box-border px-8">
    <div
      class="grid grid-cols-1 md:grid-cols-3 justify-items-center gap-6 mt-6"
    >
      <Card class="max-w-80 bg-surface-50 dark:bg-surface-600">
        <template #header>
          <img
            alt="Quick Setup"
            src="../assets/images/santa_horizontal.png"
            class="rounded-md"
          />
        </template>
        <template #title>Quick & Easy Setup</template>
        <template #content>
          <p>
            Start your event in seconds. All you need is your group's names, and
            you're ready to go!
          </p>
        </template>
      </Card>

      <Card class="max-w-80 bg-surface-50 dark:bg-surface-600">
        <template #header>
          <img
            alt="Shareable Link"
            src="../assets/images/santa_computer.png"
            class="rounded-md"
          />
        </template>
        <template #title>Share with a Single Link</template>
        <template #content>
          <p>
            Share a unique link with everyone in your group. No sign-ups
            required for them either!
          </p>
        </template>
      </Card>

      <Card class="max-w-80 bg-surface-50 dark:bg-surface-600">
        <template #header>
          <img
            alt="Secret Matches"
            src="../assets/images/fireplace.png"
            class="rounded-md"
          />
        </template>
        <template #title>Secret Gift Matching</template>
        <template #content>
          <p>
            Keep the magic alive! Matches are confidential, so each gift is a
            surprise.
          </p>
        </template>
      </Card>
    </div>
  </section>
</template>
