/* eslint-disable @typescript-eslint/no-require-imports */
import { app, BrowserWindow, ipcMain, webContents, nativeImage } from 'electron/main'
import { join } from 'node:path'
import process from 'node:process';
import Store from 'electron-store';

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const store = new Store()
const icon = nativeImage.createFromPath('src/assets/BMW_icon.png')
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
let lastSync = undefined

ipcMain.on('window:set-title', (event, title) => {
  const webContents = event.sender
  const win = BrowserWindow.fromWebContents(webContents)
  win.setTitle(title)
})
ipcMain.on('window:create', (event, url) => {
  createWindow(url)
})
ipcMain.on('window:set-size', (event, width, height) => {
  const webContents = event.sender
  const win = BrowserWindow.fromWebContents(webContents)
  win.setBounds({ width, height })
})

ipcMain.on('sync:fetch', (event) => {
  if (lastSync) {
    event.sender.send('sync:broadcast', lastSync)
  }
})

ipcMain.on('sync:submit', (event, content) => {
  lastSync = content
  webContents.getAllWebContents().map((webContent) => {
    webContent.send('sync:broadcast', content)
  })
})
ipcMain.handle('store:get', async (_event, key) => {
  return store.get(key); // 返回值將作為 Promise 的解析值
});

ipcMain.handle('store:set', async (_event, key, val) => {
  store.set(key, val);
});


const createWindow = url => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: icon,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
    },
  })
  win.removeMenu()
  let baseUrl = 'http://localhost:3000'
  if (url) {
    baseUrl = baseUrl + url
  }

  win.loadURL(baseUrl, { frame: false })// 使用 Vue 的開發伺服器地址
  return win
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
