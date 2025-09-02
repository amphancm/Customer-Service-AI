<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center overflow-y-auto z-50"
    @click.self="closeModal"
  >
    <div
      class="bg-white   rounded-3xl shadow-md w-full max-w-[500px] mx-4 my-10 overflow-hidden flex flex-col"
      @click.stop
    >
      <!-- Header -->
      <div class="flex justify-between items-center p-6 border-b border-white/20 rounded-t-3xl">
        <h3 class="text-xl font-bold text-textColor">{{ title }}</h3>
        <button
          @click="closeModal"
          class="text-red-500 0 text-2xl font-bold"
          aria-label="Close modal"
        >
          &times;
        </button>
      </div>

      <!-- Body (Scrollable) -->
      <div class="p-7 max-h-[60vh] overflow-y-auto">
        <slot name="body">
          <p class="text-textColor">This is the modal content.</p>
        </slot>

      </div>

       <!-- Footer -->
        <div class="flex justify-center items-center p-6 border-t border-white/20 rounded-b-3xl gap-4">
          <button
            @click="confirmAction"
            class="  text-white text-lg px-6 py-3 rounded-xl font-jeju flex items-center gap-2 bg-[#E43A32] hover:bg-red-700 "
          >
            <img src="/src/assets/icons/trash (5).png" alt="Delete Icon" class="h-5 w-5   "/>

            Delete
          </button>
          <button
            @click="closeModal"
            class="  text-textColor text-lg px-6 py-3 rounded-xl font-jeju flex items-center gap-2 bg-[#F0F1F1] hover:bg-gray-500 "
          >
            <img src="/src/assets/icons/cross (1).png" alt="Delete Icon" class="h-5 w-5   "/>
            Cancel
        </button>
      </div>
    </div>
  </div>
</template>



<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue'

// Props
defineProps({
  isOpen: Boolean,
  isAlert: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Modal Title',
  },
})

// Emits
const emit = defineEmits(['close', 'confirm'])

// Methods
function closeModal() {
  emit('close')
}

function confirmAction() {
  emit('confirm')
}
</script>

<style scoped>
/* Additional styling if needed */
</style>
