<!-- <template>
  <div class="h-full flex flex-col p-4">
    <div class="-h-screen w-full flex items-center text-white text-ls">
      <h3>Documents</h3>
    </div>

    <div class="flex overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="mb-6 flex justify-end">
          <button
            class="bg-cuttomCreate text-textColor px-4 py-2 rounded-full hover:bg-green-600"
            @click="handleCreate"
          >
            Create
          </button>
        </div>
        <table class="w-full border bg-customTr border-gray-200 rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-gray-100">
              <th class="text-left bg-customTr text-textColor p-3 border border-gray-300 w-36">Title</th>
              <th class="text-left bg-customTr text-textColor p-3 border border-gray-300 w-36">Content</th>
              <th class="text-left bg-customTr text-textColor p-3 border border-gray-300 w-36">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="bg-customTr1 hover:bg-white transition-colors duration-300 p-4"
              v-for="doc in Object.values(documents)"
              :key="doc.id"
            >
              <td class="p-3 border border-gray-300">
                <p class="truncate w-36">{{ doc.title }}</p>
              </td>
              <td class="p-3 border border-gray-300">
                <p class="truncate whitespace-pre line-clamp-1 w-[500px]">
                  {{ doc.content }}
                </p>
              </td>
              <td class="p-3 border border-gray-300 text-center space-x-2">
                <button
                  @click="handleEdit(doc.id)"
                  class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Edit
                </button>
                <button
                  @click="handleDelete(doc.id)"
                  class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


    <div
      v-if="isCreating"
      class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-createdocument p-6 rounded-xl shadow-xl w-[90%] max-w-[1000px] h-[80vh] relative">

        <button
          class="absolute top-3 right-8 text-white hover:text-red-500"
          @click="isCreating = false"
        >
          x
        </button>


        <h3 class="text-xl font-jeju text-textColor mb-4">Create Document</h3>
        <input
          v-model="newDoc.title"
          type="text"
          placeholder="Enter title"
          class="w-full mb-3 px-4 placeholder-textCreate bg-customSystempromt py-2 border border-gray-300 rounded-md"
        />
        <textarea
          v-model="newDoc.content"
          rows="4"
          placeholder="Enter content"
          class="w-full mb-4 px-4 py-2 placeholder-textCreate bg-customSystempromt border border-gray-300 rounded-md"
        ></textarea>
        <div class="flex justify-end space-x-2">
          <button
            @click="submitDocument"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Save
          </button>
          <button
            @click="isCreating = false"
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
        <div class="mt-4 flex justify-end">
          <Upload_Button @file-uploaded="onFileUploaded" />
        </div>
      </div>
    </div>
    <div
      v-if="isLoading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="loading">Loading...</div>
    </div>
  </div>
</template> -->

<template>
  <div class="h-full flex flex-col p-4">
    <!-- Header -->
    <div class="mt-20 flex items-center justify-start space-x-4 mb-4">
      <h3 class="text-back text-ls font-bold text-2xl">Documents</h3>
      <button
        class="flex items-center gap-2 text-white px-4 py-2 rounded-full hover:bg-red-700 bg-[#E43A32]"

        @click="handleCreate"
      >
        <img src="@/assets/icons/ant-design_plus-circle-filled.svg" width="20" height="20" alt="Chat" />
        <span class="font-Prompt">Create</span>
      </button>
    </div>

    <!-- Documents Table -->
   <table class="w-full border border-gray-500 rounded-xl border-collapse overflow-hidden">
      <thead>
        <tr class="bg-customTr">
          <th class="text-left text-textColor p-3 border border-gray-300 w-12 font-bold">ลำดับ</th>
          <th class="text-left text-textColor p-3 border border-gray-300 w-36 font-bold">หัวข้อ</th>
          <th class="text-left text-textColor p-3 border border-gray-300 w-36 font-bold">เนื้อหา</th>
          <th class="text-left text-textColor p-3 border border-gray-300 w-36"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(doc, index) in Object.values(documents)" :key="doc.id" class="border border-gray-300">
          <td class="p-3 border border-gray-300 text-center">{{ index + 1 }}</td>
          <td class="p-3 border border-gray-300">
            <p class="truncate w-36">{{ doc.title }}</p>
          </td>
          <td class="p-3 border border-gray-300">
            <p class="truncate whitespace-pre line-clamp-1 w-[500px]">{{ doc.content }}</p>
          </td>
          <td class="p-3 border border-gray-300 text-center ">
            <div class="flex justify-center  items-center gap-3 flex-nowrap">
              <button @click="handleEdit(doc.id)" class="w-24 bg-gray-100 text-black px-3 py-2 rounded-xl hover:bg-blue-600 flex items-center justify-center gap-2">
                <img src="/src/assets/icons/iconEdit.png" alt="Edit Icon" class="h-5 w-5" />
                <span class="font-bold">Edit</span>

              </button>
              <button @click="openConfirm(doc.id)"
               class="w-24 px-3 py-2 rounded-xl  flex items-center justify-center gap-2 hover:bg-red-600 bg-[#FFB5B559]"
              >
                <img src="/src/assets/icons/bin (1) 1.png" alt="Delete Icon" class="h-5 w-5" />
                <span class="font-bold text-[#FF0000]">Delete</span>

              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Create Document Modal -->
  <div v-if="isCreating" class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-createdocument p-6 rounded-xl shadow-xl w-[90%] max-w-[1000px] h-[80vh] relative flex flex-col">
      <button class="absolute top-3 right-8 text-back text-2xl hover:text-red-500" @click="isCreating = false" aria-label="Close">×</button>
      <h3 class="text-2xl font-Prompt font-bold text-textColor mb-4">Create</h3>

      <div class="mb-4 flex items-center space-x-4">
        <label class="text-textColor font-Promot whitespace-nowrap mr-5">หัวข้อ:</label>
        <input v-model="newDoc.title" type="text" placeholder="กรุณาระบุ" class=" px-4 py-2 bg-createdocument border border-gray-300 rounded-xl" />
      </div>

      <div class="mb-4 flex items-center space-x-4">
        <label class="text-textColor font-Promot whitespace-nowrap">อัปโหลด:</label>
        <Upload_Button @file-uploaded="onFileUploaded" class="bg-green-600 text-white px-4 py-2 rounded-xl transition " />
      </div>


      <label class="text-gray-700 font-medium whitespace-nowrap mr-10">เนื้อหา:</label>
      <textarea v-model="newDoc.content" rows="6" placeholder="" class="px-4 py-2 bg-[#F0F0F0] border border-gray-300 rounded-xl -mt-2 w-[880px] ml-auto "></textarea>
      <div class="flex-grow"></div>
      <div class="w-full max-w-7xl flex ml-10 pr-10 justify-end">

        <button @click="submitDocument" class="bg-customSildboxred hover:bg-red-700 text-white text-lg px-6 py-3 rounded-2xl font-Promt flex items-center gap-2">
          <img src="@/assets/icons/disk (2).png" alt="My Icon" class="w-6 h-6" />
          Save
        </button>
      </div>
    </div>
  </div>

  <!-- Edit Modal
  <EditDocumentModal v-if="isEditing" :doc="editDoc" @close="isEditing = false" @save="handleUpdateDocument" /> -->

  <!-- Loading -->
  <div v-if="isLoading" class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="loading text-white text-lg font-bold">Loading...</div>
  </div>

  <!-- ✅ Popup ยืนยันการลบ อยู่กลางจอ -->
  <div v-if="showConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-3xl shadow-xl w-[660px] h-[230] text-center space-y-10">
      <h2 class="text-lg font-bold mb-2 text-left">Confirm Delete</h2>
      <h2 class="text-lg font-bold mb-6 text-left">Do you want to delete ?</h2>
      <div class="flex justify-center gap-4">
        <button @click="confirmDelete" class="bg-customSildboxred hover:bg-red-700 text-white text-lg px-6 py-3 rounded-2xl font-Promt flex items-center gap-2">
        <img src="@/assets/icons/ant-design_save-filled.png" alt="My Icon" class="w-6 h-6" />
        Delete
      </button>
        <button @click="showConfirm = false" class="text-black text-lg px-6 py-3 rounded-2xl font-Promt flex items-center gap-2 bg-[#F0F1F1] hover:bg-gray-500">

          <img src="@/assets/icons/ant-design_close-outlined.svg" alt="My Icon" class="w-6 h-6" />
          Cancle
        </button>
      </div>
    </div>
  </div>
</template>




<!-- <script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { Icon } from '@iconify/vue'
import router from '@/router'

import { useDocumentStore } from '@/stores/documents'
import EditDocumentModal from '@/components/EditDocumentModal.vue'
import Upload_Button from '@/components/Upload_Button.vue'



const isLoading = ref(false)

const documentStore = useDocumentStore()

const documents = computed(() => documentStore.documents)

const isCreating = ref(false)
const newDoc = ref({ title: '', content: '' })

const isEditing = ref(false)

const editDoc = ref<{ id: string; title: string; content: string }>({ id: '', title: '', content: '' })



onMounted(() => {
  documentStore.fetchDocuments()
})



function onFileUploaded(content: string) {
  newDoc.value.content = content
}

// Function to save the document
async function handleSave() {
  isLoading.value = true
  try {
    await documentStore.saveDocument(newDoc.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  // Clear form after creation
  router.push('/docs')
}

function handleEdit(id: string) {
  router.push({ name: 'editing-docs', params: { id: id } }).catch((err) => console.error(err))
}

function handleCreate() {
  isCreating.value = true
}
// function handleCancel() {
//   isCreating.value = false
//   newDoc.value = { title: '', content: '' }
// }

function submitupload() {
  isCreating.value = false
  newDoc.value = { title: '', content: '' }
  router.push('/docs/upload')
}
// function handleCreate() {
//   router.push({ name: 'create-doc' }).catch((err) => console.error(err))
// }

async function submitDocument() {
  if (!newDoc.value.title.trim() || !newDoc.value.content.trim()) {
    alert('กรุณากรอก Title และ Content ให้ครบถ้วนก่อนบันทึก')
    return
  }

  isLoading.value = true
  try {
    await documentStore.createDocument(newDoc.value)
    newDoc.value = { title: '', content: '' }
    isCreating.value = false
    await documentStore.fetchDocuments()
  } catch (error) {
    console.error('Error creating document:', error)
  } finally {
    isLoading.value = false
  }
}


// Function to create a new document
async function handleDelete(id: string) {
  if (!id) {
    console.warn('Invalid id for deletion:', id)
    return
  }
  isLoading.value = true
  try {
    await documentStore.deleteDocument(id)
    await documentStore.fetchDocuments() // โหลดข้อมูลหลังลบด้วย
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
</style> -->


<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import router from '@/router'
import { useDocumentStore } from '@/stores/documents'
import Upload_Button from '@/components/Upload_Button.vue'
import EditDocumentModal from '@/components/EditDocumentModal.vue'

// Store
const documentStore = useDocumentStore()
const documents = computed(() => documentStore.documents)

// State
const isCreating = ref(false)
const isEditing = ref(false)
const isLoading = ref(false)
const showConfirm = ref(false) // Popup ยืนยันการลบ
const targetId = ref<string | null>(null) // เก็บ id ที่จะลบ

const newDoc = ref({ title: '', content: '' })
const editDoc = ref({ id: '', title: '', content: '' })

onMounted(() => {
  documentStore.fetchDocuments()
})

function handleCreate() {
  isCreating.value = true
}

function onFileUploaded(content: string) {
  newDoc.value.content = content
}

async function submitDocument() {
  if (!newDoc.value.title.trim() || !newDoc.value.content.trim()) {
    alert('กรุณากรอก Title และ Content ให้ครบถ้วนก่อนบันทึก')
    return
  }

  isLoading.value = true
  try {
    await documentStore.createDocument(newDoc.value)
    newDoc.value = { title: '', content: '' }
    isCreating.value = false
    await documentStore.fetchDocuments()
  } catch (error) {
    console.error('Error creating document:', error)
  } finally {
    isLoading.value = false
  }
}

function handleEdit(id: string) {
  router.push({ name: 'editing-docs', params: { id: id } }).catch((err) => console.error(err))
}

// เปิด Popup ยืนยันการลบ
function openConfirm(id: string) {
  targetId.value = id
  showConfirm.value = true
}

// ลบจริงเมื่อกดยืนยัน
async function confirmDelete() {
  if (!targetId.value) return
  showConfirm.value = false
  isLoading.value = true
  try {
    await documentStore.deleteDocument(targetId.value)
    await documentStore.fetchDocuments()
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการลบเอกสาร:', error)
  } finally {
    isLoading.value = false
  }
}

</script>


<style scoped>
.loading {
  text-align: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}
</style>

