import router from '@/router'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { CONFIG } from '@/config'

export const  linecallback = defineStore('linecallback', {
  actions: {
    async linecallback() {
      try {
        const token = ref(localStorage.getItem("token"));
        const response = await fetch(`${CONFIG.API_BASE_URL}/nani`, {headers:{
          'Authorization' : 'Bearer '+token.value
        }})
        // const res = await handleResponse(response);
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }

        const getdata = await response.json();
        console.log("getdata", getdata);
        return getdata
      } catch (error) {
        console.error('Failed to fetch systemPrompts:', error)
      }
    },
  },
})
