<template>
  <div class="h-full flex flex-col p-4">
    <div class=" h-12 w-full flex items-center">
      <h3 class=" text-back text-ls font-bold text-2xl mt-36  ">Product</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto">
        <div class="float-end mb-6">
                <button
                  class="flex items-center gap-2 text-white px-4 py-2 rounded-full relative left-[-950px] top-[10px] hover:bg-red-700 bg-[#E43A32]"

                  @click="handleCreate"
                >
              <img src="@/assets/icons/ant-design_plus-circle-filled.svg" width="20" height="20" alt="Add" />
              Create
          </button>
        </div>
        <table class="w-full border border-gray-200 rounded-lg overflow-hidden ">
          <thead>
            <tr class="bg-gray-100">
              <th class="text-left p-3 border border-gray-300 font-bold">Name</th>
              <th class="text-left p-3 border border-gray-300 font-bold">Category</th>
              <th class="text-left p-3 border border-gray-300 font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="hover:bg-gray-50 "
              v-for="(doc, index) in Object.values(products)"
              :key="index"
            >
              <td class="p-3 border border-gray-300">
                <p class="truncate w-36">{{ doc.name }}</p>
              </td>
              <td class="p-3 border border-gray-300">
                <p class="truncate whitespace-pre line-clamp-1">
                  {{ doc.category }}
                </p>
              </td>
              <td class="p-1 border border-gray-300 text-center space-x-4">
                <button
                  @click="handleEdit(doc.id)"
                  class="  bg-[#EBEBEB] text-black px-4 py-2 rounded-xl hover:bg-blue-600 "
                >
                 <img src="@/assets/icons/Vector (1).png" alt="Edit" class="w-5 h-5 align-middle inline-block -mt-1" />
                  <span class="font-bold">Edit</span>
                </button>

                <button
                  @click="handleDelete(doc.id)"
                  class="bg-[#FFB5B559] text-[#FF0000] px-4 py-2 rounded-xl hover:bg-red-600 "
                 >
                  <img src="@/assets/icons/trash (7).png" alt="Edit" class="w-5 h-5 align-middle inline-block -mt-1" />
                 <span class="font-bold"> Delete</span>
                </button>
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

import { useProductStore } from '@/stores/products'

const isLoading = ref(false)

const documentStore = useProductStore()

const products = computed(() => documentStore.products)

onMounted(() => {
  documentStore.fetchProducts()
})

function handleEdit(id: string) {
  router.push({ name: 'editing-product', params: { id: id } }).catch((err) => console.error(err))
}

function handleCreate() {
  router.push({ name: 'create-product' }).catch((err) => console.error(err))
}

// Function to create a new document
async function handleDelete(id: string) {
  isLoading.value = true
  try {
    await documentStore.deleteProduct(id)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
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
