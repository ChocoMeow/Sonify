<!-- Register.vue -->
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const name = ref("");
const password = ref("");
const message = ref("");

async function register() {
    try {
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}register`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name.value,
                    password: password.value,
                }),
            }
        );
        const data = await response.json();
        message.value = data.message;
        if (response.ok) router.push("/login");
    } catch (error) {
        message.value = "An error occurred";
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <h2 class="auth-title">Create Account</h2>
            <form @submit.prevent="register" class="auth-form">
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
                <button type="submit" class="auth-button">Register</button>
            </form>
            <p
                class="auth-message"
                :class="{ error: message.includes('error') }"
            >
                {{ message }}
            </p>
            <p class="auth-link">
                Already have an account?
                <router-link to="/login">Login</router-link>
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
