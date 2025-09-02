<template>
     <button
        class="text-red-500 text-3xl px-10 py-3 rounded-lg font-Promt flex items-center gap-2"
        @click="handleCancel"
      >
      <img src="/src/assets/icons/arrow-small-left.png" alt="Save Icon" class="h-10 w-10" />
      </button>
    <div class="h-full flex flex-col p-4">
      <div class="h-12 w-full flex items-center front-Promt ml-10">
        <h3 class="text-back text-ls font-bold text-2xl">Create Account</h3>
      </div>
    <div class="w-[1100px] mt-1 p-10">
      <div class="overflow-x-auto w-full">
        <div class="mb-8 border-b pb-3">
        <div class="flex">
          <div class="w-80 flex items-center text-left">
            <h5 for="username" class="text-[16px] text-textColor font-Promt">Username</h5>

          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.username"
              type="text"
              id="username"
              class="w-full mt-1 px-3 py-2 border border-gray-300 bg-gray-200 text-textColor rounded-full shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter username"
            />
          </div>
        </div>
       </div>

        <div class="flex mt-4 border-b pb-3">
          <div class="w-80 flex text-left py-2 ">
            <h5 for="email" class="text-[16px] text-textColor font-Promt">Email</h5>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.email"
              type="text"
              id="email"
              class="w-full mt-1 px-3 py-2 border border-gray-300 bg-gray-200 text-textColor rounded-[px] shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter email"
            />
          </div>
        </div>

        <div class="flex mt-4 border-b pb-3">
          <div class="w-80 flex text-left py-2">
            <h5 for="role" class="text-[16px] text-textColor font-Promt">Role</h5>
          </div>
          <div class="flex-4 w-full">
            <select
              v-model="newAccount.role"
              id="role"
              class="w-full mt-1 px-3 py-2 border border-gray-300 bg-gray-200 focus:bg-white text-gray-400  rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="" disabled selected>Select role</option>
              <option value="admin">Admin</option>
              <option value="editor">Editor</option>
              <option value="viewer">User</option>
              <option value="viewer">Chatter</option>
            </select>
          </div>
        </div>

        <div class="flex mt-4 border-b pb-3">
          <div class="w-80 flex text-left py-2">
            <h5 for="password" class="text-[16px] text-textColor font-Promt">Password</h5>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.password"
              type="password"
              id="password"
             class="w-full mt-1 px-3 py-2 border border-gray-300 bg-gray-200 text-textColor shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-xl"

              placeholder="Enter Password"
            />
          </div>
        </div>

        <div class="flex mt-4 border-b pb-3">
          <div class="w-80 flex text-left py-2">
            <h5 for="confirmPassword" class="text-[16px] text-textColor font-Promt">Confirm Password</h5>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.confirmPassword"
              type="password"
              id="confirmPassword"
              class="w-full mt-1 px-3 py-2 border border-gray-300 bg-gray-200 text-textColor rounded-full shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Confirm Password"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Submit & Cancel buttons -->
    <div class="mt-4 ml-8 flex gap-4">
      <button
        class="bg-customSildboxred text-white text-lg px-6 py-3 rounded-2xl font-Promt flex items-center gap-2 hover:bg-red-600"
        @click="handleCreate"
      >
        <img src="/src/assets/icons/disk (2).png" alt="Save Icon" class="h-5 w-5" />
        Save
      </button>

      <!-- <button
        class="border-4 border-red-500 bg-Cancel text-red-500 text-lg px-10 py-3 rounded-lg font-Promt flex items-center gap-2  hover:bg-gray-400"
        @click="handleCancel"
      >
        Cancel
      </button> -->
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="isLoading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="loading">Loading...</div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import router from '@/router'
import { useAccountStore } from '@/stores/accounts'
import { ref } from 'vue'

const documentStore = useAccountStore()
const isLoading = ref(false)

const newAccount = ref({
  username: '',
  email: '',
  role: '',
  password: '',
  confirmPassword: ''
 })


function handleCancel() {
  router.push('/settings/account') // หรือใช้ window.history.back() ก็ได้
}


async function handleCreate() {
  isLoading.value = true
  try {
    await documentStore.createAccount(newAccount.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  newAccount.value = {
    username: '',
    email: '',
    role: '',
    password: '',
    confirmPassword: ''
   }
  router.push('/settings/account')
}
</script>
