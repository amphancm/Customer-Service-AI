<template>
  <div class="flex w-full">
    <div class="bg-customeChat flex-none w-[260px] ">
      <div class="h-screen flex flex-col p-4 ">
        <div class="flex-none w-full text-center ">

        </div>
        <div class="flex-grow py-4 overflow-y-auto mb-2">
          <div v-for="(chatRoom, index) in Object.values(chatRooms).reverse()" :key="index"
            class="w-full h-14 rounded-xl mb-2 flex items-center px-4 cursor-pointer justify-between relative hover:bg-gray-400">
            <div class="flex items-center w-full">
              <div @click="selectRoom(Object.values(chatRooms).length - 1 - index)"
                class="flex items-center space-x-2 w-4/5 cursor-pointer">
                <div class="pl-[10px]">
                  <span>New Chat {{ index + 1 }}</span>
                  <p class="truncate whitespace-nowrap w-40">
                    {{ chatRoom.chatOption.name }}
                  </p>
                </div>
              </div>

              <div class="w-1/5 flex justify-end">
                <button @click.stop="toggleSubmenu(index)">
                  <svg class="w-6 h-6 text-gray-600 hover:text-black" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      d="M6 10a2 2 0 114 0 2 2 0 01-4 0zm6 0a2 2 0 114 0 2 2 0 01-4 0zm6 0a2 2 0 114 0 2 2 0 01-4 0z" />
                  </svg>
                </button>
              </div>
            </div>



            <div class="relative">
              <div v-if="isSubmenuVisible && isSubmenuVisibleIndex == index"
                class="absolute mb-1  bg-customeChat border rounded-xl shadow-xl w-24 right-0 z-50">
                <ul class="text-textColor">
                  <li class="px-6 py-1 hover:text-gray-500 rounded cursor-pointer">
                    <h6>Rename </h6>
                  </li>
                  <li class="px-6 py-1 hover:text-gray-500 rounded cursor-pointer" @click="openModalSystemPrompt">
                    <h6>Prompt</h6>
                  </li>
                  <li class="px-6 py-1 hover:text-red_jetts rounded cursor-pointer" @click="openModalDelete">
                  <h6>Delete</h6>
                </li>
                </ul>
              </div>
            </div>
          </div>

        </div>
        <div class="flex-none">
          <button class="bg-red_jetts text-white px-4 py-2 rounded-full w-full hover:bg-red-600"
            @click="openCreateModalSystemPrompt()">
            Create Room
          </button>
        </div>
      </div>
    </div>
    <div class="flex-auto w-full">
      <div class="h-screen flex flex-col p-4 mt-4">
        <div class="h-12 flex items-center justify-between">
          <div class="relative">
            <button class="text-black font-bold px-4 py-2 rounded hover:bg-gray-200 transition" @click="toggleSubmenu"
              ref="targetRef">
              PROMPT
            </button>
          </div>

        </div>
        <div class="flex flex-grow parent overflow-y-auto w-full rounded-md">
          <div class=" w-full h-full flex flex-col" ref="messagesContainer">
            <div
              v-if="chatRoomsList.length > 0 && chatRoomsList[selectIndexing]?.messages && chatRoomsList[selectIndexing].messages.length > 0"
              class="flex-1 overflow-y-auto max-h-full px-2">
              <div v-for="(message, index) in chatRoomsList[selectIndexing].messages" :key="index" :class="[
                'mb-4', // เพิ่มช่องว่างระหว่างแต่ละข้อความ
                'flex items-end',
                message.role === 'user' ? 'justify-end' : 'justify-start',
                'gap-2' // เพิ่ม gap ระหว่าง avatar กับ bubble
              ]">
                <!-- Assistant avatar (left) -->
                <div v-if="message.role !== 'user'" class="mr-2 flex-shrink-0">
                  <Icon icon="mdi:robot" width="32" height="32" class="text-gray-400" />
                </div>
                <!-- Message bubble -->
                <div :class="[
                  'max-w-[75%] px-5 py-3 rounded-2xl shadow',
                  message.role === 'user'
                    ? 'bg-[#F9EAEA] text-black rounded-br-none'
                    : 'bg-white text-black rounded-bl-none border'
                ]" style="margin-bottom: 2px;">
                  <template v-if="message.type === 'text'">
                    <template v-if="/^https?:\/\/.*\.(png|jpg|jpeg|gif|webp|svg)$/i.test(message.content)">
                      <a :href="message.content" target="_blank" rel="noopener">
                        <img :src="message.content" alt="image" class="w-40 h-40 object-cover rounded-md mb-2" />
                      </a>
                    </template>
                    <!-- Check if content is a markdown image link -->
                    <template v-else-if="extractImageUrlFromMarkdown(message.content)">
                      <a :href="extractImageUrlFromMarkdown(message.content)" target="_blank" rel="noopener">
                        <img :src="extractImageUrlFromMarkdown(message.content)" alt="image"
                          class="w-40 h-40 object-cover rounded-md mb-2" />
                      </a>
                    </template>
                    <template v-else>
                      <pre v-if="message.role !== 'user'"
                        class="whitespace-pre-wrap break-words font-mono text-base leading-relaxed">
                        {{ message.content }}
                      </pre>
                      <p v-else v-for="(messager, idx) in message.content.split('\n')" :key="idx"
                        class=" text-[#404040] ">
                        {{ messager }}
                      </p>
                    </template>
                  </template>
                  <template v-else>
                    <img :src="message.content" alt="image" class="w-40 h-40 object-cover rounded-md" />
                  </template>
                </div>
                <!-- User avatar (right) -->
                <div v-if="message.role === 'user'" class="ml-2 flex-shrink-0">
                  <Icon icon="mdi:account-circle" width="32" height="32" class="text-gray-400" />
                </div>
              </div>
              <div v-if="isAssistantTyping" class="assistant">
                <div class="loader">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
              <div v-if="isUserTyping" class="user">
                <div class="loader">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
            <div v-else class="flex-1 flex flex-col items-center justify-center text-gray-400 px-4">
              <p class=" text-xl font-bold text-black mb-2">What can i help with?</p>
              <div class="w-full flex justify-center mt-6">
                <div class="relative w-full max-w-4xl">
                 <input
                      type="text"
                      class="w-full p-4 pr-12 rounded-xl bg-customeChat border-2 border-gray-300 text-black focus:outline-none focus:ring-2 focus:ring-customSildboxred appearance-none overflow-hidden"
                    placeholder="Ask anything about company..." v-model="inputMessage"
                    @keydown.enter="handleSubmitMessage" />


                        <div class="flex space-x-4">
                          <div class=" mt-[10px] w-[166px] h-[46px] bg-white rounded-2xl flex items-center justify-center border border-gray-300 shadow hover:bg-gray-600">
                            <p class="text-[15px]  text-black">About Company</p>
                          </div>
                          <div class=" mt-[10px] w-[230px] h-[46px] bg-white rounded-2xl flex items-center justify-center border border-gray-300 shadow hover:bg-gray-600">
                            <p class="text-[15px]  text-black">About Role Responsibility</p>
                          </div>
                          <div class=" mt-[10px] w-[166px] h-[46px] bg-white rounded-2xl flex items-center justify-center border border-gray-300 shadow hover:bg-gray-600">
                            <p class="text-[15px]  text-black">About Project...</p>
                          </div>
                        </div>

                  <button
                    class=" absolute top-1/2 right-3 -translate-y-1/2 mt-[-28px] bg-red_jetts rounded-2xl p-2 cursor-pointer hover:bg-red-700"
                    @click="handleSubmitMessage" aria-label="Send message">
                    <Icon icon="material-symbols:send" width="24" height="24" class="text-white" />
                  </button>
                </div>
              </div>
              <div v-if="isAssistantTyping" class="assistant">
                <div class="loader">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
              <div v-if="isUserTyping" class="user">
                <div class="loader">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="chatRoomsList.length > 0 && chatRoomsList[selectIndexing]?.messages && chatRoomsList[selectIndexing].messages.length > 0"
          class="h-16 w-full flex items-center mb-4 px-2">
          <input type="text" class="flex-1 p-4 rounded-full bg-customeChat border-2 mr-2" placeholder="Input Here......"
            v-model="inputMessage" @keydown.enter="handleSubmitMessage" />
          <button
            class="flex items-center border-2 rounded-full border-white p-3 outline-slate-500 bg-red_jetts cursor-pointer hover:bg-red-700"
            @click="handleSubmitMessage">
            <Icon icon="material-symbols:send" width="24" height="24" class="text-white" />
          </button>
        </div>
      </div>
    </div>
  </div>
  <Modal :isOpen="isModalSystemPromptOpen" title="System Prompt Edit" @close="closeModalSystemPrompt"
    @confirm="handleConfirmSystemPrompt">
    <template #body>
      <div class="w-full max-w-[1200px]  p-7 rounded-3xl shadow-md">

        <!-- Name label and input แยกบรรทัด -->
        <div class="mb-6">
          <label class="block text-lg text-textColor font-jeju mb-2">Name :</label>
          <input v-model="name"
            class="w-full max-w-[1200px] text-center px-4 py-2 rounded-md  border-4  text-textColor focus:outline-none focus:ring-2 focus:ring-customSildboxred"
            type="text" placeholder="Enter name" />
        </div>

        <!-- Temperature -->
        <div class="mb-8">
          <div class="flex items-center gap-8 mb-5">
            <label class="text-lg text-textColor font-jeju mr-10">Temperature</label>
            <input v-model.number="temperature" @input="validateInput" type="number" min="0" max="1" step="0.01"
              class="text-center max-w-xs px-4 py-2 rounded-full bg-customSystempromt text-textColor border-4 border-white  focus:outline-none focus:ring-2 focus:ring-customSildboxred no-spinner" />
          </div>

          <input type="range" min="0" max="1" step="0.01" v-model.number="temperature" class="custom-slider mb-6"
            @input="(e) => updateSliderFill(e.target as HTMLInputElement)" />
        </div>

        <!-- System Prompt label และ textarea แยกบรรทัด -->
        <div class="mb-8">
          <label class="block mb-2 text-xl text-textColor font-jeju">System Prompt</label>
          <textarea v-model="systemPrompt" rows="20"
            class="w-full p-4 rounded-lg  border border-black/20 text-textColor placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-customSildboxred"
            placeholder="Enter System Prompt"></textarea>
        </div>
      </div>

    </template>
  </Modal>

  <Modal :isOpen="isModalDeleteOpen" title="Confirm Delete" @close="closeModalDelete" :isAlert="true"
    @confirm="handleConfirmDelete">
    <template #body>
      <p>Do you want to delete ?</p>
    </template>
  </Modal>

  <div v-if="isSuccess" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-96">
      <h2 class="text-lg font-semibold text-green-600">Success!</h2>
      <p class="mt-2 text-gray-600">
        Your operation was completed successfully.
      </p>
      <div class="flex justify-end mt-4">
        <button @click="closeModal" class="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700">
          OK
        </button>
      </div>
    </div>
  </div>

</template>

<script lang="ts" setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import Modal from '../components/CustomModal.vue'
import { useChatRoomStore } from '@/stores/chatRooms'
import { Icon } from '@iconify/vue'
import { useSystemPromptStore } from '@/stores/systemPrompt'
import { useAuthenticationStore } from '@/stores/authentication'
import { useSettingStore } from '@/stores/setting'
import { useRouter } from 'vue-router'

const router = useRouter()
const settingStore = useSettingStore()

const selectIndexing = ref(0)
const isSubmenuVisible = ref(false)
const isSubmenuVisibleIndex = ref(0)
const name = ref('')
const systemPrompt = ref('')
const temperature = ref('')
const type = ref('')
const inputMessage = ref('')
const isSuccess = ref(false)

const isAssistantTyping = ref(false)
const isUserTyping = ref(false)
const targetRef = ref<HTMLElement | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)
let profile = {
  username: '',
  token: '',
}
const chatRoomsStore = useChatRoomStore()
const chatRooms = computed(() => chatRoomsStore.chatRoom) // Replace `chatRoom` with your actual state variable

const systemPromptStore = useSystemPromptStore()
const system_prompt = computed(() => systemPromptStore.systemPrompts)

const authentication = useAuthenticationStore()


watch(() => temperature.value, (newVal) => {
  const slider = document.querySelector<HTMLInputElement>('input.custom-slider');
  if (slider) {
    slider.value = String(newVal);
    updateSliderFill(slider);
  }
});

onMounted(() => {
  const slider = document.querySelector<HTMLInputElement>('input.custom-slider');
  if (slider) updateSliderFill(slider);
});


function updateSliderFill(target: HTMLInputElement) {
  const value = parseFloat(target.value);
  if (isNaN(value)) return;

  const min = parseFloat(target.min);
  const max = parseFloat(target.max);

  const percentage = ((value - min) / (max - min)) * 100;
  target.style.setProperty('--slider-percentage', percentage + '%');
}

function validateInput() {
  const value = parseFloat(temperature.value);

  if (value < 0 || value > 1 || isNaN(value)) {
    temperature.value = ''; // Reset invalid input
  }
}

let chatRoomsList: {
  id: string
  chatOption: { name: string; temperature: string; systemPrompt: string }
  messages: Array<{ type: string; role: string; content: string }>
}[] = []

onMounted(async () => {
  try {
    // Check settings first
    await settingStore.fetchSettings()

    // Check if any model is configured (server or local)
    const hasServerModel = settingStore.Settings.server?.enabled &&
      settingStore.Settings.server?.domainname &&
      settingStore.Settings.server?.apikey &&
      settingStore.Settings.server?.modelname

    const hasLocalModel = settingStore.Settings.local?.enabled &&
      settingStore.Settings.local?.domainname &&
      settingStore.Settings.local?.modelname

    // Check if legacy settings exist (fallback)
    const hasLegacySettings = settingStore.Settings.domainname &&
      settingStore.Settings.apikey &&
      settingStore.Settings.modelname

    if (!hasServerModel && !hasLocalModel && !hasLegacySettings) {
      alert('Please configure your AI model settings before using the chat.')
      await router.push('/setting')
      return
    }

    // Proceed with normal initialization if settings are configured
    profile = await authentication.getProfile();
    await chatRoomsStore.fetchChatRooms(profile)
    await systemPromptStore.fetchSystemPrompts()

    chatRoomsList = Object.values(chatRooms.value)
    selectIndexing.value = chatRoomsList.length > 0 ? chatRoomsList.length - 1 : 0;
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  } catch (error) {
    console.error('Error checking settings:', error)
    alert('Unable to load settings. Please configure your settings.')
    await router.push('/setting')
  }
  document.addEventListener('click', handleClickOutside)
  const slider = document.querySelector<HTMLInputElement>('input.custom-slider');
  if (slider) updateSliderFill(slider);
})

function openModal() {
  isSuccess.value = true;
}
function closeModal() {
  isSuccess.value = false;
}

watch(
  chatRooms,
  (newValue) => {
    chatRoomsList = Object.values(chatRooms.value)
  },
  { deep: true },
)

watch(inputMessage, (newValue) => {
  if (newValue.trim() !== '') {
    isUserTyping.value = true
  } else {
    isUserTyping.value = false
  }
})

async function handleSubmitMessage() {
  if (chatRoomsList.length == 0) {
    alert('Please create a chat room before sending a message.')
    return
  }
  const messageContent = inputMessage.value
  inputMessage.value = ''
  if (messageContent.trim() != '') {
    isAssistantTyping.value = true
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
    await chatRoomsStore.submitMessage({
      id: chatRoomsList[selectIndexing.value].id,
      systemPrompt: chatRoomsList[selectIndexing.value].chatOption.systemPrompt,
      temperature: chatRoomsList[selectIndexing.value].chatOption.temperature,
      message: messageContent,
    })
    isAssistantTyping.value = false
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }
}

function selectRoom(index: number) {
  selectIndexing.value = index
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function toggleSubmenu(index: number) {
  isSubmenuVisibleIndex.value = index
  isSubmenuVisible.value = !isSubmenuVisible.value

}

const handleClickOutside = (event: MouseEvent) => {
  if (targetRef.value && !targetRef.value.contains(event.target as Node)) {
    isSubmenuVisible.value = false
  }
}

// Modal State
const isModalSystemPromptOpen = ref(false)
const isModalDeleteOpen = ref(false)

async function openCreateModalSystemPrompt() {
  type.value = 'create'
  name.value = ''
  systemPrompt.value = system_prompt.value.content
  temperature.value = system_prompt.value.temperature

  type.value = 'create'
  await chatRoomsStore.createChatRooms({
    account_owner: profile.username,
    chatOption: {
      name: name.value,
      temperature: system_prompt.value.temperature,
      systemPrompt: system_prompt.value.content,
    },
    messages: [],
  })

  selectIndexing.value = chatRoomsList.length - 1

}

function openModalSystemPrompt(index) {
  selectIndexing.value = index
  type.value = 'edit'
  name.value = chatRoomsList[index].chatOption.name
  systemPrompt.value = chatRoomsList[index].chatOption.systemPrompt
  temperature.value = chatRoomsList[index].chatOption.temperature
  isModalSystemPromptOpen.value = true
}


function closeModalSystemPrompt() {
  isModalSystemPromptOpen.value = false
}

function openModalDelete() {
  isModalDeleteOpen.value = true
}

function closeModalDelete() {
  isModalDeleteOpen.value = false
}

async function handleConfirmSystemPrompt() {
  if (type.value == 'create') {
    await chatRoomsStore.createChatRooms({
      account_owner: profile.username,
      chatOption: {
        name: name.value,
        temperature: temperature.value,
        systemPrompt: systemPrompt.value,
      },
      messages: [],
    })
  } else {
    await chatRoomsStore.saveChatRooms({
      chatOption: {
        name: name.value,
        temperature: temperature.value,
        systemPrompt: systemPrompt.value,
      },
      id: chatRoomsList[selectIndexing.value].id,
    })
  }
  closeModalSystemPrompt()
  selectIndexing.value = chatRoomsList.length - 1
}

async function handleConfirmDelete() {
  await chatRoomsStore.deleteChatRooms(chatRoomsList[selectIndexing.value].id)
  selectIndexing.value = chatRoomsList.length - 1
  closeModalDelete()
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function extractImageUrlFromMarkdown(text: string): string | null {
  // Matches [text](http://...image.png)
  const match = text.match(/\[.*?\]\((https?:\/\/.*\.(?:png|jpg|jpeg|gif|webp|svg))\)/i)
  return match ? match[1] : null
}

const isSidebarOpen = ref(true)

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}





</script>

<style scoped>
.assistant {
  @apply bg-white max-w-96 rounded-md p-2 mb-4 text-wrap;
  width: fit-content;
  /* max-width: 400px; */
  word-wrap: break-word;
  /* Ensures long words are wrapped */
  overflow-wrap: break-word;
  /* Modern equivalent for wrapping text */
  white-space: normal;
}

.user {
  @apply bg-white max-w-96 rounded-md p-3 mb-4 text-wrap;
  margin-left: auto;
  /* Align to the right */
  width: fit-content;
  /* max-width: 400px; */
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}

/* The typewriter cursor effect */
@keyframes blink-caret {

  from,
  to {
    border-color: transparent;
  }

  50% {
    border-color: orange;
  }
}

.parent {
  @apply flex flex-col justify-end;
}

.loader {
  text-align: center;
}

.loader span {
  display: inline-block;
  vertical-align: middle;
  width: 10px;
  height: 10px;
  background: black;
  border-radius: 20px;
  animation: loader 0.8s infinite alternate;
}

.loader span:nth-of-type(2) {
  animation-delay: 0.2s;
}

.loader span:nth-of-type(3) {
  animation-delay: 0.6s;
}

@keyframes loader {
  0% {
    opacity: 0.9;
    transform: scale(0.5);
  }

  100% {
    opacity: 0.1;
    transform: scale(1);
  }
}

.message-bubble {
  margin-bottom: 8px;
  padding: 14px 20px;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  font-size: 1rem;
  line-height: 1.7;
}

.bg-red_jetts {
  background-color: #e53935;
}

.text-white {
  color: #fff;
}

.text-black {
  color: #222;
}

pre.whitespace-pre-wrap {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Sarabun';
  background: transparent;
  margin: 0;
  padding: 0;
  font-size: 1.05rem;
  line-height: 1.8;
}
</style>

<!-- เพิ่มใน <head> ของ index.html -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap" rel="stylesheet">
