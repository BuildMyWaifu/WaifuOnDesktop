<template>
  <v-container class="fill-height">
    <v-responsive class="align-centerfill-height mx-auto" max-width="900">
      <v-img class="mb-4" height="150" src="@/assets/logo.png" />

      <div class="text-center">
        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

        <h1 class="text-h2 font-weight-bold">Vuetify</h1>
      </div>

      <div class="py-4" />
      {{ getVersion() }}
      <v-btn @click="console.log(2)">asdf</v-btn>
      > test test fasdf;asdifj;asdf
      <v-card>
        <v-card-title>set title example</v-card-title>
        <v-card-text>
          <v-text-field v-model="titleValue" />
          <v-btn @click="clickSetTitle">set</v-btn>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>set size</v-card-title>
        <v-btn @click="clickSetSize">set size</v-btn>
      </v-card>
      <v-card title="create new window">
        <v-btn @click="()=>{createWindow('/')}">create another home page</v-btn>
      </v-card>
    </v-responsive>
  </v-container>
</template>
<script setup lang="ts">
  import { createWindow, getVersion, setSize, setTitle } from '@/utils/electronAPI'

  const titleValue = ref('test')
  function clickSetSize () {
    setSize(200, 400)
  }
  function clickSetTitle () {
    setTitle(titleValue.value)
  }
</script>
