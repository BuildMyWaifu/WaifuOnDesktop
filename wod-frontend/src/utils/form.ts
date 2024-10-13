export function required (v: string) {
  return !!v || '此欄位不得留空'
}
export function email (v: string) {
  return !v ||
        /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
        '請輸入電子郵件'
}

export function password (v: string) {
  if (!v || v.length < 8) {
    return '密碼長度至少為8'
  }

  if (!/[a-z]/.test(v)) {
    return '密碼必須包含至少一個小寫字母'
  }

  if (!/[A-Z]/.test(v)) {
    return '密碼必須包含至少一個大寫字母'
  }

  if (!/\d/.test(v)) {
    return '密碼必須包含至少一個數字'
  }

  return true
}
