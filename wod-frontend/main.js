const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('node:path')
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

const createWindow = (url) => {
  const win = new BrowserWindow({
    width: 600,
    height: 450,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  })
  let baseUrl = 'http://localhost:3000'
  if (url) {
    baseUrl = baseUrl + url
  }

  win.loadURL(baseUrl, { frame: false })// 使用 Vue 的開發伺服器地址
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
