type Document = {
    _id: string
}

export interface Companion extends Document {
    profile: {
      name: string,
      role: string
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
}
