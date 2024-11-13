
import { Sync } from "./model"

/* eslint-disable @typescript-eslint/no-explicit-any */
export function setTitle (newTitle: string) {
  (window as any).electronAPI.setTitle(newTitle)
}
export function getVersion () {
  return {
    chrome: (window as any).versions.chrome(),
    node: (window as any).versions.node(),
    electron: (window as any).versions.electron(),
  }
}
export function setSize (width: number, height: number) {
  (window as any).electronAPI.setSize(width, height)
}

export function createWindow (url: string) {
  (window as any).electronAPI.createWindow(url)
}

export function broadcast(sync: Sync) {
(window as any).electronAPI.broadcast(JSON.stringify(sync))
}

export function setBroadcastCallback(callback: (sync: Sync) => void) {
  (window as any).electronAPI.onBroadcast(callback)
}

export function fetchSync() {
  (window as any).electronAPI.fetch()
}