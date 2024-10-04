<template>
  <v-container class="fill-height">
    <v-responsive class="align-centerfill-height mx-auto" max-width="900">
      <v-img class="mb-4" height="150" src="@/assets/logo.png" />

      <div class="text-center">
        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

        <h1 class="text-h2 font-weight-bold">Vuetify</h1>
      </div>

      <div class="py-4" />
      <v-btn @click="resizeWindow">test resize 1</v-btn>
      <v-btn @click="console.log(2)">asdf</v-btn>
>
      test

      test
      fasdf;asdifj;asdf
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
  function resizeWindow () {
    // 獲取 Electron 的窗口對象
    alert(`本应用正在使用 Chrome (v${window.versions.chrome()}), Node.js (v${window.versions.node()}), 和 Electron (v${window.versions.electron()})`)
    // const { remote } = require('electron')
    // console.log(remote)
    // const currentWindow = remote.getCurrentWindow()

    // // 設置新的窗口大小
    // currentWindow.setSize(1024, 1024, true) // 修改為您想要的大小
    // currentWindow.center()
  }

</script>
