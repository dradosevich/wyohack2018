const {app, BrowserWindow} = require('electron')

let main_window = null
let ready = false

function init_main_window (){

  let main_window = new BrowserWindow({width: 1200, height: 600, backgroundColor: '#d5d5d5'})
  main_window.webContents.openDevTools()
  main_window.loadFile('index.html')
  main_window.show()
}

app.on('ready',init_main_window)
