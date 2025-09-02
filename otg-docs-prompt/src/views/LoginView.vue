<template>
  <div class="flex flex-col items-center justify-center">
    <div class="absolute top-[152px] left-[507px] w-[444px] h-[433px] bg-white rounded-[40px] shadow-md flex flex-col justify-center p-6 text-center">
      <h2 class=" text-2xl font-bold text-customSildboxred flex items-center justify-center">
         <img src="@/assets/icons/Rectangle 3466563.png" class="mr-3" width="70" height="70" alt="Settings" />
          Natachat
          <span class="text-black font-bold ml-3 ">AI</span>
        </h2>
        <span class="block text-xs text-gray-300 mb-3 text-left">
          Please login to continue
        </span>
        <form @submit.prevent="handleLogin">
        <div class="mb-4 text-left ">
          <label for="username" class="block text-sm font-Promt text-gray-700">Username</label>
          <input
            v-model="username"
            type="text"
            id="username"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter your username"
            required
          />
        </div>
          <div class="mb-4 text-left">
            <label for="password" class="block text-sm font-Promt text-gray-700">Password</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showLineKey ? 'text' : 'password'"
                id="password"
                class="w-full mt-1 px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter your password"
                required
              />
              <button
                type="button"
                @click="showLineKey = !showLineKey"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
              >
                <span v-if="showLineKey">
                  <img src="@/assets/icons/eye (1).png" alt="Hide" width="19" height="19" />
                </span>
                <span v-else>
                  <img src="@/assets/icons/eye-crossed.png" alt="Show" width="19" height="19" />
                </span>
              </button>
            </div>
          </div>

        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <input
              v-model="remember"
              type="checkbox"
              id="remember"
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-900">Remember me</label>
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-customSildboxred text-white py-2 px-4 rounded-xl hover:bg-red-700 focus:outline-none font-bold"
        >
          Login
        </button>

        <!-- <div id="error" class="text-red-500 mt-4 hidden">
         เข้าสู่ระบบไม่สำเร็จ Username & Password ไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง
        </div> -->
      </form>
    </div>
  </div>
</template>



<script lang="ts" setup>
import router from "@/router";
import { useAuthenticationStore } from "@/stores/authentication";
import { onMounted, ref } from "vue";

const showLineKey = ref(false)
const username = ref("");
const password = ref("");
const remember = ref(false);
const authenticationStore = useAuthenticationStore()


onMounted(() => {
  const token = ref(localStorage.getItem("token"));
  if (token.value) {
    router.push({ path: "/" }).catch((err) => console.error(err));
  }
});
const handleLogin = async () => {
  localStorage.removeItem("token")
  await authenticationStore.login({
    username: username.value,
    password: password.value,
    remember: remember.value
  })

  const token = ref(localStorage.getItem("token"));
  console.log(token.value);
  if (token.value) {
    await authenticationStore.getProfile();
    location.reload();
    //

  } else {
    // If token does not exist, log an error or redirect to login
    console.error("Token is missing in localStorage.");
    router.push({ path: "/login" }).catch((err) => console.error(err));
  }
};
// function login() {
//   const username = document.getElementById('username').value;
//   const password = document.getElementById('password').value;
//   const errorDiv = document.getElementById('error');

//   // ตัวอย่างเช็ค username, password แบบง่าย
//   if (username === 'admin' && password === '1234') {
//     alert('เข้าสู่ระบบสำเร็จ');
//     errorDiv.classList.add('hidden'); // ซ่อนข้อความ error ถ้าล็อกอินถูก
//   } else {
//     errorDiv.classList.remove('hidden'); // แสดงข้อความ error ถ้าล็อกอินผิด
//   }
// }

</script>

<style scoped>
/* Add any custom styles here */


</style>
