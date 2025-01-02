<template>
    <v-card v-if="localCompanion" style="height: 100vh;width: 100vw" class="d-flex flex-column overflow-y-auto">
        <div class="pl-8 pt-4">
            你正在編輯伴侶
        </div>
        <div class="pl-8 py-2">
            <v-btn prepend-icon="mdi-arrow-left" text="返回" :to="`/app/${companionId}`" flat></v-btn>
        </div>

        <div style="padding-left: 100px;padding-right: 100px;">
            <v-btn size="large" color="success" block variant="tonal" :disabled="!isCompanionValid(localCompanion)"
                @click="updateCompanion">儲存</v-btn>
        </div>
        <CompanionEdit v-model="localCompanion" flat></CompanionEdit>
    </v-card>
</template>
<script lang="ts" setup>
    import { ref, computed, onMounted } from 'vue'
    import { Companion } from '@/utils/model'
    import CompanionEdit from '@/components/CompanionEdit.vue'
    import { useRoute } from 'vue-router';
    import { useAppStore } from '@/stores/app';
    import { copy, isCompanionValid } from '@/utils/utils';
    import { patchApi } from '@/utils/api';
    const route = useRoute()
    function getCompanionId() {
        if ("companionId" in route.params && route.params.companionId) {
            return route.params.companionId as string;
        }
    }
    const companionId = getCompanionId() as string;
    const store = useAppStore();
    const companion = computed(() => store.getCompanion(companionId))
    const localCompanion = ref<Companion>();

    onMounted(() => {
        if (!companion.value) {
            alert("載入時，找不到對應的companion");
            return;
        }
        localCompanion.value = copy(companion.value);
    })

    async function updateCompanion() {
        if (!localCompanion.value) {
            alert("儲存時，找不到對應的companion");
            return;
        }
        const res = await patchApi(`/companion/${companionId}`, {
            name: localCompanion.value.name,
            description: localCompanion.value.description,
            live2dModelSettingPath: localCompanion.value.live2dModelSettingPath,
            poseMap: localCompanion.value.poseMap,
            backstory: localCompanion.value.backstory,
        });
        alert(res.message);

    }
</script>