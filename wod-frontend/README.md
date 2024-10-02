# develop

1. `npm run dev`
2. `npm run electron`

`src/main.ts` 是 vue 前端的進入點
`main.js` 是 electron 桌面的進入點

由於我們目前是開發中，所以需要先用第一個指令編譯出網頁，再用第二個指令，把網頁，和一些額外的程式，包裝成應用程式

由於安全性的可量，作業系統相關的操作規定只能在主緒（electron 緒）上執行
而使用者操作的 vuetify 前端會在 渲染緒 上執行
緒之間溝通需要透過 ipc
