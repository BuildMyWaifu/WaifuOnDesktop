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

interface Pose { 
    motion: string,
    expression: string
}

export interface Companion extends Document {
    
    userId: string // 擁有者的ID

    name: string
    description: string // 給使用者看的敘述

    live2dModelSettingPath: string
    poseMap: {
        [key: string]: Pose } // poseMap[poseName]: pose
    
    backstory: string // 角色背景故事
    trait?: {
        role: string,
        personality: string,
        communication_style: string,
        emotional_response: string,
    }

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
    pose?: Pose
}
