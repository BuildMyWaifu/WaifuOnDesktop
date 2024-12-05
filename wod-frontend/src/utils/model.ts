type Document = {
    _id: string
}

export interface SyncCompanionStat {
    window: {
        facetime: boolean
    }  // 目前的設置只是範例，因為目前需要同步的只有視窗的開啟狀態（未來應該還需要同步角色動作）
}

export interface Sync {
    companion: { [key: string]: SyncCompanionStat | undefined } // companion[companionId]: SyncCompanionStat
}

export interface Companion extends Document {
    profile: {
        name: string
        description: string // 給使用者看的敘述
    }
    // avatarId: string // 現階段先不做這部分
    prompt: {
        character: string,
        backstory: string
    }
    userId: string // 擁有者的ID
}

export interface User extends Document {
    profile: {
        avatarId: string,
        name: string,
        email: string,
    }
}
export interface Message extends Document {
    role: string, // 這是人工智慧相關需要的屬性
    companionId: string,
    content: string,
    createdAt: number, // unix timestamp ms
}
