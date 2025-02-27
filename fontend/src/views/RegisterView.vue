<template>
    <div class="wrapper">
        <div class="login-container">
            <div class="login-card">
                <img class="logo" :src="logoURL" alt="Sonify Logo" />
                <div class="login-header">
                    <h2 class="login-title">Create an Account</h2>
                    <p>Join us by filling out the form below.</p>
                </div>
                <form @submit.prevent="register" class="login-form">
                    <div class="login-input-group">
                        <input
                            v-model="email"
                            placeholder="Email Address"
                            required
                            class="login-input"
                        />
                    </div>
                    <div class="login-input-group">
                        <input
                            v-model="name"
                            placeholder="Username"
                            required
                            class="login-input"
                        />
                    </div>
                    <div class="login-input-group">
                        <input
                            v-model="password"
                            type="password"
                            placeholder="Password"
                            required
                            class="login-input"
                        />
                    </div>
                    <button type="submit" class="login-button">Register</button>
                </form>
                <p
                    class="login-message"
                    :class="{ error: message.includes('Invalid', 'Already') }"
                >
                    {{ message }}
                </p>
                <div class="login-line-with-text">
                    <span></span>
                    <p class="text">Or signin with</p>
                    <span></span>
                </div>
                <div class="login-platforms">
                    <div class="login-platform">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            x="0px"
                            y="0px"
                            width="100"
                            height="100"
                            viewBox="0 0 48 48"
                        >
                            <path
                                fill="#FFC107"
                                d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"
                            ></path>
                            <path
                                fill="#FF3D00"
                                d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"
                            ></path>
                            <path
                                fill="#4CAF50"
                                d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"
                            ></path>
                            <path
                                fill="#1976D2"
                                d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"
                            ></path>
                        </svg>
                        <p>Google</p>
                    </div>
                    <div class="login-platform">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            x="0px"
                            y="0px"
                            width="100"
                            height="100"
                            viewBox="0 0 50 50"
                            fill="white"
                        >
                            <path
                                d="M 44.527344 34.75 C 43.449219 37.144531 42.929688 38.214844 41.542969 40.328125 C 39.601563 43.28125 36.863281 46.96875 33.480469 46.992188 C 30.46875 47.019531 29.691406 45.027344 25.601563 45.0625 C 21.515625 45.082031 20.664063 47.03125 17.648438 47 C 14.261719 46.96875 11.671875 43.648438 9.730469 40.699219 C 4.300781 32.429688 3.726563 22.734375 7.082031 17.578125 C 9.457031 13.921875 13.210938 11.773438 16.738281 11.773438 C 20.332031 11.773438 22.589844 13.746094 25.558594 13.746094 C 28.441406 13.746094 30.195313 11.769531 34.351563 11.769531 C 37.492188 11.769531 40.8125 13.480469 43.1875 16.433594 C 35.421875 20.691406 36.683594 31.78125 44.527344 34.75 Z M 31.195313 8.46875 C 32.707031 6.527344 33.855469 3.789063 33.4375 1 C 30.972656 1.167969 28.089844 2.742188 26.40625 4.78125 C 24.878906 6.640625 23.613281 9.398438 24.105469 12.066406 C 26.796875 12.152344 29.582031 10.546875 31.195313 8.46875 Z"
                            ></path>
                        </svg>
                        <p>Apple</p>
                    </div>
                </div>
                <p class="login-link">
                    Already have an account?
                    <router-link :to="{ name: 'login' }">Login</router-link>
                </p>
            </div>
            <div class="login-slider">
                <div
                    class="login-slider-inner"
                    :style="{
                        transform: `translateX(-${currentSlide * 400}px)`,
                    }"
                >
                    <img
                        v-for="(src, i) in images"
                        :key="i"
                        :src="src"
                        alt=""
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

import logoURL from "@/assets/logo.svg";

const router = useRouter();
const email = ref("");
const name = ref("");
const password = ref("");
const message = ref("");

const currentSlide = ref(0);
const images = ref([]);

onMounted(async () => {
    const imagePromises = [
        import("@/assets/illustration1.jpg"),
        import("@/assets/illustration2.jpg"),
        import("@/assets/illustration3.jpg"),
    ];
    const resolvedImages = await Promise.all(imagePromises);
    images.value = resolvedImages.map((module) => module.default);
});

let intervalId;
onMounted(() => {
    intervalId = setInterval(() => {
        currentSlide.value = (currentSlide.value + 1) % 3;
    }, 5000);
});

onUnmounted(() => {
    clearInterval(intervalId);
});

async function register() {
    try {
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}register`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: email.value,
                    name: name.value,
                    password: password.value,
                }),
            }
        );
        const data = await response.json();
        message.value = data.message;
        if (response.ok) router.push({ name: "login" });
    } catch (error) {
        message.value = "An error occurred";
    }
}
</script>

<style lang="scss" scoped>
.wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-container {
    display: flex;
    gap: 20px;
}

.login-slider {
    width: 400px;
    overflow: hidden;
}

.login-slider-inner {
    display: flex;
    height: 100%;
    transition: transform 0.5s ease;
}

.login-slider img {
    width: 400px;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.login-card {
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 400px;
}

.logo {
    width: 40px;
}

.login-header {
    margin: 10px 0 25px;
    p {
        color: var(--sub-text);
    }
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.login-input-group {
    display: flex;
    flex-direction: column;
}

.login-input {
    padding: 0.75rem;
    border: 1.5px solid var(--sub-text);
    border-radius: 10px;
    font-size: 1rem;
    transition: border-color 0.1s;
    background: none;
    color: var(--text);
}

.login-input:focus {
    outline: none;
    border-color: var(--primary);
}

.login-button {
    padding: 0.75rem;
    background: var(--accent);
    color: var(--text);
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
}

.login-button:hover {
    background: var(--primary);
}

.login-message {
    text-align: center;
    margin-top: 1rem;
}

.login-message.error {
    color: var(--error);
}

.login-link {
    text-align: center;
    margin-top: 1rem;
    color: var(--sub-text);
    a {
        color: var(--primary);
        text-decoration: none;
    }
}

.login-forget-password {
    align-self: flex-end;
    font-size: 14px;
    cursor: pointer;
    &:hover {
        text-decoration: underline;
    }
}

.login-platforms {
    display: flex;
    align-items: center;
    gap: 10px;
}

.login-platform {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 8px 0;
    border: solid 2px var(--sub-text);
    border-radius: 10px;
    transition: background-color 0.1s;
    cursor: pointer;
    svg {
        height: 18px;
        width: 18px;
    }
    &:hover {
        background-color: var(--primary-200);
    }
}

.login-line-with-text {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 20px 0;
    span {
        flex: 1;
        border-bottom: 1px solid var(--sub-text);
    }
    .text {
        white-space: nowrap;
        padding: 0 10px;
        color: var(--sub-text);
        font-size: 12px;
        font-weight: 400;
    }
}

@media screen and (max-width: 900px) {
    .login-slider {
        display: none;
    }
    .login-card {
        padding: 0;
    }
}
</style>
