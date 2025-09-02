<template>
  <div class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-xl shadow-xl w-[90%] max-w-[1000px] h-[60vh] relative flex flex-col">
      <!-- ปุ่มปิด -->
      <button
        class="absolute top-3 right-8 text-2xl text-gray-700 hover:text-red-500"
        @click="goBackToDocuments"
        aria-label="Close"
      >
        ×
      </button>

      <!-- หัวข้อ -->
      <h3 class="text-xl font-bold text-gray-800 mb-4">Edit</h3>

      <!-- Input Title -->
      <div class="mb-3 flex items-center space-x-4">
        <label class="text-gray-700 font-medium whitespace-nowrap mr-11">หัวข้อ:</label>
        <input
          v-model="newDoc.title"
          type="text"
          placeholder="กรอกหัวข้อ"
          class="flex-1 px-4 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <!-- Upload Button แยกบรรทัด -->
      <div class="mb-3 flex items-center space-x-4">
        <label class="text-gray-700 font-medium whitespace-nowrap mr-10">เนื้อหา:</label>
        <textarea
          v-model="newDoc.content"
          id="content"
          rows="5"
          placeholder="กรอกเนื้อหา"
          class="w-full px-4 py-2 border border-gray-300 rounded-md"
        ></textarea>
      </div>


      <!-- Textarea Content
      <div class="mb-4">
        <label class="block mb-2 text-gray-700 font-medium">เนื้อหา:</label>
        <textarea
          v-model="newDoc.content"
          id="content"
          rows="10"
          placeholder="กรอกเนื้อหา"
          class="w-full px-4 py-2 border border-gray-300 rounded-md"
        ></textarea>
      </div> -->

      <!-- ปุ่มบันทึก ด้านล่างขวา -->
      <div class="flex-grow"></div>
      <div class="w-full max-w-7xl flex justify-end pr-10">
        <button
          class="bg-[#E43A32] px-6 py-3 rounded-2xl text-white text-lg font-medium hover:bg-red-700 disabled:opacity-50 flex items-center gap-2"
          :disabled="isLoading"
          @click="handleSave"
        >
          <img src="@/assets/icons/iconSave.png" alt="Save Icon" class="w-6 h-6" />
          {{ isLoading ? 'Saving...' : 'Save' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useDocumentStore } from '@/stores/documents'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import router from '@/router'
// import UploadButton from '@/components/upload_button.vue'
import Upload_Button from '@/components/Upload_Button.vue'

const route = useRoute()
const id = route.params.id
const emit = defineEmits(['close'])
const documentStore = useDocumentStore()
const documents = computed(() => documentStore.documents)
const document = computed(() => documents.value[id as string])
const isLoading = ref(false)
//const newDoc = ref({ title: '', content: '' })

//Form data
const newDoc = ref({
  id: document.value.id,
  title: document.value.title,
  content: document.value.content,
  doc_id: document.value.doc_id,
})

const goBackToDocuments = () => {
  router.push('/docs') // หรือเส้นทางตามที่ตั้งไว้
}


// function handleCancel() {
//   isCreating.value = false
//   newDoc.value = { title: '', content: '' }
// }



// // Function to create a new document
// async function handleSave() {
//   console.log('[handleSave] Called');
//   console.log('[handleSave] newDoc.value:', newDoc.value);

//   isLoading.value = true;
//   console.log('[handleSave] isLoading set to', isLoading.value);

//   try {
//     console.log('[handleSave] Attempting to save document...');
//     await documentStore.saveDocument(newDoc.value);
//     console.log('[handleSave] Document saved successfully');
//   } catch (error) {
//     console.error('[handleSave] Error saving document:', error);
//   } finally {
//     isLoading.value = false;
//     console.log('[handleSave] isLoading set to', isLoading.value);
//   }

//   console.log('[handleSave] Navigating to /docs');
//   router.push('/docs');
// }


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

</script>
