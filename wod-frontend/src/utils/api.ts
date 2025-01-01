import { electronStoreGet } from "./electronAPI";


export async function fetchApi (path: string = '') {
  try {
    const token = await electronStoreGet("token"); 
    const response = await fetch(`/api${path}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`, // 使用 token
      },
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export async function postApi(path: string = '', data: object) {
  try {
    const token = await electronStoreGet("token");
    const response = await fetch(`/api${path}`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`, // 使用 token
      },
      body: JSON.stringify(data),
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export async function rawPostApi(path: string = "", data: FormData) {
  try {

    const token = await electronStoreGet("token");
    const response = await fetch(`/api${path}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`, // 使用 token
      },
      body: data,
      credentials: "include",
    });
    return await response.json();
  }
  catch (error) {
    return new Promise((resolve) => {
      resolve({ status: "error", message: `在請求時發生錯誤${error}` });
    });
  }
}

export async function patchApi (path = '', data: object) {
  try {
    const token = await electronStoreGet("token"); 
    const response = await fetch(`/api${path}`, {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`, // 使用 token
      },
      body: JSON.stringify(data),
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export async function deleteApi (path = '') {
  try {
    const token = await electronStoreGet("token"); 
    const response = await fetch(`/api${path}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`, // 使用 token
      }
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export function handleErrorAlert (res: { status: NonNullable<'success' | 'error' | 'info' | 'warning'>, message: string, data: object }) {
  if (res.status === 'success') {
    return res.data
  } else {
    alert(res.message)
  }
}

// export function handleErrorSnackbar (res: { status: NonNullable<'success' | 'error' | 'info' | 'warning'>, message: string, data: object }) {
//   const store = useViewStore()
//   if (res.status === 'success') {
//     return res.data
//   } else {
//     store.addSnackbar(res)
//   }
// }
