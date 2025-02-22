<template>
    <div class="tabs">
        <div class="tabs__buttons">
            <div
                v-for="tab in tabs"
                :key="tab.name"
                @click="selectTab(tab.name)"
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

const selectTab = (name) => {
    selectedTab.value = name;
};

provide("selectedTab", selectedTab);
provide("addTab", addTab);
provide("selectTab", selectTab);
</script>

<style scoped>
.tabs__buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
</style>
