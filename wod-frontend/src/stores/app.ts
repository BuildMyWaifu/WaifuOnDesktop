// Utilities
import { defineStore } from 'pinia'
import { Companion, Message, User } from '@/utils/model'

export const useAppStore = defineStore('app', {
  state: () => ({
    user: undefined as User| undefined,
    companionList: [
      {
        _id: 'test 1',
        profile: {
          name: 'test name 1',
          description: 'asdf',
        },
        prompt: {
          character: 'asf',
          backstory: 'asdf',
        },
      },
      {
        _id: 'test 2',
        profile: {
          name: 'test name 1',
          description: 'asdf',
        },
        prompt: {
          character: 'asf',
          backstory: 'asdf',
        },
      },
      {
        _id: 'test 3',
        profile: {
          name: 'test name 1',
          description: 'asdf',
        },
        prompt: {
          character: 'asf',
          backstory: 'asdf',
        },
      },
    ] as Companion[],
    messageMap: new Map() as Map<string, Message[]>,
  }),
  actions: {
    login (user: User) {
      // 當你登入後，將登入取得的使用者資訊傳入此函式
      this.user = user
    },
    logout () {
      this.user = undefined
    },
    generateMockMessages () {
      for (const companion of this.companionList) {
        const messages: Message[] = []
        for (let i = 0; i < 10; i++) {
          messages.push({
            _id: `test message ${i}`,
            role: (i % 2 === 1) ? 'bot' : 'user',
            companionId: companion._id,
            content: `test message content ${i}`,
            createdAt: new Date().getTime(),
          })
        }
        this.messageMap.set(companion._id, messages)
      }
    },
  },
})
