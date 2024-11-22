<template>
    
    <v-navigation-drawer>
        <v-container class="d-flex flex-column align-center pt-10" style="height: 100%;">
  
          <!-- <v-sheet class="mb-4" width="60%" color="grey" style="aspect-ratio: 1; border: 4px solid gray; border-radius: 10%;">
            <v-img src="https://upload.wikimedia.org/wikipedia/zh/thumb/f/fc/%E5%8E%9F%E7%A5%9E_%E5%9C%8B%E9%9A%9B%E7%89%88.jpeg/220px-%E5%8E%9F%E7%A5%9E_%E5%9C%8B%E9%9A%9B%E7%89%88.jpeg" 
            alt="image" max-width="100%" max-height="100%" contain style="border-radius: 10%;"></v-img>
          </v-sheet> -->
          <v-row justify="center">
            <v-col class="text-center">
              <v-card-title class="text-h5">
                {{companion.profile.name}}
              </v-card-title>
              <v-card-text class="text-h7">
                {{ companion.profile.description }}
              </v-card-text>
              <v-dialog >

              </v-dialog>
              
            </v-col>
          </v-row>
        </v-container>
      </v-navigation-drawer>
      
        
    
</template>
<script lang="ts" setup>
import { useAppStore } from '@/stores/app';
import { copy } from '@/utils/utils';
import { computed, ref } from 'vue';

const props = defineProps({
  companionId: {
    type: String,
    required: true
  }
})
const companion = computed(() => store.getCompanion(props.companionId) )
const newCompanion = ref()  
// 在開啟 dialog 之後，透過 copy(companion.value) 來初始化 newCompanion
const store = useAppStore()

</script>