// Utilities
import { defineStore } from 'pinia'
import { Companion, User } from '@/utils/model'

export const useAppStore = defineStore('app', {
  state: () => ({
    user: undefined as User| undefined,
    companionList: [] as Companion[],
  }),
  actions: {
    login (user: User) {
      // 當你登入後，將登入取得的使用者資訊傳入此函式
      this.user = user
    },
  },
})
