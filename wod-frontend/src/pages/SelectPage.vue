<template>
  <v-container class="fill-height" style="justify-content: flex-start; align-items: flex-start;">

    <div class="d-flex flex-column">
      <v-btn @click="showMenu" class="mb-2" style="width: 50px; height: 50px; border-radius: 50%;" icon>
        <v-icon>{{ isCardVisible ? 'mdi-menu-open' : 'mdi-menu' }}</v-icon>
      </v-btn>

      <v-card >
        <v-card-text v-if="isCardVisible">
          <div class="d-flex flex-column" >
            <v-btn @click="() => { createWindow('/DisplayPage') }" class="mb-2">to display page</v-btn>
            <v-btn @click="() => { createWindow('/FacetimePage') }" class="mb-2">to facetime page</v-btn>
            <v-btn @click="goHome">back to homepage</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <v-responsive class="align-center fill-height mx-auto" max-width="900" >
      <!-- <v-img class="mb-4" height="150" src="@/assets/logo.png" /> -->

      <div class="text-center">
        <h1 class="text-h3 font-weight">Select Page</h1>
      </div>

      <div class="py-4" />
    </v-responsive>

  </v-container>
</template>
<script setup lang="ts">
import { createWindow, setSize } from '@/utils/electronAPI'
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const isCardVisible = ref(false);
const router = useRouter();

function showMenu(){
  isCardVisible.value = !isCardVisible.value;
  isCardVisible.value ? setSize(800, 450) : setSize(600, 450);
};
function goHome(){
  setSize(600, 450);
  router.push('/');
}
</script>
