/* eslint-disable @typescript-eslint/no-require-imports */
import { app, BrowserWindow, ipcMain, webContents } from 'electron/main'
import { join } from 'node:path'
import process  from 'node:process';

import { fileURLToPath } from 'url';
import { dirname } from 'path';


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
  event.sender.send('sync:broadcast', lastSync)
})

ipcMain.on('sync:submit', (event, content) => {
  lastSync = content
   webContents.getAllWebContents().map((webContent) => {
    webContent.send('sync:broadcast', content)
  })
})

const createWindow = url => {
  const win = new BrowserWindow({
    width: 600,
    height: 450,
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
