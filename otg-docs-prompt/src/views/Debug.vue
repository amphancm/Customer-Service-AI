<!-- <template>
    <div class="bg-gray-800 h-full flex flex-col p-4">
        <div class="text-white h-12 w-full flex items-center">
            <h3>Debug หน้านี้สำหรับทดสอบ</h3>
        </div>
        Toggle Switch for API Key
        <div class="flex items-center gap-2 my-2">
            <label class="text-white w-40" for="toggle-api-key">Show API Key:</label>
            <input id="toggle-api-key" type="checkbox" v-model="showApiKey" class="toggle-checkbox" />
        </div>
        Conditionally rendered API Key input
        <div v-if="showApiKey" class="flex items-center gap-2 mb-2">
            <label for="api-key" class="text-white w-40">API Key:</label>
            <input id="api-key" v-model="apiKey" type="text" class="rounded px-2 py-1 border border-gray-300 flex-1"
                placeholder="Enter API Key" />
            <button class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600" @click="saveApiKey">
                Save
            </button>
        </div>

        Line Secret Key, Secret Channel, and Line Token Inputs
        <div class="my-4 flex flex-col gap-2 max-w-md">
            <div class="flex items-center gap-2">
                <label for="line-secret-key" class="text-white w-40">Line Secret Key:</label>
                <input
                    id="line-secret-key"
                    v-model="lineSecretKey"
                    :type="showLineSecret ? 'text' : 'password'"
                    class="rounded px-2 py-1 border border-gray-300 flex-1"
                    placeholder="Enter Line Secret Key"
                />
                <button type="button" @click="showLineSecret = !showLineSecret" class="text-gray-500">
                    <span v-if="showLineSecret">🙈</span>
                    <span v-else>👁️</span>
                </button>
            </div>
            <div class="flex items-center gap-2">
                <label for="secret-channel" class="text-white w-40">Secret Channel:</label>
                <input
                    id="secret-channel"
                    v-model="secretChannel"
                    :type="showSecretChannel ? 'text' : 'password'"
                    class="rounded px-2 py-1 border border-gray-300 flex-1"
                    placeholder="Enter Secret Channel"
                />
                <button type="button" @click="showSecretChannel = !showSecretChannel" class="text-gray-500">
                    <span v-if="showSecretChannel">🙈</span>
                    <span v-else>👁️</span>
                </button>
            </div>
            Line Token Text Box remains unchanged
            <div class="flex items-center gap-2">
                <label for="line-textcallback" class="text-white w-40">Line Text box:</label>
                <input id="line-textcallback" v-model="line_text_callback" type="text"
                    class="rounded px-2 py-1 border border-gray-300 flex-1"
                    placeholder="Enter Line text for callback" />
            </div>
        </div>
        <button class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600" @click="testLineCallback">
            Test Callback
        </button>
    </div>
</template> -->

<script lang="ts" setup>
    import { computed, onMounted, ref } from 'vue'
    import { Icon } from '@iconify/vue'
    import router from '@/router'
    import { linecallback } from '@/stores/debug'
    // import { useProductStore } from '@/stores/products'

    const isLoading = ref(false)

    // Toggle for API Key input
    const showApiKey = ref(false)
    const apiKey = ref('')

    // Add refs for the new inputs
    const lineSecretKey = ref('')
    const secretChannel = ref('')
    const line_text_callback = ref('') // <-- Added for Line Token

    const showLineSecret = ref(false)
    const showSecretChannel = ref(false)

    function saveApiKey() {
        // You can replace this with your actual save logic
        alert('API Key saved: ' + apiKey.value )
    }

    const authenticationStore =linecallback()

    // function testLineCallback() {
    const testLineCallback = async () => {
        await authenticationStore.linecallback()
        //alert(' and secret key : ' + lineSecretKey.value + ' and secret channel : ' + secretChannel.value + 'Testing Line callback : ' + line_text_callback.value)
        // localStorage.removeItem("token")
        // await authenticationStore.login({
        //     username: username.value,
        //     password: password.value,
        //     remember: remember.value
        // })

        // const token = ref(localStorage.getItem("token"));
        // console.log(token.value);
        // if (token.value) {
        //     await authenticationStore.getProfile();
        //     location.reload();
        //     //

        // } else {
        //     // If token does not exist, log an error or redirect to login
        //     console.error("Token is missing in localStorage.");
        //     router.push({ path: "/login" }).catch((err) => console.error(err));
        // }
    };

    // You can replace this with your actual callback test logic
    //alert(' and secret key : ' + lineSecretKey.value + ' and secret channel : ' + secretChannel.value + 'Testing Line callback : ' + line_text_callback.value)
// }
</script>

<style scoped>
.assistant {
    @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
    width: fit-content;
    max-width: 50%;
    word-wrap: break-word;
    /* Ensures long words are wrapped */
    overflow-wrap: break-word;
    /* Modern equivalent for wrapping text */
    white-space: normal;
}

.user {
    @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
    margin-left: auto;
    /* Align to the right */
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
