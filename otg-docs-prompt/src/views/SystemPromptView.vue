<template>
  <div class="h-full min-h-screen flex flex-col items-start justify-start p-12 pl-[1px] text-white  text-base">

    <div class="pl-20 w-[1000px]">
    <!-- กล่อง System Prompt -->
     <div class="mb-8">
          <h4 class="text-2xl text-textColor font-Promt mb-3 font-bold">Parameters</h4>

        <!-- Label + Input -->
        <div class="flex items-center gap-20 mb-10">
          <label class="text-lg text-textColor font-Promt mr-10"> Temperature</label>
          <!-- <input
            type="number"
            @input="validateInput"
            min="0"
            max="1"
            step="0.01"
            v-model="system_prompt.temperature"
            class="text-center w-16 px-2 py-1 rounded-md bg-customSystempromt border-2 border-black border-opacity-10 text-textColor font-Promt focus:outline-none focus:ring-2 focus:ring-customSildboxred no-spinner"
          /> -->
        </div>


        <!-- Slider -->
       <div class="relative w-full mt-8">
          <!-- ตัวเลขที่อยู่บนหัว slider -->
          <div
            id="slider-value"
            class="absolute -top-12 text-white text-xs font-semibold bg-[#E43A32] px-3 py-1 rounded-xl shadow transform -translate-x-1/2 transition-all duration-100"
            style="left: 0%"
          >
            0.00
          </div>

          <!-- Slider -->
          <input
            id="slider"
            type="range"
            min="0"
            max="1"
            step="0.01"
            v-model="system_prompt.temperature"
            class="w-full appearance-none h-2 rounded-lg bg-[#E43A32] custom-slider"


            @input="(e) => updateSliderFill(e.target as HTMLInputElement)"
          />
        </div>
      </div>

      <!-- Textarea -->
      <div class="mb-8">
        <label class="text-lg text-textColor font-Promt mr-10 font-bold"> System Prompt</label>
        <textarea
          v-model="system_prompt.content"
          rows="10"
          class="w-full p-4 rounded-xl border border-back-500 text-textColor placeholder-black focus:outline-none focus:ring-2 focus:ring-customSildboxred no-spinner text-base"
          placeholder="Enter System Prompt"
        ></textarea>
      </div>

    <!-- ปุ่ม Save -->
    <div class="w-full max-w-7xl flex  ml-1 mt-6">
      <button
        @click="handleSave"
        class="bg-customSildboxred text-white text-lg px-6 py-3 rounded-2xl font-Promt flex items-center gap-2 hover:bg-red-600 "
      >
        <img src="@/assets/icons/disk (2).png" alt="My Icon" class="w-6 h-6" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1" />
        Save
      </button>
    </div>
  </div>

    <!-- ✅ SUCCESS OVERLAY (ไม่มีพื้นหลัง) -->
    <div v-if="isSuccess" class="fixed inset-0 z-50 flex items-center justify-center pointer-events-none">
      <div
        class="flex flex-col items-center px-10 py-8 rounded-2xl pointer-events-auto animate-scaleIn"
        style="background: transparent;"
      >
     <!-- วงกลมขนาดใหญ่ขึ้น + ติ๊กถูกตรงกลาง -->
        <div class="w-48 h-48  rounded-full border-[12px] border-green-500 flex items-center justify-center shadow-xl">
          <svg
            class="w-24 h-24 text-green-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <!-- ข้อความ -->
        <p class="mt-6 text-4xl font-bold text-green-600">Saved successfully</p>
      </div>
    </div>
  </div>
</template>



<script lang="ts" setup>
import { useSystemPromptStore } from '@/stores/systemPrompt'
import { computed, onMounted, ref } from 'vue'
import { watch } from 'vue'

const systemPromptStore = useSystemPromptStore()
const system_prompt = computed({
  get: () => systemPromptStore.systemPrompts,
  set: (val) => {
    systemPromptStore.systemPrompts = val
  }
})
const isLoading = ref(false)
const isSuccess = ref(false)

watch(() => system_prompt.value.temperature, (newVal) => {
  const slider = document.querySelector<HTMLInputElement>('input.custom-slider')
  if (slider) {
    // เปลี่ยนค่า slider ให้ตรงกับ temperature ที่พิมพ์มา
    slider.value = String(newVal)
    updateSliderFill(slider)
  }
})


onMounted(async () => {
  await systemPromptStore.fetchSystemPrompts()
  setTimeout(() => {
    const slider = document.querySelector<HTMLInputElement>('input.custom-slider')
    if (slider) updateSliderFill(slider)
  }, 0)
})


function openModal() {
  isSuccess.value = true;
  setTimeout(() => {
    isSuccess.value = false;
  }, 2000); // แสดง 3 วินาที แล้วซ่อน
}


function closeModal() {
  isSuccess.value = false;
}

function validateInput() {
  const value = parseFloat(system_prompt.value.temperature);

  if (value < 0 || value > 1 || isNaN(value)) {
    system_prompt.value.temperature = ''; // Reset invalid input
  }
}

// เปลี่ยนฟังก์ชันรับ HTMLInputElement แทน Event
function updateSliderFill(target: HTMLInputElement) {
  const value = parseFloat(target.value);
  if (isNaN(value)) return;

  const min = parseFloat(target.min);
  const max = parseFloat(target.max);
  const percentage = ((value - min) / (max - min)) * 100;

  // ✅ อัปเดตสีของแถบ Slider
 target.style.background = `linear-gradient(to right, #E43A32 ${percentage}%, #d1d5db ${percentage}%)`;

  // ✅ อัปเดตกรอบแสดงค่า
  const valueDisplay = document.getElementById('slider-value');
  const sliderRect = target.getBoundingClientRect();

  if (valueDisplay && sliderRect.width) {
    const thumbOffset = sliderRect.width * (percentage / 100);
    valueDisplay.style.left = `${thumbOffset}px`;
    valueDisplay.textContent = value.toFixed(2);
  }
}



async function handleSave() {
  console.log('handleSave called');
  console.log('system_prompt.value:', system_prompt.value);

  if (!system_prompt.value.id) {
    console.log('Creating new system prompt with:', {
      content: system_prompt.value.content,
      temperature: system_prompt.value.temperature,
    });

    await systemPromptStore.createSystemPrompt({
      content: system_prompt.value.content,
      temperature: system_prompt.value.temperature,
    });

    console.log('New system prompt created');
    openModal();
  } else {
    console.log('Saving existing system prompt with ID:', system_prompt.value.id);
    isLoading.value = true;

    try {
      await systemPromptStore.saveSystemPrompt({
        id: system_prompt.value.id,
        content: system_prompt.value.content,
        temperature: system_prompt.value.temperature,
      });

      console.log('System prompt saved successfully');
    } catch (error) {
      console.error('Error saving system prompt:', error);
    } finally {
      openModal();
      isLoading.value = false;
      console.log('Finished saving system prompt');
    }
  }
}

</script>

<style scoped>
@keyframes scaleIn {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

.animate-scaleIn {
  animation: scaleIn 0.3s ease-out forwards;
}

.animate-bounceIn {
  animation: bounceIn 0.5s ease-out forwards;
}

</style>

