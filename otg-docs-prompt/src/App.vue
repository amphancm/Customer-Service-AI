<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from "vue";
import { RouterLink, RouterView, useRoute } from 'vue-router';
import router from '@/router';
import { useAuthenticationStore } from "./stores/authentication";
import { Icon } from "@iconify/vue/dist/iconify.js";
import { useChatRoomStore } from "./stores/chatRooms";

const route = useRoute();

// Determine if the current route is the login page
const isLoginPage = computed(() => route.path === '/login');
const token = ref(localStorage.getItem("token"));
const authentication = useAuthenticationStore();
const chatroom = useChatRoomStore();
const isIconmenuVisible = ref(false);
const menuIcon = ref<HTMLElement | null>(null);
const isSidebarOpen = ref(JSON.parse(localStorage.getItem("isSidebarOpen") || "true")); // Persist sidebar state

const profile = computed(() => authentication.profile);

// Sidebar submenu state
const submenuOpen: Record<string, boolean> = reactive({
  chat: false,
  settings: false,
});

onMounted(() => {
  getProfile();
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

function toggleIconMenu() {
  isIconmenuVisible.value = !isIconmenuVisible.value;
}

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value;
  localStorage.setItem("isSidebarOpen", JSON.stringify(isSidebarOpen.value)); // Save state
}

const handleClickOutside = (event: MouseEvent) => {
  if (menuIcon.value && !menuIcon.value.contains(event.target as Node)) {
    isIconmenuVisible.value = false;
  }
};

function toggleSubmenu(menu: string) {
  submenuOpen[menu] = !submenuOpen[menu];
}

async function getProfile() {
  if (token.value) {
    await authentication.getProfile();
  } else {
    console.error("Token is missing in localStorage.");
    router.push({ path: "/login" }).catch((err) => console.error(err));
  }
}

function pushRouteLogin() {
  router.push({ name: 'login' }).catch((err) => console.error(err));
}

async function logout() {
  isIconmenuVisible.value = false;
  await chatroom.resetChatRooms();
  await authentication.logout();
  router.push({ path: "/login" }).catch((err) => console.error(err));
}
</script>

<template>
  <div>
    <div v-if="isLoginPage" class="h-screen  bg-gradient items-center justify-center">
      <RouterView />
    </div>
    <div v-else class="flex min-h-screen">
      <!-- Sidebar -->
      <div v-show="isSidebarOpen"
        class="flex-none min-h-screen customLight w-[250px] shadow-lg transition-all duration-300 relative bg-[#F2F2F2]">
        <div class="flex flex-col h-screen py-6 ">
          <h3
            class="flex justify-center items-center font-Promt text-2xl transition-transform duration-200 hover:scale-105">
            <img src="@/assets/icons/Rectangle 3466563.png" class="mr-2" width="50" height="50" alt="Documents" />
            <RouterLink to="/" class="text-customSildboxred font-bold mr-2"> Natachat</RouterLink>
           <span class="text-black font-bold ">AI</span>
          </h3>
          <!-- <div class="bg-gray-700 w-4/5 h-0.5 rounded-lg mx-auto mb-6"></div> -->

          <!-- Menu Items -->
          <div class="space-y-4 text-left px-10">
            <!-- Documents -->
            <RouterLink to="/docs" v-slot="{ isActive }">
              <h4
              class="flex items-center text-base px-4 py-2 rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black mb-4"
              :class="{ 'bg-customSildboxred text-black': isActive }">
             <img src="@/assets/icons/task-checklist.png" class="mr-3" width="20" height="20" alt="Documents" />
              Documents
            </h4>
            </RouterLink>

            <!-- System Prompt -->
            <RouterLink to="/system_prompt" v-slot="{ isActive }">
              <h4
                class="w-full flex items-center whitespace-nowrap text-base px-4 py-2 rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black mb-4"
                :class="{ 'bg-customSildboxred text-black': isActive }">
              <img src="@/assets/icons/bulb.png" class="mr-3" width="20" height="20" alt="System Prompt" />
                System Prompt
              </h4>
            </RouterLink>

            <!-- Product -->
            <RouterLink to="/products" v-slot="{ isActive }">
              <h4
                class="flex items-center text-base px-4 py-2 rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black mb-4"
                :class="{ 'bg-customSildboxredtext-black': isActive }">
               <img src="@/assets/icons/box-open-full.png" class="mr-3" width="20" height="20" alt="Product" />
                Product
              </h4>
            </RouterLink>

            <!-- User Feedback -->
            <RouterLink to="/issues" v-slot="{ isActive }">
              <h4
                class="w-full flex items-center whitespace-nowrap text-base px-4 py-2 rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black mb-4"
                :class="{ 'bg-customSildboxred text-black ': isActive }">
                <img src="@/assets/icons/users-alt.png" class="mr-3" width="20" height="20" alt="User Feedback" />
                User Feedback
              </h4>
            </RouterLink>

            <!-- Chat -->
             <RouterLink to="/" v-slot="{ isActive }">
            <h4>
              <button
                class="flex items-center justify-between whitespace-nowrap text-base px-4 py-2 w-full rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black mb-4"
                :class="{ 'bg-customSildboxred text-black': submenuOpen['chat'] }" @click="toggleSubmenu('chat')">
                <div class="flex items-center font-semibold ">
                  <img src="@/assets/icons/comment.png" class="mr-3" width="20" height="20" alt="Chat" />
                  Chat
                </div>
                <!-- <Icon icon="mdi:chevron-down" class="transition-transform duration-300"
                  :class="{ 'rotate-180': submenuOpen['chat'] }" /> -->
              </button>
            </h4>
            </RouterLink>


            <!-- Chat Submenu -->
            <transition>
              <div v-show="submenuOpen['chat']" class="ml-6 space-y-4 ss">
                <RouterLink to="/" v-slot="{ isActive }">
                  <!-- <h5
                    class="flex items-center text-base px-4 py-2 rounded font-semibold transition duration-200 hover:bg-customSildboxred hover:text-black mb-2"
                    :class="{ 'bg-customSildboxred text-black ': isActive }">
                    <Icon icon="/Users/jirapatsomseang/Desktop/llm_agent/otg-docs-prompt/src/assets/icons/Frame_14.png" class="mr-3" width="20" height="20" />
                    Chat
                  </h5> -->
                <!-- </RouterLink>
                <RouterLink to="/chat/line" v-slot="{ isActive }"> -->
                  <!-- <h5
                    class="flex items-center text-base px-4 py-2 rounded font-semibold transition duration-200 hover:bg-customSildboxred hover:text-black mb-2"
                    :class="{ 'bg-customSildboxred text-black ': isActive }">
                    <Icon icon="mdi:message-outline" class="mr-3" width="20" height="20" />
                    Line Chat
                  </h5> -->
                <!-- </RouterLink>
                <RouterLink to="/Debug" v-slot="{ isActive }"> -->
                  <!-- <h5
                    class="flex items-center text-base px-4 py-2 rounded font-semibold transition duration-200 hover:bg-customSildboxred hover:text-black"
                    :class="{ 'bg-customSildboxred text-black ': isActive }">
                    <Icon icon="mdi:bug-outline" class="mr-3" width="20" height="20" />
                    DEBUG
                  </h5> -->
                </RouterLink>
              </div>
            </transition>

            <!-- Settings -->
            <h4>
              <button
                class="flex items-center justify-between text-base px-4 py-2 w-full rounded-xl transition duration-200 hover:bg-customSildboxred hover:text-black"
                :class="{ 'bg-customSildboxred text-black ': submenuOpen['settings'] }" @click="toggleSubmenu('settings')">
                <div class="flex items-center font-semibold">
                  <img src="@/assets/icons/settings.png" class="mr-3" width="20" height="20" alt="Settings" />
                  Settings
                </div>
                <Icon icon="mdi:chevron-down" class="transition-transform duration-300"
                  :class="{ 'rotate-180': submenuOpen['settings'] }" />
              </button>
            </h4>
            <transition>
              <div v-show="submenuOpen['settings']" class="ml-6 space-y-2">
                <RouterLink to="/setting" v-slot="{ isActive }">
                  <h5 class="flex items-center mb-2 text-base px-4 py-2 rounded-xl font-semibold transition duration-200 hover:bg-customSildboxred hover:text-black"
                    :class="{ 'bg-customSildboxred text-black': isActive }">
                     <!-- <img src="@/assets/icons/file-invoice (1).png" class="mr-3" width="20" height="20" alt="Settings" /> -->
                    General
                  </h5>
                </RouterLink>
                <RouterLink to="/settings/account" v-slot="{ isActive }">
                  <h5 class="flex items-center text-base px-4 py-2 rounded-xl font-semibold transition duration-200 hover:bg-customSildboxred hover:text-black"
                    :class="{ 'bg-customSildboxred text-black': isActive }">
                     <!-- <img src="@/assets/icons/portrait.png" class="mr-3" width="20" height="20" alt="Settings" /> -->
                    account
                  </h5>
                </RouterLink>
              </div>
            </transition>
          </div>
        </div>

        <!-- Bottom Menu -->
        <div class="absolute bottom-0 w-full px-4 py-2 ">
          <div v-if="profile != null" class="flex">
            <div class="flex-auto items-center flex justify-center">
              <img src="@/assets/icons/Rectangle 3466563.png" class="mr-3" width="40" height="40" alt="Chat" />
              <p>{{ profile.username }}</p>
            </div>
            <div class="w-5 justify-end cursor-pointer" @click="toggleIconMenu" ref="menuIcon">
              <Icon icon="system-uicons:menu-vertical" width="24" height="24" />
              <div v-if="isIconmenuVisible"
                class="absolute mt-2 bg-white border rounded-xl shadow-lg w-48 bottom-14 left-1">
                <ul class="text-gray-700">
                  <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer" @click="logout">
                    <h6 class="font-bold">Logout</h6>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <button v-else @click="pushRouteLogin"
            class="bg-slate-600 text-white px-4 py-2 rounded hover:bg-green-600 w-full">
            Login
          </button>
        </div>
      </div>

      <!-- Toggle Sidebar Button -->
      <!-- <button @click="toggleSidebar"
        class="absolute top-3 left-4 bg-gray-800 text-white p-2  rounded hover:bg-gray-600 z-10 ">
        <Icon :icon="isSidebarOpen ? 'mdi:menu-open' : 'mdi:menu'" class="text-white" width="24" height="24" />
      </button> -->

      <!-- Main Content -->
      <div class="flex-auto bg-custombodyLight ">
        <RouterView />
      </div>
    </div>
  </div>
</template>


