<template>
    <div class="tabs">
        <div class="tabs__buttons">
            <div
                v-for="tab in tabs"
                :key="tab.name"
                @click="handleTabClick(tab)"
                tabindex="0"
                role="button"
                :aria-pressed="selectedTab === tab.name"
            >
                <Button
                    :icon="tab.icon"
                    :name="tab.name"
                    :isToggle="selectedTab === tab.name"
                />
            </div>
        </div>
        <div class="tabs__content">
            <slot />
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, provide } from "vue";
import Button from "@/components/Button.vue";

const selectedTab = ref("");
const tabs = reactive([]);

const addTab = (tab) => {
    tabs.push(tab);
    if (!selectedTab.value) {
        selectedTab.value = tab.name;
    }
};

const handleTabClick = async (tab) => {
    selectedTab.value = tab.name;

    if (tab.asyncFunction) {
        await tab.asyncFunction();
    }
};

provide("selectedTab", selectedTab);
provide("addTab", addTab);
</script>

<style scoped>
.tabs__buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
</style>
