// src/auth.js
import { reactive } from "vue";

// API fetch utility
export async function apiFetch(url, options = {}) {
    const token = authState.token;
    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
        throw new Error("API request failed");
    }
    return response.json();
}

// Reactive authentication state with initial load from localStorage
export const authState = reactive({
    token: localStorage.getItem("token") || "",
    currentUser: JSON.parse(localStorage.getItem("currentUser")) || {
        email: "",
        name: "",
        avatarUrl: "",
        userId: "",
    },
});

// Check if user is logged in
export function isLoggedIn() {
    return !!authState.token;
}

// Login function
export async function login(credentials) {
    try {
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}login`, {
            method: "POST",
            body: JSON.stringify(credentials),
        });
        authState.token = data.token;
        localStorage.setItem("token", data.token);
        authState.currentUser = {
            email: data.user.email || "", 
            name: data.user.name || "",
            avatarUrl: data.user.avatarUrl || "",
            userId: data.user.userId || "",
        };
        localStorage.setItem(
            "currentUser",
            JSON.stringify(authState.currentUser)
        );
        return data;
    } catch (error) {
        throw new Error("Login failed");
    }
}

// Logout function
export function logout(router) {
    authState.token = "";
    authState.currentUser = { email: "", name: "", avatarUrl: "", userId: "" };
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    router.push({ name: "home" });
}