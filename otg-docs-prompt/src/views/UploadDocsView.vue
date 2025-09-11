<template>
  <div class="h-full flex flex-col p-6 bg-gray-50">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-2xl font-bold text-gray-800">File Manager</h3>

      <!-- Upload Button -->
      <label class="cursor-pointer flex items-center gap-2 bg-[#E43A32] hover:bg-red-700 text-white px-5 py-2 rounded-full">
        <img src="@/assets/icons/ant-design_plus-circle-filled.svg" width="20" height="20" alt="Add" />
        Upload File
        <input type="file" class="hidden" @change="handleUpload" />
      </label>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full border border-gray-200 rounded-lg overflow-hidden">
        <thead>
          <tr class="bg-gray-100">
            <th class="text-left p-3 border border-gray-300 font-bold">Filename</th>
            <th class="text-left p-3 border border-gray-300 font-bold">Uploaded At</th>
            <th class="text-left p-3 border border-gray-300 font-bold">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in files" :key="file.id" class="hover:bg-gray-50">
            <td class="p-3 border border-gray-300 truncate w-48">{{ file.filename }}</td>
            <td class="p-3 border border-gray-300">{{ formatDate(file.uploaded_at) }}</td>
            <td class="p-3 border border-gray-300 text-center space-x-2">
              <button
                @click="handleDownload(file.id)"
                class="bg-[#EBEBEB] text-black px-3 py-1 rounded-xl hover:bg-blue-600"
              >
                <img src="@/assets/icons/Vector (1).png" alt="Download" class="w-4 h-4 inline-block -mt-1" />
                <span class="font-bold">Download</span>
              </button>

              <button
                @click="handleDelete(file.id)"
                class="bg-[#FFB5B559] text-[#FF0000] px-3 py-1 rounded-xl hover:bg-red-600"
              >
                <img src="@/assets/icons/trash (7).png" alt="Delete" class="w-4 h-4 inline-block -mt-1" />
                <span class="font-bold">Delete</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Loader -->
    <div v-if="isLoading" class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="loading">Loading...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import axios from "axios"
import { CONFIG } from '@/config'

const files = ref<any[]>([])
const isLoading = ref(false)

async function fetchFiles() {
  isLoading.value = true
  try {
    const { data } = await axios.get(`${CONFIG.API_BASE_URL}/upload/documents`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    })
    files.value = data
  } catch (err) {
    console.error("Error fetching files:", err)
  } finally {
    isLoading.value = false
  }
}

async function handleUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append("file", file)

  isLoading.value = true
  try {
    await axios.post(`${CONFIG.API_BASE_URL}/upload/documents`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })
    await fetchFiles()
  } catch (err) {
    console.error("Upload failed:", err)
  } finally {
    isLoading.value = false
  }
}

async function handleDelete(id: string) {
  if (!confirm("Are you sure you want to delete this file?")) return

  isLoading.value = true
  try {
    await axios.delete(`${CONFIG.API_BASE_URL}/upload/documents/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    })
    await fetchFiles()
  } catch (err) {
    console.error("Delete failed:", err)
  } finally {
    isLoading.value = false
  }
}

async function handleDownload(id: string) {
  try {
    const response = await axios.get(`${CONFIG.API_BASE_URL}/upload/documents/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      responseType: "blob"
    })

    let filename = "download"
    const disposition = response.headers["content-disposition"]

    if (disposition) {
      // Case 1: RFC 5987 (filename*=UTF-8'')
      const utf8FilenameRegex = /filename\*\=UTF-8''(.+)/
      const matchesUtf8 = utf8FilenameRegex.exec(disposition)
      if (matchesUtf8 && matchesUtf8[1]) {
        filename = decodeURIComponent(matchesUtf8[1])
      } else {
        // Case 2: Basic filename="..."
        const filenameRegex = /filename="?([^"]+)"?/
        const matches = filenameRegex.exec(disposition)
        if (matches && matches[1]) {
          filename = matches[1]
        }
      }
    }

    // Preserve MIME type
    const mimeType = response.headers["content-type"] || "application/octet-stream"
    const blob = new Blob([response.data], { type: mimeType })

    // Create blob link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.setAttribute("download", filename) // ✅ now real Thai filename works
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error("Download failed:", err)
  }
}

function formatDate(dateString: string | null) {
  if (!dateString) return "—"
  return new Date(dateString).toLocaleString()
}

onMounted(fetchFiles)
</script>

<style scoped>
.loading {
  text-align: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
