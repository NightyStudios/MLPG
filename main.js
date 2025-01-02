const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let mainWindow;

// Функция получения списка моделей
function fetchModels(callback) {
  exec('mlpg list', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing mlpg list: ${error.message}`);
      callback([]);
      return;
    }
    if (stderr) {
      console.warn(`Warning: ${stderr}`);
    }

    const models = stdout
      .split('\n')
      .map((line) => line.trim())
      .filter(
        (line) =>
          line !== '' &&
          line !== 'Hugging Face rules the world :3' &&
          line !== '------------------------------'
      );
    callback(models);
  });
}

// IPC-обработчик для получения списка моделей
ipcMain.handle('fetch-models', async () => {
  return new Promise((resolve) => {
    fetchModels((models) => {
      resolve(models);
    });
  });
});

// IPC-обработчик для скачивания модели
ipcMain.handle('download-model', async (event, modelName) => {
  return new Promise((resolve) => {
    exec(`mlpg install ${modelName}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error downloading model: ${error.message}`);
        resolve(false);
        return;
      }
      if (stderr) {
        console.warn(`Warning: ${stderr}`);
      }
      resolve(true);
    });
  });
});

// IPC-обработчик для удаления модели
ipcMain.handle('delete-model', async (event, modelName) => {
  return new Promise((resolve) => {
    exec(`mlpg delete ${modelName}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error deleting model: ${error.message}`);
        resolve(false);
        return;
      }
      if (stderr) {
        console.warn(`Warning: ${stderr}`);
      }
      resolve(true);
    });
  });
});

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  mainWindow.loadFile('index.html');
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
