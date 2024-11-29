<template>
    <div>

    </div>
</template>
<script lang="ts" setup>
    import { Companion } from '@/utils/model';
    import { PropType, ref } from 'vue';

    const companion = ref<Companion>()

    defineProps({
        modelValue: {
            type: Object as PropType<Companion>,
            required: true
        }
    })

    const emits = defineEmits(['update:modelValue'])
    emits('update:modelValue', companion.value)

</script>
