<template>
  <div class="h-full flex flex-col p-2">
    <!-- <div class="h-12 w-full -mt-2 flex items-center">
      <h3 class="font-Promt text-customSystempromt">Account</h3>
    </div> -->
    <div class="w-[1200px] mt-20 ml-5">
      <div class="overflow-x-auto">
        <div class="mb-4 flex items-center space-x-4">
          <h3 class="text-back text-ls font-bold text-2xl">Account</h3>
          <button
            class="flex items-center   text-customSildboxred px-4 py-2 rounded-full hover:bg-red-600 bg-[#E43A32]"

            @click="handleCreate"
          >
          <div
          class=" flex items-center justify-center rounded-full text-base font-bold leading-none"
          >
          </div>
          <img src="@/assets/icons/ant-design_plus-circle-filled.svg" width="20" height="20"  />
          <span class="font-Prompt" style="color: white;">Create</span>
          </button>
        </div>
        <table class="w-full font-Promt rounded-lg overflow-hidden border-separate border-spacing-0">
          <thead>
            <tr class="bg-gray-100">
              <th class="relative p-3  w-36 text-left pl-2 font-bold" style="background-color: #F0F2F3;">
                Username
                <span class="absolute top-1/4 bottom-1/4 right-0 w-[1px] bg-gray-300"></span>
                <span class="block border-gray-300 mt-1"></span> <!-- เส้นล่างเต็ม -->
              </th>

              <th class="relative p-3  w-36 text-left pl-2 font-bold" style="background-color: #F0F2F3;">
                Email
                <span class="absolute top-1/4 bottom-1/4 right-0 w-[1px] bg-gray-300"></span>
                <span class="block border-gray-300 mt-1"></span>
              </th>

              <th class="relative p-3  w-36 text-left pl-2 font-bold" style="background-color: #F0F2F3;">
                Role
                <span class="absolute top-1/4 bottom-1/4 right-0 w-[1px] bg-gray-300"></span>
                <span class="block border-gray-300 mt-1"></span>
              </th>

              <th class="relative p-3  w-36 text-left pl-2 font-bold" style="background-color: #F0F2F3;">
               Actions
                <span class="absolute top-2 bottom- right-0 w-[1px] bg-gray-300"></span>
                <span class="block border-gray-300 mt-1 right-0 "></span> <!-- ไม่มีเส้นขวา -->
              </th>

            </tr>
        </thead>
          <tbody>
            <tr
              class="hover:bg-gray-50"
              v-for="(acc, index) in Object.values(accounts)"
              :key="index"
            >
              <td class="p-3 border-b border-l border-gray-300">
                <p class="truncate w-36">{{ acc.username }}</p>
              </td>
              <td class="p-3 border-b border-gray-300">
                <p class="truncate whitespace-pre line-clamp-1">
                  {{ acc.email }}
                </p>
              </td>
              <td class="p-3 border-b border-gray-300">
                <p class="truncate whitespace-pre line-clamp-1">
                  {{ acc.role }}
                </p>
              </td>
              <td class="p-3 border-b border-r border-gray-300 text-center">
                <div class="flex justify-center items-center gap-2 flex-nowrap">
                  <button
                    @click="handleEdit(acc.id)"
                    class="w-24   text-black px-3 py-2 rounded-xl  flex items-center justify-center gap-2 hover:bg-blue-600"
                  >
                    <img src="/src/assets/icons/iconEdit.png" alt="Edit Icon" class="h-5 w-5" />
                    <span class=" font-bold">Edit</span>
                  </button>


                  <button
                    @click="showConfirm = true"
                    class="w-24  text-black px-3 py-2 rounded-xl flex items-center justify-center gap-2 hover:bg-red-600 bg-[#FFB5B559]"

                  >
                    <img src="/src/assets/icons/bin (1) 1.png" alt="Delete Icon" class="h-5 w-5" />
                    <span class="text-[#FF0000] font-bold">Delete</span>
                  </button>
                  <!-- กล่องยืนยันการลบ -->
                    <div v-if="showConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 ">
                      <div class="bg-white p-6 rounded-xl shadow-lg w-[300px] text-center space-y-10">
                       <h2 class="text-lg font-bold mb-2 text-left">Confirm Delete</h2>
                       <h2 class="text-lg font-bold mb-6 text-left">Do you want to delete ?</h2>
                        <div class="flex justify-center gap-4">
                          <button @click="confirmDelete" class="bg-red-500 text-white px-4 py-2 rounded-xl hover:bg-red-600">
                            <img src="@/assets/icons/trash (5).png" alt="Edit" class="w-5 h-5 align-middle inline-block -mt-1" />
                            Delete
                          </button>
                          <button @click="showConfirm = false" class="bg-gray-300 px-4 py-2 rounded-xl hover:bg-gray-400">
                            <img src="@/assets/icons/cross.png" alt="Edit" class="w-5 h-5 align-middle inline-block -mt-1" />
                            Cancle
                          </button>
                        </div>
                      </div>
                    </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div
      v-if="isLoading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="loading">Loading...</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { Icon } from '@iconify/vue'
import router from '@/router'

import { useAccountStore } from '@/stores/accounts'

const isLoading = ref(false)

const accountStore = useAccountStore()

const accounts = computed(() => accountStore.accounts)

onMounted(() => {
  accountStore.fetchAccounts()
})

function handleEdit(id: string) {
  router.push({ name: 'editing-acc', params: { id: id } }).catch((err) => console.error(err))
}

function handleCreate() {
  router.push({ name: 'create-acc' }).catch((err) => console.error(err))
}

// Function to create a new account


const showConfirm = ref(false)

function confirmDelete() {
  showConfirm.value = false
  alert('ลบข้อมูลเรียบร้อย') // ตรงนี้แทนที่ด้วยโค้ดลบจริงของคุณ
}
</script>

<style scoped>
.assistant {
  @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
  width: fit-content;
  max-width: 50%;
  word-wrap: break-word; /* Ensures long words are wrapped */
  overflow-wrap: break-word; /* Modern equivalent for wrapping text */
  white-space: normal;
}

.user {
  @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
  margin-left: auto; /* Align to the right */
  width: fit-content;
  max-width: 50%;
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
.loading {
  text-align: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
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


</style>
