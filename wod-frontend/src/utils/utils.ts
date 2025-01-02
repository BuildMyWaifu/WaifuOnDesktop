import crypto from 'crypto-js'
import { Companion } from '../utils/model'
export function copy(data: object) {
  return JSON.parse(JSON.stringify(data))
}

export function equal(data1: object, data2: object) {
  return JSON.stringify(data1) === JSON.stringify(data2)
}

export function isNotEmpty(data: object) {
  return (data && Object.keys(data).length > 0)
}

export function hash(input: string) {
  return crypto.SHA256(input).toString()
}

// TODO: 在這裡寫一個檢查 companion 是否合法的函數，並且在更新時檢查

export function isCompanionValid(companion: Companion) {
  if (companion.name.length > 20 || companion.name.length < 1) {
    return false
  } else if (companion.description.length > 100 || companion.description.length < 1) {
    return false
  } else if (companion.backstory.length > 500 || companion.backstory.length < 1) {
    return false
  } else if (!isNotEmpty(companion.poseMap)) {
    return false
  } else if (companion.live2dModelSettingPath == '')   {
    return false
  }
  else {
    return true
  }
  
}