<script setup lang="ts">
import { ref, type Ref, computed } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import ButtonGroup from 'primevue/buttongroup'
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
const resetParticipants = () => {
  participants.value = []
}
const sendParticipants = () => {
  console.log(participants.value)
}
</script>
<template>
  <div class="flex place-content-center flex-col gap-y-12">
    <section>
      <h1 class="text-4xl text-center">Let's get you started in no time</h1>
    </section>
    <section
      class="place-self-center grid grid-cols-1 gap-y-8 border-2 rounded-md border-gray-950 dark:border-white p-8 box-border"
    >
      <h2 class="text-lg text-center">
        Who will be joining your Secret Santa event?
      </h2>
      <form
        @submit.prevent="addParticipant"
        class="flex flex-row justify-items-start gap-x-10 mb-8"
      >
        <InputText v-model="participant" type="text" class="w-8/12" />
        <Button
          icon="pi pi-plus-circle"
          label="Add Participant"
          type="submit"
          size="small"
        />
      </form>
      <div
        v-if="participantCount > 0"
        class="flex flex-col flex-wrap gap-10 place-self-center max-h-80 overflow-y-auto"
      >
        <div
          v-for="participant in participants"
          :key="participant"
          class="flex flex-row flex-wrap items-center gap-x-3"
        >
          <Button
            @click="removeParticipant(participants.indexOf(participant))"
            icon="pi pi-times"
            aria-label="remove"
            variant="outlined"
            severity="danger"
            rounded
            size="small"
          />
          <p class="font-bold text-lg">{{ participant }}</p>
        </div>
      </div>
      <ButtonGroup
        v-if="participantCount > 0"
        class="flex w-full"
        @click="sendParticipants"
      >
        <Button label="Continue" class="w-full" icon="pi pi-arrow-right" />
        <Button
          label="Reset"
          class="w-full"
          icon="pi pi-replay"
          severity="danger"
          @click="resetParticipants"
        />
      </ButtonGroup>
    </section>
  </div>
</template>
