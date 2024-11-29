<template>
    <div>

    </div>
</template>
<script lang="ts" setup>
    import { Companion } from '@/utils/model';
    import { PropType } from 'vue';


    defineProps({
        modelValue: {
            type: Object as PropType<Companion>,
            required: true
        }
    })

    const emits = defineEmits(['update:modelValue'])

</script>
