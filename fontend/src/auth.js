// src/auth.js
import { reactive } from "vue";

export async function apiFetch(url, options = {}) {
    const token = authState.token;
    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    let response = await fetch(url, { ...options, headers });
    if (response.status === 401 && authState.refreshToken) {
        try {
            await refreshAccessToken();
            headers.Authorization = `Bearer ${authState.token}`;
            response = await fetch(url, { ...options, headers });
        } catch (error) {
            throw new Error("Session expired, please log in again");
        }
    }

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }
    return response.json();
}

export const authState = reactive({
    token: localStorage.getItem("token") || "",
    refreshToken: localStorage.getItem("refreshToken") || "",
    currentUser: JSON.parse(localStorage.getItem("currentUser")) || {
        email: "",
        name: "",
        avatarUrl: "",
        userId: "",
    },
});

export function isLoggedIn() {
    return !!authState.token;
}

export async function login(credentials) {
    try {
        const loginData = await apiFetch(
            `${import.meta.env.VITE_API_URL}login`,
            {
                method: "POST",
                body: JSON.stringify(credentials),
            }
        );

        authState.token = loginData.access_token;
        authState.refreshToken = loginData.refresh_token;
        localStorage.setItem("token", loginData.access_token);
        localStorage.setItem("refreshToken", loginData.refresh_token);

        const userData = await apiFetch(`${import.meta.env.VITE_API_URL}me`);
        authState.currentUser = {
            email: userData.email || "",
            name: userData.name || "",
            avatarUrl: userData.avatarUrl || "",
            userId: userData.userId || "",
        };
        localStorage.setItem(
            "currentUser",
            JSON.stringify(authState.currentUser)
        );

        return { token: loginData.access_token, user: userData };
    } catch (error) {
        throw new Error("Login failed");
    }
}

export async function refreshAccessToken() {
    try {
        const refreshData = await fetch(
            `${import.meta.env.VITE_API_URL}refresh`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh_token: authState.refreshToken }),
            }
        );

        if (!refreshData.ok) {
            throw new Error("Refresh failed");
        }

        const data = await refreshData.json();
        authState.token = data.access_token;
        localStorage.setItem("token", data.access_token);
        return data.access_token;
    } catch (error) {
        authState.token = "";
        authState.refreshToken = "";
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        throw new Error("Token refresh failed");
    }
}

export function logout(router) {
    authState.token = "";
    authState.refreshToken = "";
    authState.currentUser = { email: "", name: "", avatarUrl: "", userId: "" };
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("currentUser");
    router.push({ name: "home" });
}
