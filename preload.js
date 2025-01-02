const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  fetchModels: async (callback) => {
    const models = await ipcRenderer.invoke('fetch-models');
    callback(models);
  },
  downloadModel: async (modelName, callback) => {
    const success = await ipcRenderer.invoke('download-model', modelName);
    callback(success);
  },
  deleteModel: async (modelName, callback) => {
    const success = await ipcRenderer.invoke('delete-model', modelName);
    callback(success);
  },
});
