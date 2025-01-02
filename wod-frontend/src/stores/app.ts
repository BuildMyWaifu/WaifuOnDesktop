// Utilities
import { defineStore } from "pinia";
import { Companion, Message, Sync, User, Pose } from "@/utils/model";
import { fetchApi, handleErrorAlert } from "@/utils/api";
import { electronStoreSet } from "@/utils/electronAPI";

const defaultSync = {
  companion: {},
} as Sync;

export const useAppStore = defineStore("app", {
  state: () => ({
    user: undefined as User | undefined,
    companionList: undefined as Companion[] | undefined,
    messageMap: new Map() as Map<string, Message[]>,
    sync: defaultSync as Sync,
    motionQueue: [] as string[],
    expressionQueue: [] as string[],
  }),
  actions: {
    async loadMessageList(companionId: string, options: { before: number, after: number } = { before: 0, after: 0 }) { 
      let affix = ''
      if (options.before !== 0 ) {
        affix = `?before=${options.before}`
      }
      if (options.after !== 0 ) {
        affix = `?after=${options.after}`
      }
      const messageList = handleErrorAlert(
        await fetchApi(`/message/${companionId}${affix}`),
      ) as Message[] | undefined;
      if (!messageList) {
        return;
      }
      this.messageMap.set(companionId, messageList);
    },
    async loadCompanionList() {
      const companionList = handleErrorAlert(await fetchApi("/companion")) as
        | Companion[]
        | undefined;
      if (!companionList) {
        return;
      }
      this.companionList = companionList;
    },
    async login(user: User) {
      // 當你登入後，將登入取得的使用者資訊傳入此函式
      this.user = user;

      // load companionList
      await this.loadCompanionList();
    },
    async logout() {
      this.user = undefined;
      await electronStoreSet("token", "");
      this.reset()
    },
    reset() {
      this.$reset();
    },
    getCompanion(companionId: string): Companion | undefined {
      if (!this.companionList) {
        return undefined ;
      }
      const companion = this.companionList.find(
        (companion) => companion._id === companionId,
      );
      if (!companion) {
        return undefined; 
      }
      return companion;
    },
    setSync(content: Sync) {
      this.sync = content;
    },
    pushMotion(motion: string) {
      this.motionQueue.push(motion);
    },
    pushExpression(expression: string) {
      this.expressionQueue.push(expression);
    },
    popMotion(): string | undefined {
      return this.motionQueue.shift();
    },
    popExpression(): string | undefined {
      return this.expressionQueue.shift();
    },
    doPose(pose: Pose) {
      if (pose.motion) {
        this.pushMotion(pose.motion)
      }
      if (pose.expression) {
        this.pushExpression(pose.expression)
      }
    }
  },
});
