const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('electronAPI', {
  setTitle: title => ipcRenderer.send('window:set-title', title),
  setSize: (width, height) => ipcRenderer.send('window:set-size', width, height),
  createWindow: url => ipcRenderer.send('window:create', url),
})
contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron,
  // 除函数之外，我们也可以暴露变量
})
