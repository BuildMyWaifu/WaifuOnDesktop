type Document = {
    _id: string
}

export interface Companion extends Document {
    profile: {
      name: string,
    }
  }

export interface User extends Document {
    profile: {
        avatarId: string,
        name: string,
        email: string,
    }
}
