<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-customDark text-white -mt-2 h-12 w-full flex items-center">
      <h3>Edit Documents</h3>
    </div>
    <div class="w-full max-w-[1200px] bg-customSildbox p-7 rounded-3xl shadow-md ml-10">
      <div class="overflow-x-auto w-full">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="title" class="text-white">Title</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newDoc.title"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-4">
            <h4 for="title" class="text-white">Content</h4>
          </div>
          <div class="flex-4 w-full">
            <textarea
              v-model="newDoc.content"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 h-[500px]"
              placeholder="Enter content"
            ></textarea>
          </div>
        </div>
        <div class="float-end mt-4 flex space-x-2">
          <button
            class="bg-gray-500 p-4 rounded-md text-white hover:bg-gray-600"
            @click="emit('close')"
          >
            Cancel
          </button>
          <button
            class="bg-red-600 p-4 rounded-md text-white hover:bg-red-700"
            @click="handleSave"
          >
            Save
          </button>
        </div>
        <div class="float-end mt-4">
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

// const goBackToDocuments = () => {
//   router.push('/docs') // หรือเส้นทางตามที่ตั้งไว้
// }

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
