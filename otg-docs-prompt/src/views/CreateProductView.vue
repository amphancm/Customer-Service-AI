<template>
  <div>
     <!-- ปุ่มเปิด Popup -->
      <!-- <button @click="showModal = true" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Create Product
      </button> -->


    <!-- Popup Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white w-full max-w-2xl rounded-3xl shadow-lg overflow-hidden relative">

        <!-- Header -->
          <div class="h-12 w-full flex items-center justify-between px-4 text-black">
            <h3 class="text-back text-ls font-bold text-2xl">Create Product</h3>
            <button @click="showModal = false" class="text-black text-2xl">
            <img src="/src/assets/icons/cross (1).png"  class="h-5 w-5" />
            </button>
          </div>


        <!-- เนื้อหา Form -->
        <div class="flex flex-col p-4 max-h-[80vh] overflow-y-auto">

          <!-- Name -->
          <div class="flex mb-4">
            <div class="w-40 flex items-center text-left">
              <h4 class="text-black font-bold ">Name</h4>
            </div>
            <div class="flex-4 w-full">
              <input
                v-model="newProduct.name"
                type="text"
                class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="ป้อนชื่อ"
              />
            </div>
          </div>

          <!-- Category -->
          <div class="flex mb-4">
            <div class="w-40 flex items-center text-left">
              <h4 class="text-black font-bold">Category</h4>
            </div>
            <div class="flex-4 w-full">
              <select
                v-model="newProduct.category"
                class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="" disabled>เลือกหมวดหมู่</option>
                <option value="food">Food</option>
                <option value="service">Service</option>
                <option value="travel">Travel</option>
              </select>
            </div>
          </div>

          <!-- Detail -->
          <div class="flex mb-4">
            <div class="w-40 flex text-left py-2">
              <h4 class="text-black font-bold">Detail</h4>
            </div>
            <div class="flex-4 w-full">
              <textarea
                v-model="newProduct.detail"
                rows="4"
                class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 h-[150px] bg-[#F0F0F0]"
                placeholder="ป้อนรายละเอียด"
              ></textarea>
            </div>
          </div>

          <!-- Pictures -->
          <div class="flex mb-4">
            <div class="w-40 flex text-left py-2">
              <h4 class="text-black font-bold">Pictures</h4>
            </div>
            <div class="flex-4 w-full">
              <div class="flex items-center gap-4">
                  <label
                    class="text-white px-4 py-2 rounded-xl cursor-pointer hover:opacity-90"
                    style="background-color: #E43A32;"
                  >
                  เลือกไฟล์
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    class="hidden"
                    @change="handleFileUpload"
                  />
                </label>
              </div>

              <div v-if="newProduct.pictures.length" class="flex flex-wrap gap-4 my-4">
                <div
                  v-for="(preview, index) in newProduct.pictures"
                  :key="index"
                  class="relative"
                  style="width: 100px; height: 100px;"
                >
                  <img
                    :src="preview"
                    alt="Preview"
                    class="w-full h-full object-cover rounded-md shadow"
                  />
                  <button
                    @click="removePreview(index)"
                    class="absolute top-1 right-1 bg-red-600 text-white p-1 rounded"
                  >
                    &times;
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- ปุ่ม Submit -->
          <div class="flex justify-end mt-4">
            <button
              class="bg-[#E43A32] px-4 py-2 rounded-xl text-white flex items-center gap-2 "
              @click="submitAndClose"
              :disabled="isLoading"
            >
             <img src="@/assets/icons/disk (2).png" alt="Save Icon" class="w-6 h-6" />
              Save
            </button>

          </div>
        </div>

        <!-- Loading Overlay -->
        <div
          v-if="isLoading"
          class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
        >
          <div class="loading text-white">Loading...</div>
        </div>

      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import router from '@/router'
import { useProductStore } from '@/stores/products'
import { Icon } from '@iconify/vue/dist/iconify.js'
import { ref } from 'vue'

const productStore = useProductStore()
const isLoading = ref(false)
const newProduct = ref<{
  name: string;
  category: string;
  detail: string;
  pictures: string[];
}>({
  name: '',
  category: '',
  detail: '',
  pictures: [],
})

// const pictures = ref<string[]>([])

// Handle file input change
const handleFileUpload = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (!files) return

  Array.from(files).forEach((file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      newProduct.value.pictures.push(e.target?.result as string)
    }
    reader.readAsDataURL(file)
  })
  // Reset the input so the same file can be reselected
  ;(event.target as HTMLInputElement).value = ''
}

// Remove preview
const removePreview = (index: number) => {
  newProduct.value.pictures.splice(index, 1)
}

// ฟังก์ชันสร้างสินค้า จริง ๆ ใช้ใน submit ของ popup
async function handleCreate() {
  isLoading.value = true
  try {
    await productStore.createProduct(newProduct.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  newProduct.value = {
    name: '',
    category: '',
    detail: '',
    pictures: []
  }
  router.push('/products')
}

import { ref, onMounted } from 'vue'

const showModal = ref(false)

onMounted(() => {
  showModal.value = true
})
const submitAndClose = async () => {
  await handleCreate()
  showModal.value = false
}


</script>

<style scoped>
img {
  border: 1px solid #ddd;
}
</style>
