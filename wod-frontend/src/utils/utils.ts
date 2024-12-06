import crypto from 'crypto-js'

export function getCookie(cname: string) {
  const name = cname + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


export function copy (data: object) {
  return JSON.parse(JSON.stringify(data))
}

export function equal (data1: object, data2: object) {
  return JSON.stringify(data1) === JSON.stringify(data2)
}

export function isNotEmpty (data: object) {
  return (data && Object.keys(data).length > 0)
}

export function hash (input: string) {
  return crypto.SHA256(input).toString()
}
