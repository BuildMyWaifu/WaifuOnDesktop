import crypto from 'crypto-js'

export function copy (data: Object) {
  return JSON.parse(JSON.stringify(data))
}

export function equal (data1: Object, data2: Object) {
  return JSON.stringify(data1) === JSON.stringify(data2)
}

export function isNotEmpty (data: Object) {
  return (data && Object.keys(data).length > 0)
}

export function hash (input: string) {
  return crypto.SHA256(input).toString()
}
