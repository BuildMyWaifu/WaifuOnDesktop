// Utilities
import { defineStore } from "pinia";
import { Companion, Message, Sync, User } from "@/utils/model";
import { fetchApi, handleErrorAlert } from "@/utils/api";

const defaultSync = {
  companion: {},
} as Sync;

export const useAppStore = defineStore("app", {
  state: () => ({
    user: undefined as User | undefined,
    companionList: undefined as Companion[] | undefined,
    messageMap: new Map() as Map<string, Message[]>,
    sync: defaultSync as Sync,
  }),
  actions: {
    async login(user: User) {
      // 當你登入後，將登入取得的使用者資訊傳入此函式
      this.user = user;

      // load companionList
      const companionList = handleErrorAlert(await fetchApi("/companion")) as
        | Companion[]
        | undefined;
      if (!companionList) {
        return;
      }
      this.companionList = companionList;
    },
    logout() {
      this.user = undefined;
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      this.reset();
    },
    reset() {
      this.$reset();
    },
    getCompanion(companionId: string): Companion {
      if (!this.companionList) {
        throw new Error("Companion list not loaded");
      }
      const companion = this.companionList.find(
        (companion) => companion._id === companionId,
      );
      if (!companion) {
        throw new Error(`Companion ${companionId} not found`);
      }
      return companion;
    },
    generateMockCompanionList() {
      if (!this.user) {
        return;
      }
      this.companionList = [
        {
          _id: "咪醬",
          userId: this.user._id,
          profile: {
            name: "咪醬",
            description: "可愛又元氣滿滿的貓娘女僕，喜歡撒嬌和主人喵～！",
          },
          prompt: {
            character: "元氣可愛的貓娘女僕",
            backstory:
              "咪醬天生就是一隻充滿愛與熱情的貓娘，最喜歡主人，讓主人的每一天都充滿幸福和快樂喵！",
          },
        },
        {
          _id: "test 2",
          userId: this.user._id,
          profile: {
            name: "test name 1",
            description: "asdf",
          },
          prompt: {
            character: "asf",
            backstory: "asdf",
          },
        },
        {
          _id: "test 3",
          userId: this.user._id,
          profile: {
            name: "test name 1",
            description: "asdf",
          },
          prompt: {
            character: "asf",
            backstory: "asdf",
          },
        },
      ];
    },
    generateMockMessages() {
      if (!this.companionList) {
        throw new Error("Companion list not loaded");
      }
      for (const companion of this.companionList) {
        const messages: Message[] = [];
        for (let i = 0; i < 10; i++) {
          messages.push({
            _id: `test message ${i}`,
            role: i % 2 === 1 ? "bot" : "user",
            companionId: companion._id,
            content: `test message content ${i}`,
            createdAt: new Date().getTime(),
          });
        }
        this.messageMap.set(companion._id, messages);
      }
    },
    setSync(content: Sync) {
      this.sync = content;
    },
  },
});
