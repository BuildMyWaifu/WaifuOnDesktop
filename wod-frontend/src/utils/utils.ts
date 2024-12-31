import crypto from 'crypto-js'
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
