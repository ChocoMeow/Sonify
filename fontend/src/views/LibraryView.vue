<template>
    <div class="library-view">
        <Tabs>
            <Tab name="Songs"></Tab>
            <Tab name="Playlists"></Tab>
        </Tabs>
    </div>
</template>

<script setup>
import Tabs from "@/components/tab/Tabs.vue";
import Tab from "@/components/tab/Tab.vue";
</script>

<style lang="scss" scoped>
.library-view {
    padding: 20px 0;
}
</style>
