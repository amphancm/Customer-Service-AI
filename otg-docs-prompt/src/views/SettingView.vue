<template>
  <div class="flex flex-col p-4 min-h-screen "> <!-- สีพื้นตามภาพ -->
    <!-- Header -->
    <!-- <div class="h-12 flex items-center p-20">
      <h3 class="font-jeju text-2xl text-black">Setting</h3>
    </div> -->

    <!-- Main Container -->
    <div class="w-full p-10 ml-10">
      <h3 class="font-bold text-2xl mt-15 mb-8 text-black">Setting</h3>
      <!-- Line bot Setting -->
      <section class="mb-8">
        <div class="mb-8 border-b pb-2">
          <div class="flex items-center justify-start gap-8 mb-4">
            <h5 class="font-Promt text-textColor text-base w-56 ">Line Bot Setting</h5>
            <label class="relative inline-flex cursor-pointer items-center">
              <input id="switch-line" type="checkbox" class="peer sr-only" v-model="isLineTokenEnabled" />
              <div class="relative w-[47px] h-[28px] rounded-[16px] border bg-slate-200
                  after:absolute after:top-[4px] after:left-[4px] after:h-[18px] after:w-[18px]
                  after:rounded-full after:border after:border-gray-300 after:bg-gray-400
                  after:transition-all after:content-['']
                  peer-checked:bg-customSildboxred peer-checked:after:bg-white
                  peer-checked:after:translate-x-[19px] peer-focus:ring-customSildboxred">
              </div>
            </label>
            <span class="font-Promt text-textColor text-sm ml-12">Enable Line Issue Token</span>
          </div>

          <div v-if="isLineTokenEnabled" class="flex flex-col gap-5 pl-12">
            <div class="flex items-center gap-4">
              <label class="w-48 font-Promt text-textColor text-sm">Line Issue Token</label>
              <input
                v-model="settingStore.Settings.line_key"
                :type="showLineKey ? 'text' : 'password'"
                class="flex-grow max-w-[300px] px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter Line API Key"
              />
              <button type="button" @click="showLineKey = !showLineKey" class="text-gray-500">
                <span v-if="showLineKey">
                  <img src="@/assets/icons/eye 2.png" alt="Hide" width="20" height="20" />
                </span>
                <span v-else>
                  <img src="@/assets/icons/visibility-off 3.png" alt="Show" width="20" height="20" />
                </span>

              </button>
            </div>
            <div class="flex items-center gap-4">
              <label class="w-48 font-Promt text-textColor text-sm">Line Secret Channel Key</label>
              <input
                v-model="settingStore.Settings.line_secret"
                :type="showLineSecret ? 'text' : 'password'"
                class="mb-3 flex-grow max-w-[300px] px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter Secret Channel Key"
              />
              <button type="button" @click="showLineSecret = !showLineSecret" class="text-gray-500">
                <span v-if="showLineKey">
                  <img src="@/assets/icons/eye 2.png" alt="Hide" width="20" height="20" />
                </span>
                <span v-else>
                  <img src="@/assets/icons/visibility-off 3.png" alt="Show" width="20" height="20" />
                </span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Facebook Bot Setting -->
      <section class="mb-8">
        <div class="mb-8 border-b pb-2">
          <div class="flex items-center justify-start gap-8 mb-4">
            <h5 class="font-Promt text-textColor text-base w-56">Facebook Bot Setting</h5>
            <label class="relative inline-flex cursor-pointer items-center">
              <input id="switch-facebook" type="checkbox" class="peer sr-only" v-model="isFacebookTokenEnabled" />
              <div class="relative w-[47px] h-[28px] rounded-[16px] border bg-slate-200
                  after:absolute after:top-[4px] after:left-[4px] after:h-[18px] after:w-[18px]
                  after:rounded-full after:border after:border-gray-300 after:bg-gray-400
                  after:transition-all after:content-['']
                  peer-checked:bg-customSildboxred peer-checked:after:bg-white
                  peer-checked:after:translate-x-[19px] peer-focus:ring-customSildboxred">
              </div>
            </label>
            <span class="font-Promt text-textColor text-sm ml-12">Enable Facebook Issue Token</span>
          </div>

          <div v-if="isFacebookTokenEnabled" class="flex flex-col gap-5 pl-12">
            <div class="flex items-center gap-4">
              <label class="w-48 font-Prmot text-textColor text-sm">Facebook Token</label>
              <input
                v-model="settingStore.Settings.facebook_token"
                type="text"
                class="flex-grow max-w-[300px] px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter Facebook Token"
              />

            </div>
            <div class="flex items-center gap-4">
              <label class="w-48 font-Promt text-textColor text-sm">Password Verify</label>
              <div class="flex flex-grow gap-3">
                <input
                  v-model="settingStore.Settings.facebook_verify_password"
                  type="text"
                  class="flex-grow max-w-[260px] px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Password Verify"
                />

                <button @click="generateFacebookPassword()"
                  class="w-[82px] h-[42px] bg-customSildboxred hover:bg-red-500 text-white rounded-[8px] flex justify-center items-center text-sm"
                  >
                  Generate
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Greeting Mode -->
      <section class="mb-8">
        <div class="mb-8 border-b pb-4">
          <div class="flex items-center justify-start gap-8 mb-4">
            <h5 class="font-Promt text-textColor text-base w-56">Greeting Mode</h5>
            <label class="relative inline-flex cursor-pointer items-center">
              <input type="checkbox" class="peer sr-only" v-model="isGreetingEnabled" />
              <div class="relative w-[47px] h-[28px] rounded-[16px] border bg-slate-200
                  after:absolute after:top-[4px] after:left-[4px] after:h-[18px] after:w-[18px]
                  after:rounded-full after:border after:border-gray-300 after:bg-gray-400
                  after:transition-all after:content-['']
                  peer-checked:bg-customSildboxred peer-checked:after:bg-white
                  peer-checked:after:translate-x-[19px] peer-focus:ring-customSildboxred">
              </div>
            </label>
            <span class="font-Promt text-textColor text-sm ml-12">First Conversation with AI</span>
          </div>

          <div v-if="isGreetingEnabled" class="flex items-center gap-4 pl-12">
            <label class="w-48 font-Promt text-textColor text-sm">Greeting Prompt</label>
            <input
              v-model="settingStore.Settings.greeting_prompt"
              type="text"
                class="flex-grow max-w-[300px] px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Greeting Prompt"
              />
          </div>
        </div>
      </section>

      <!-- Product Setting -->
      <section class="mb-8 border-b pb-4">
        <div class="flex items-center justify-start gap-8">
          <h5 class="font-Promt text-textColor text-base w-56">Product Setting</h5>
          <label class="relative inline-flex cursor-pointer items-center">
            <input type="checkbox" class="peer sr-only" v-model="isProductTokenEnabled" />
            <div class="relative w-[47px] h-[28px] rounded-[16px] border bg-slate-200
                after:absolute after:top-[4px] after:left-[4px] after:h-[18px] after:w-[18px]
                after:rounded-full after:border after:border-gray-300 after:bg-gray-400
                after:transition-all after:content-['']
                peer-checked:bg-customSildboxred peer-checked:after:bg-white
                peer-checked:after:translate-x-[19px] peer-focus:ring-customSildboxred">
            </div>
          </label>
          <span class="font-Promt text-textColor text-sm ml-12">Enable Product Placement in Answer</span>
        </div>
      </section>

      <!-- Feedback Report Setting -->
      <section class="mb-8 border-b pb-4">
        <div class="flex items-center justify-start gap-8">
          <h5 class="font-Promt text-textColor text-base w-56">Feedback Report Setting</h5>
          <label class="relative inline-flex cursor-pointer items-center">
            <input type="checkbox" class="peer sr-only" v-model="isOrderTokenEnabled" />
            <div class="relative w-[47px] h-[28px] rounded-[16px] border bg-slate-200
                after:absolute after:top-[4px] after:left-[4px] after:h-[18px] after:w-[18px]
                after:rounded-full after:border after:border-gray-300 after:bg-gray-400
                after:transition-all after:content-['']
                peer-checked:bg-customSildboxred peer-checked:after:bg-white
                peer-checked:after:translate-x-[19px] peer-focus:ring-customSildboxred">
            </div>
          </label>
          <span class="font-Promt text-textColor text-sm ml-12">Create feedback report from user</span>
        </div>
      </section>

      <!-- Replace the Server/Local Model Section with this: -->
      <h2 class="text-lg font-bold mb-2 text-left">Server Selection</h2>

      <div class="card max-w-2xl my-8 p-6 border rounded-lg shadow-lg bg-[#F8FAFC]"
        style="width: 785px; height: 360px; top: 6251px; left: 10564px; border-radius: 20px; opacity: 1; transform: rotate(0deg);"
      >
        <!-- RADIO GROUP -->
        <div class="radio-group flex gap-4 mb-4 justify-center items-center  ">
          <div class="radio-option cursor-pointer flex items-center gap-2" :class="{ 'active': currentTab === 'api' }"
            @click="currentTab = 'api'">
            <div class="red-dot" :style="currentTab === 'api' ? {} : inactiveDotStyle"></div>
            <span>Api Model</span>
          </div>

          <div class="radio-option cursor-pointer flex items-center gap-2" :class="{ 'active': currentTab === 'local' }"
            @click="currentTab = 'local'">
            <div class="red-dot" :style="currentTab === 'local' ? {} : inactiveDotStyle"></div>

            <span>Local Model</span>
          </div>
        </div>


        <!-- API CARD -->
        <div v-show="currentTab === 'api'" id="apiCard">
          <div class="form-control relative mt-3 flex items-center ">
            <label for="domain-select" class="mr-2 w-32">Domain Name</label>
            <select id="domain-select" v-model="selectedApiDomain"
              class="w-full border rounded px-3 py-2 cursor-pointer"
             :class="selectedApiDomain === '' ? 'text-gray-400' : 'text-black'"
              >
              <option v-for="domain in apiDomains" :key="domain.value" :value="domain.value" :disabled="domain.value == '' " >
                {{ domain.label }}{{ domain.value !== '' ? ` (${domain.value})` : '' }}
              </option>

            </select>
          </div>


          <div class="form-control relative mt-3 flex items-center ">
            <label class="mr-2 w-32">API Key</label>
            <input :type="showApiKey ? 'text' : 'password'" v-model="apiKey" placeholder="Enter API Key"
              class="w-full px-2 py-1 border rounded">
            <span class="toggle-eye absolute right-2 top-3 cursor-pointer" @click="showApiKey = !showApiKey">
              <img v-if="showApiKey" src="@/assets/icons/eye 2.png" alt="Hide" width="20" height="20" />
              <img v-else src="@/assets/icons/visibility-off 3.png" alt="Show" width="20" height="20" />
            </span>
          </div>


          <div class="form-control relative mt-3 flex items-center ">
            <label class="mr-2 w-32 ">Model Name</label>
            <select v-model="apiModel" class="w-full px-2 py-1 border rounded " :class="apiModel === 'Select Model Name' ? 'text-gray-400' : 'text-black'">
              <option v-for="model in apiModelOptions" :key="model" :disabled="model == 'Select Model Name' " >{{ model }}
              </option>
            </select>

          </div>

          <!-- <div class="form-control relative mt-3">
            <label>API Key</label>
            <input :type="showApiKey ? 'text' : 'password'" v-model="apiKey" placeholder="Enter API Key"
              class="w-full px-2 py-1 border rounded" />
            <span class="toggle-eye absolute right-2 top-7 cursor-pointer" @click="showApiKey = !showApiKey">
              {{ showApiKey ? '🙈' : '👁️' }}
            </span>
          </div> -->
        </div>


        <!-- LOCAL CARD -->
        <div v-show="currentTab === 'local'" id="localCard">
          <div class="form-control mb-3 flex items-center mr-10">
            <label class="mr-2 w-32">Model Name</label>
            <select v-model="localModel" class="w-full px-2 py-1 border rounded" :class="localModel === 'Select Model Name' ? 'text-gray-400' : 'text-black'">
              <option v-for="model in localModelOptions" :key="model"
               :disabled="model == 'Select Model Name' "
                >{{ model }}
              </option>
            </select>
          </div>


          <!-- <label>Domain Name</label>
          <div class="form-control domain-option flex items-center gap-2" @click="selectedApiDomain = domain.value"
            :class="{ active: selectedApiDomain === domain.value }">
            <div class="red-dot"></div>
            <span class="cursor-pointer" @click="selectDomain('ollama')">ollama</span>
          </div> -->
          <!-- <label>Domain Name</label>
          <div class="form-control domain-option flex items-center gap-2 cursor-pointer" v-for="domain in apiLocal"
            :key="domain.value" @click="selectedApiDomain = domain.value"
            :class="{ active: selectedApiDomain === domain.value }">
            <div class="red-dot" :style="selectedApiDomain === domain.value ? {} : inactiveDotStyle"></div>
            {{ domain.label }}
            <span class="text-xs text-gray-400 ml-2">{{ domain.value }}</span>
          </div> -->

          <!-- <div v-show="currentTab === 'local'" id="localCard"></div>
          <div class="">
            <label></label>

          </div> -->
        </div>

        <button
          class="bg-customSildboxred hover:bg-red-600 text-white px-6 py-3 rounded-xl font-jeju flex justify-center items-center gap-2 translate-x-60 translate-y-[30px]"
          @click="handleSave">
          <img src="/src/assets/icons/disk (2).png" alt="Save Icon" class="h-5 w-5" />
          Save
        </button>
      </div>
      <!-- End card -->
    </div>

    <!-- Save Button -->
    <!-- <div class="flex justify-center w-full -translate-x-64">
      <button
        class="bg-customSildboxred hover:bg-red-600 text-white px-6 py-3 rounded-md font-jeju flex items-center gap-2"
        @click="handleSave">
        <img src="/src/assets/icons/iconSave.png" alt="Save Icon" class="h-5 w-5" />
        Save
      </button>
    </div> -->

    <!-- Loading Overlay -->
    <div v-if="isLoading"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-xl font-jeju">
      Loading...
    </div>



    <!-- Success Modal -->
    <div v-if="isSuccess" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center ">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm text-center font-jeju  ">
        <h2 class="text-lg mb-4">Save Successfully!</h2>
        <button class="bg-red-600 px-4 py-2 rounded-xl text-white hover:bg-red-700 " @click="closeModal">
          Close
        </button>
      </div>
    </div>
  </div>

</template>


<script lang="ts" setup>
import { useSettingStore } from '@/stores/setting'
import { computed, nextTick, onMounted, ref } from 'vue'

const settingStore = useSettingStore()

// --- Model/Domain Tab UI State ---
const currentTab = ref('api')
const inactiveDotStyle = 'background: #ccc; border: 1px solid #aaa;'
const showApiKey = ref(false)

const apiModelOptions = computed(() => {
  if (selectedApiDomain.value === 'https://api.together.xyz/v1') {
    return [
      'Qwen/Qwen2.5-72B-Instruct-Turbo',
      'ngamthip98/lora-datasetv02-Llama-3.1-8B-customer-service-chatbot'
    ]
  } else if (selectedApiDomain.value === 'https://openrouter.ai/api/v1') {
    return [
      'deepseek/deepseek-chat-v3-0324:free',
      'google/gemini-2.5-pro-preview',
      'mistralai/mistral-7b-instruct-v0.3'
    ]
  } else if (selectedApiDomain.value === 'mock_ollama') {
    return ['tinyllama:latest', 'gemma2:2b']
  } else if (selectedApiDomain.value === 'mock_vllm') {
    return ['tinyllama:latest', 'gemma2:2b']
  }
  return ['Select Model Name']
})

const apiDomains = ref([
  { label: 'Select Domain Name', value: '' },
  { label: 'TogetherAI', value: 'https://api.together.xyz/v1' },
  { label: 'OpenRouter', value: 'https://openrouter.ai/api/v1' }
])

const localModelOptions = ref([
  'Select Model Name',
  'tinyllama:latest',
  'gemma2:2b'
])

const apiModel = computed({
  get: () => settingStore.Settings.server?.modelname || apiModelOptions.value[0],
  set: val => {
    if (!settingStore.Settings.server) {
      settingStore.Settings.server = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.server.modelname = val
  }
})

const selectedApiDomain = computed({
  get: () => settingStore.Settings.server?.domainname || (apiDomains.value.length > 0 ? apiDomains.value[0].value : ''),
  set: val => {
    if (!settingStore.Settings.server) {
      settingStore.Settings.server = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.server.domainname = val
  }
})

const apiKey = computed({
  get: () => settingStore.Settings.server?.apikey || '',
  set: val => {
    if (!settingStore.Settings.server) {
      settingStore.Settings.server = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.server.apikey = val
  }
})

const localModel = computed({
  get: () => settingStore.Settings.local?.modelname || 'Select Model Name',
  set: val => {
    if (!settingStore.Settings.local) {
      settingStore.Settings.local = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.local.modelname = val
  }
})

const selectedLocalDomain = computed({
  get: () => settingStore.Settings.local?.domainname || '',
  set: val => {
    if (!settingStore.Settings.local) {
      settingStore.Settings.local = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.local.domainname = val
  }
})

// Activation toggles
const isLineTokenEnabled = computed({
  get: () => !!settingStore.Settings.line_activate,
  set: v => (settingStore.Settings.line_activate = v)
})
const isFacebookTokenEnabled = computed({
  get: () => !!settingStore.Settings.fb_activate,
  set: v => (settingStore.Settings.fb_activate = v)
})
const isProductTokenEnabled = computed({
  get: () => !!settingStore.Settings.product_activate,
  set: v => (settingStore.Settings.product_activate = v)
})
const isOrderTokenEnabled = computed({
  get: () => !!settingStore.Settings.feedback_activate,
  set: v => (settingStore.Settings.feedback_activate = v)
})
const isGreetingEnabled = computed({
  get: () => !!settingStore.Settings.greeting_activate,
  set: v => (settingStore.Settings.greeting_activate = v)
})

const isLoading = ref(false)
const isSuccess = ref(false)
const showLineKey = ref(false)
const showLineSecret = ref(false)

onMounted(async () => {
  await settingStore.fetchSettings()
  if (settingStore.Settings.server?.enabled) currentTab.value = 'api'
  else if (settingStore.Settings.local?.enabled) currentTab.value = 'local'
})

function openModal() {
  isSuccess.value = true
}
function closeModal() {
  isSuccess.value = false
}

async function generateFacebookPassword() {
  settingStore.Settings.facebook_verify_password = Math.random().toString(36).slice(-8)
  await nextTick()
}

async function handleSave() {
  if (currentTab.value === 'api') {
    if (!settingStore.Settings.server) {
      settingStore.Settings.server = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.server.enabled = true
    // ✅ บังคับอัปเดตค่า modelname ก่อน save
    settingStore.Settings.server.modelname = apiModel.value

    settingStore.Settings.local = { enabled: false, domainname: '', apikey: '', modelname: '' }
  } else {
    if (!settingStore.Settings.local) {
      settingStore.Settings.local = { enabled: true, domainname: '', apikey: '', modelname: '' }
    }
    settingStore.Settings.local.enabled = true
    const ollamaHost = import.meta.env.VITE_OLLAMA_HOST
    settingStore.Settings.local.domainname = ollamaHost
    settingStore.Settings.local.apikey = 'ollama'
    // ✅ บังคับอัปเดตค่า modelname local
    settingStore.Settings.local.modelname = localModel.value

    settingStore.Settings.server = { enabled: false, domainname: '', apikey: '', modelname: '' }
  }

  // Prepare the save data with nested structure
  const saveData = {
    id: settingStore.Settings.id,
    time_activate: settingStore.Settings.time_activate ?? false,
    line_activate: settingStore.Settings.line_activate ?? false,
    fb_activate: settingStore.Settings.fb_activate ?? false,
    product_activate: settingStore.Settings.product_activate ?? false,
    feedback_activate: settingStore.Settings.feedback_activate ?? false,
    greeting_activate: settingStore.Settings.greeting_activate ?? false,
    line_key: settingStore.Settings.line_key ?? '',
    line_secret: settingStore.Settings.line_secret ?? '',
    facebook_token: settingStore.Settings.facebook_token ?? '',
    facebook_verify_password: settingStore.Settings.facebook_verify_password ?? '',
    greeting_prompt: settingStore.Settings.greeting_prompt ?? '',
    server: settingStore.Settings.server,
    local: settingStore.Settings.local
  }

  isLoading.value = true
  try {
    if (!settingStore.Settings.id) {
      await settingStore.createSetting(saveData)
    } else {
      await settingStore.saveSetting(saveData)
    }
    openModal()
  } catch (error) {
    console.error('Error saving setting:', error)
    alert('Failed to save settings. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>



<style>
/* Add to your <style> section or global CSS */
.radio-option.active {
  font-weight: bold;
}

.red-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #e53e3e;
  border: 2px solid #e53e3e;
  display: inline-block;
}

.domain-option {
  margin-bottom: 0.5rem;
}

.toggle-eye {
  cursor: pointer;
}

.radio-group {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  justify-content: center;
  align-items: center;
}

.radio-option {
  border: 1px solid #ccc;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s, border-color 0.3s;
}

.radio-option.active {
  border-color: #DE4640;
  background-color: #fde5e3;
}

.red-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: white;
  border: 2px solid black;
  transition: background-color 0.3s, border-color 0.3s;
}

.radio-option.active .red-dot {
  background-color: #DE4640;
  border-color: #DE4640;
}

.form-control {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
  font-weight: 500;
}

input[type="text"],
input[type="password"],
select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.domain-option {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
  font-weight: 500;
}

.domain-option.active {
  background-color: #fde5e3;
  border-color: #DE4640;
}

.red-dot {
  background-color: white;
  border: 2px solid black;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  transition: background-color 0.3s, border-color 0.3s;
}

.domain-option.active .red-dot {
  background-color: #DE4640;
  border-color: #DE4640;
}

.toggle-eye {
  position: absolute;
  right: 10px;
  top: 34px;
  cursor: pointer;
}

.form-control {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
  font-weight: 500;
}

select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.domain-option {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
  font-weight: 500;
}

.domain-option.active {
  background-color: #fde5e3;
  border-color: #DE4640;
}

.red-dot {
  background-color: white;
  border: 2px solid black;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  transition: background-color 0.3s, border-color 0.3s;
}

.domain-option.active .red-dot {
  background-color: #DE4640;
  border-color: #DE4640;
}

.red-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid black;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.red-dot.active {
  background-color: #DE4640;
  /* สีส้ม */
  border-color: #DE4640;
}
</style>
