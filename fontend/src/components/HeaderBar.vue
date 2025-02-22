<template>
    <div class="header">
        <Searchbar />
        <router-link to="/create">
            <Button
                icon="draw"
                name="Generate"
                backgroundColor="var(--accent)"
                hoverColor="var(--secondary)"
                activeColor="var(--secondary-600)"
            />
        </router-link>
    </div>
</template>

<script setup>
import Searchbar from "@/components/Searchbar.vue";
import Button from "@/components/Button.vue";
</script>

<style lang="scss" scoped>
.header {
    display: flex;
    position: sticky;
    padding: 20px 0;
    top: 0px;
    gap: 20px;
    z-index: 1;
    background-color: var(--background);
    margin-top: 2px;
}
</style>
