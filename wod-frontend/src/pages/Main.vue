<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-navigation-drawer app location="left" permanent>

      <v-list lines="two" select-strategy="single-independent" width="256">
        <template #prepend>
          <v-avatar /> <!-- avatar for Companion -->
        </template>

        <v-list-item v-show="store.companionList == undefined">
          <v-card-text class="d-flex text-center">
            載入伴侶列表中
          </v-card-text>
        </v-list-item>

        <v-list-item v-show="store.companionList != undefined && store.companionList.length == 0">
          <v-card-text class="d-flex text-center">
            伴侶列表為空
          </v-card-text>
        </v-list-item>

        <v-list-item v-for="companion in store.companionList" :key="companion._id" :value="companion._id"
          @click="updateCurrentCompanion(companion._id)">
          <v-list-item-title>{{ companion.profile.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-caption">{{ companion.profile.description }}</v-list-item-subtitle>
          <div class="text-body-2" v-if="store.messageMap.get(companion._id) && lastMessage(companion._id)">
            {{ lastMessage(companion._id)?.role == 'bot' ? companion.profile.name : '您' }}：{{
              lastMessage(companion._id)?.content }}
          </div>
        </v-list-item>

        <v-divider />
      </v-list>

      <div class="text-center">
        <CreateNewWife />
      </div>

      <template #append>
        <v-divider />
        <v-list-item v-if="store.user" lines="three">

          <v-list-item-title>
            {{ store.user?.profile.name }}
          </v-list-item-title>

          <template #append>
            <v-menu offset-y>
              <template #activator="{ props }">
                <v-btn v-bind="props" icon="mdi-cog" variant="text" />
              </template>
              <!-- 彈出選單內容 -->
              <v-list>
                <v-list-item to="/">
                  <v-list-item-title>回到主頁面</v-list-item-title>
                </v-list-item>
                <v-list-item @click="openUserSetting">
                  <v-list-item-title>設定</v-list-item-title>
                </v-list-item>
                <v-list-item @click="logout">
                  <v-list-item-title>登出</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <UserSetting v-if="isUserSettingOpen" @close="isUserSettingOpen = false" />
          </template>

        </v-list-item>

        <v-list-item v-else>
          <v-list-item-title>
            目前尚未登入
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-btn to="/login">登入</v-btn>
          </v-list-item-subtitle>
        </v-list-item>
        
      </template>
    </v-navigation-drawer>

    <v-main app>
      <CompanionPreview v-if="currentCompanionId !== null" :companionId="currentCompanionId"></CompanionPreview>
    </v-main>

  </v-app>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify';
import CompanionPreview from '@/components/CompanionPreview.vue';
import CreateNewWife from '@/components/CreateNewWife.vue';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';

const store = useAppStore();
const router = useRouter();
const display = useDisplay();

const currentCompanionId = ref<string | null>(null);
const leftDrawer = computed(() => display.smAndUp); // 小屏幕以上顯示
const rightDrawer = computed(() => display.mdAndUp); // 中屏幕以上顯示

const isPermanentLeft = computed(() => display.smAndUp); // 固定左側抽屜
const isPermanentRight = computed(() => display.mdAndUp); // 固定右側抽屜

const lastMessage = (Id: string) => {
  const messages = store.messageMap.get(Id);
  return messages ? messages[messages.length - 1] : undefined;
};

const updateCurrentCompanion = (Id: string) => {
  currentCompanionId.value = currentCompanionId.value === Id ? null : Id;
};

const goToSettings = () => {
  console.log('Setting');
};

const logout = () => {
  store.logout();
  router.push('/');
};

</script>

<style scoped></style>
