<script setup lang="ts">
import { ref, type Ref, computed } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
const participant = ref('')
const participants: Ref<string[], string[]> = ref([])
const addParticipant = () => {
  participants.value.push(participant.value)
  participant.value = ''
}
const participantCount = computed(() => participants.value.length)
const removeParticipant = (index: number) => {
  participants.value.splice(index, 1)
}
</script>
<template>
  <div class="flex place-content-center flex-col gap-y-12">
    <section>
      <h1 class="text-4xl text-center">Let's get you started in no time</h1>
    </section>
    <section
      class="bg-orange-50 bg-opacity-50 place-self-center grid grid-cols-1 gap-y-8"
    >
      <h2 class="text-lg text-center">
        Who will be joining your Secret Santa event?
      </h2>
      <form
        @submit.prevent="addParticipant"
        class="flex flex-row justify-items-start gap-x-10 mb-8"
      >
        <InputText v-model="participant" type="text" />
        <Button
          icon="pi pi-plus-circle"
          label="Add Participant"
          type="submit"
          size="small"
        />
      </form>
      <div v-if="participantCount > 0" class="grid grid-cols-1 gap-y-10">
        <div
          v-for="participant in participants"
          :key="participant"
          class="grid grid-cols-2 items-center justify-items-center"
        >
          <p class="font-bold text-lg">{{ participant }}</p>
          <Button
            @click="removeParticipant(participants.indexOf(participant))"
            icon="pi pi-times"
            aria-label="remove"
            variant="text"
            severity="danger"
            rounded
            size="small"
          />
        </div>
      </div>
    </section>
  </div>
</template>
