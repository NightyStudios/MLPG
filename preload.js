const { contextBridge, ipcRenderer } = require('electron');

// Экспорт функции для вызова списка моделей
contextBridge.exposeInMainWorld('api', {
  fetchModels: async (callback) => {
    const models = await ipcRenderer.invoke('fetch-models');
    callback(models);
  },
});
