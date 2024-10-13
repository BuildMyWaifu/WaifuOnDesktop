<template>
  <v-app>

    <v-navigation-drawer>
      <v-list three-line>
        <template #prepend>
          <v-avatar />
        </template>

        <v-list-item v-for="companion in store.companionList" :key="companion._id">
          <v-list-item-title>{{ companion._id }}</v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="store.messageMap.get(companion._id)">
              {{ lastMessage(companion._id)?.content || 'No messages yet' }}
            </div>
          </v-list-item-subtitle>
        </v-list-item>


      </v-list>
      <template #append>
        <div class="d-flex justify-center">
          <router-link class="text-grey" to="/">
            回到主頁面
          </router-link>
        </div>
        <div class="d-flex">
          <v-spacer />
          <v-btn stacked>設定</v-btn>
          <v-btn stacked>登出</v-btn>
        </div>
        <v-list-item v-if="store.user" lines="three">
          <v-list-item-title>
            {{ store.user?.profile.name }}
          </v-list-item-title>
        </v-list-item>
      </template>
    </v-navigation-drawer>
    <v-app-bar>
      老婆名稱
    </v-app-bar>
    <v-main>
      <v-container style="max-height: 80vh; overflow: auto">
        chat interface
        <!-- <pre><code>{{ store.messageMap }}</code></pre> -->
        
        <div v-if="store.messageMap.get('test 1')">

          <div v-if="lastMessage('test 1')">
            Last message from waifu: {{ lastMessage('test 1')?.content || 'No messages yet' }}
          </div>

          <v-list-item v-for="(message, index) in store.messageMap.get('test 1')" :key="index">
            <v-list-item-title>{{ message.role }}:</v-list-item-title>
            <v-list-item-subtitle>{{ message.content }}</v-list-item-subtitle>
          </v-list-item>
          
        </div>
        

      </v-container>
    </v-main>
  </v-app>
</template>
<script setup lang="ts">
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const lastMessage = (Id: string) => {
  const messages = store.messageMap.get(Id);
  return messages ? messages[messages.length - 1] : null;
}

</script>
