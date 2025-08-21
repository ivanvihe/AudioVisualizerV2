const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  toggleClone: () => ipcRenderer.invoke('toggle-clone'),
});
