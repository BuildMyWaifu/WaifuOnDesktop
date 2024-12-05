// import { useViewStore } from '@/store/view'

export async function fetchApi (path: string = '') {
  try {
    const response = await fetch(`/api${path}`, {
      method: 'GET',
      credentials: 'include',
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export async function postApi (path: string = '', data: object) {
  try {
    const response = await fetch(`/api${path}`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
    })

    return await response.json()
  } catch (error) {
    return new Promise(resolve => {
      resolve({ status: 'error', message: `在請求時發生錯誤${error}` })
    })
  }
}

export async function patchApi (path = '', data: object) {
  try {
    const response = await fetch(`/api${path}`, {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
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
    const response = await fetch(`/api${path}`, {
      method: 'DELETE',
      credentials: 'include',
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
