<template>
  <div class="border border-gray-300 rounded-md bg-white p-4 shadow-sm w-[1000px]">

    <div class="flex items-center justify-between">
      <!-- ปุ่มเลือกไฟล์ ซ้ายสุด -->
      <button
        class="bg-customSildboxred text-white px-4 py-2 rounded-xl hover:bg-red-700 transition"
        @click="$refs.fileInput.click()"
      >
        เลือกไฟล์
      </button>

      <!-- ข้อความแสดงชื่อไฟล์ อยู่ตรงกลาง -->
      <p class="flex-1  text-sm text-gray-600 truncate mx-4">
        {{ selectedFile?.name || 'ยังไม่ได้เลือกไฟล์' }}
      </p>

      <!-- ปุ่มอัปโหลด ขวาสุด -->
      <button
        class="bg-[#2383E2] text-white px-4 py-2 rounded-xl transition hover:opacity-80 "
        @click="uploadFile"
        :disabled="!selectedFile"
      >
        อัปโหลด
      </button>
    </div>

    <!-- ซ่อน input file -->
    <input
      ref="fileInput"
      type="file"
      accept=".docx,.txt"
      @change="handleFileUpload"
      class="hidden"
    />
  </div>
</template>

<script>
export default {
    emits: ['file-uploaded'],
    data() {
        return {
        selectedFile: null,
        fileContent: ''
        };
    },
    methods: {
        handleFileUpload(event) {
          const file = event.target.files[0]
          if (!file) return

          const allowedTypes = [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
            'text/plain' // .txt
          ]
          const allowedExtensions = ['.docx', '.txt']

          const fileName = file.name.toLowerCase()
          const hasAllowedExtension = allowedExtensions.some(ext => fileName.endsWith(ext))
          const hasAllowedType = allowedTypes.includes(file.type)

          if (!hasAllowedExtension && !hasAllowedType) {
            alert('Only .docx and .txt files are allowed.')
            return
          }

          this.selectedFile = file
        },
        async uploadFile() {
        if (!this.selectedFile) {
            alert('Please select a file.');
            return;
        }
        const formData = new FormData();
        formData.append('file', this.selectedFile);

        try {
            const response = await fetch('http://localhost:5500/upload', {
            method: 'POST',
            body: formData
            });
            const data = await response.json();
            if (data.content) {
            this.fileContent = data.content;
            this.$emit('file-uploaded', this.fileContent); // emit here
            alert('File uploaded successfully');
            } else if (data.error) {
            } else {
            alert(data.error || 'Upload failed');
            }
        } catch (err) {
            alert('Upload failed');
        }
        }
    }
    };
</script>
