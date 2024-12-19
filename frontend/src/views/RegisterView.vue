<script setup lang="ts">
import { ref, type Ref, computed } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import ButtonGroup from 'primevue/buttongroup'
import { santaService, type AssignmentResponse } from '@/lib/api'
import Dialog from 'primevue/dialog'
import ErrorComponent from '@/components/ErrorComponent.vue'

const participant = ref('')
const participants: Ref<string[], string[]> = ref([])
const userAssignments: Ref<
  AssignmentResponse | undefined,
  AssignmentResponse | undefined
> = ref()
const assignmentsMade = computed(() => userAssignments.value !== undefined)
const err = ref(false)
const errMsg = ref('')

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

const links = computed(() => {
  const data = userAssignments.value
  if (data === undefined) {
    return []
  } else {
    return data.assignments.map(assignment => {
      return {
        sender: assignment.gift_sender,
        gift_link: new URL(
          `/gift/${data.assignment_name}/${assignment.gift_sender}`,
          window.location.origin,
        ).toString(),
      }
    })
  }
})

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text)
}

const sendParticipants = async () => {
  try {
    const created_assignments = await santaService.makeAssignment({
      users: participants.value,
    })
    userAssignments.value = created_assignments
  } catch (e) {
    console.log(e)
    err.value = true
    errMsg.value = (e as Error).message
  }
}

const clearAssignments = () => {
  userAssignments.value = undefined
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
  <ErrorComponent
    v-model:visible="err"
    :errorMessage="errMsg"
    @update:visible="err = $event"
  />
  <Dialog
    v-model:visible="assignmentsMade"
    modal
    class="box-border p-4 mx-4 w-max-content"
  >
    <template #header>
      <h2 class="text-2xl">Here are your personalized links. Happy gifting!</h2>
    </template>
    <div class="flex flex-col gap-y-4">
      <div
        v-for="link in links"
        :key="link.sender"
        class="flex flex-row items-center gap-x-2"
      >
        <Button
          icon="pi pi-copy"
          aria-label="copy"
          @click="copyToClipboard(link.gift_link)"
          class="p-2"
        />
        <p class="text-lg">{{ link.sender }}'s link:</p>
        <InputText
          type="text"
          :value="link.gift_link"
          readonly
          class="border p-1 max-w-72 w-full"
        />
      </div>
    </div>
    <template #footer>
      <Button type="button" label="Cancel" @click="clearAssignments"></Button>
    </template>
  </Dialog>
</template>
