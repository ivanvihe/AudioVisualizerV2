const { app, BrowserWindow, screen, globalShortcut, ipcMain } = require('electron');
const path = require('path');

let cloneWindows = [];
let mainWindow;

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
}

function createCloneWindows() {
  const displays = screen.getAllDisplays();
  cloneWindows = displays.map((display) => {
    const win = new BrowserWindow({
      x: display.bounds.x,
      y: display.bounds.y,
      width: display.bounds.width,
      height: display.bounds.height,
      frame: false,
      show: false,
      alwaysOnTop: true,
      skipTaskbar: true,
      webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
      },
    });
    win.loadFile(path.join(__dirname, 'index.html'));
    return win;
  });
  cloneWindows.forEach((w) => w.show());
}

function closeCloneWindows() {
  cloneWindows.forEach((w) => w.close());
  cloneWindows = [];
}

function toggleClone() {
  if (cloneWindows.length === 0) {
    createCloneWindows();
  } else {
    closeCloneWindows();
  }
}

app.whenReady().then(() => {
  createMainWindow();
  globalShortcut.register('F9', toggleClone);
  ipcMain.handle('toggle-clone', toggleClone);
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
