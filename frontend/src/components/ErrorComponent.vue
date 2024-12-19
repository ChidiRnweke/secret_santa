<script setup lang="ts">
import Dialog from 'primevue/dialog'
import { ref, watch } from 'vue'
import Button from 'primevue/button'

// Props and Emits
const { errorMessage, visible: propVisible } = defineProps([
  'errorMessage',
  'visible',
])
const emit = defineEmits(['update:visible'])

const localVisible = ref(propVisible)

watch(
  () => propVisible,
  newVal => {
    localVisible.value = newVal
  },
)

// Watch localVisible to emit changes back to parent
watch(localVisible, newVal => {
  emit('update:visible', newVal)
})

// Close the dialog
function closeDialog() {
  localVisible.value = false
}
</script>

<template>
  <Dialog
    v-model:visible="localVisible"
    modal
    class="box-border p-4 mx-4 w-max-content"
  >
    <template #header>
      <h2 class="text-2xl text-red-400">An error occurred.</h2>
    </template>
    <p>{{ errorMessage }}</p>
    <template #footer>
      <Button type="button" label="Close" @click="closeDialog"></Button>
    </template>
  </Dialog>
</template>
