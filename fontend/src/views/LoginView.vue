<!-- Login.vue -->
<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { login } from "@/auth.js";

const router = useRouter();
const route = useRoute();
const name = ref("");
const password = ref("");
const message = ref("");

async function handleLogin() {
    try {
        await login({ name: name.value, password: password.value });
        message.value = "Login successful";
        router.push(route.query.redirect || "/");
    } catch (error) {
        message.value = "Invalid credentials or server error";
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <h2 class="auth-title">Welcome Back</h2>
            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="input-group">
                    <input
                        v-model="name"
                        placeholder="Username"
                        required
                        class="auth-input"
                    />
                </div>
                <div class="input-group">
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Password"
                        required
                        class="auth-input"
                    />
                </div>
                <button type="submit" class="auth-button">Login</button>
            </form>
            <p
                class="auth-message"
                :class="{ error: message.includes('Invalid') }"
            >
                {{ message }}
            </p>
            <p class="auth-link">
                Don't have an account?
                <router-link to="/register">Register</router-link>
            </p>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); */
}

.auth-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

.auth-title {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.input-group {
    display: flex;
    flex-direction: column;
}

.auth-input {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.auth-input:focus {
    outline: none;
    border-color: #007bff;
}

.auth-button {
    padding: 0.75rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
}

.auth-button:hover {
    background: #0056b3;
}

.auth-message {
    text-align: center;
    margin-top: 1rem;
    color: #666;
}

.auth-message.error {
    color: #dc3545;
}

.auth-link {
    text-align: center;
    margin-top: 1rem;
    color: #666;
}

.auth-link a {
    color: #007bff;
    text-decoration: none;
}
</style>
