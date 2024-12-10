const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let mainWindow;

// Функция для вызова Python-скрипта
function fetchModels(callback) {
  const pythonScriptPath = path.join(__dirname, 'list_models.py');

  exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Ошибка выполнения Python-скрипта: ${error.message}`);
      callback([]);
      return;
    }
    if (stderr) {
      console.error(`Ошибка в Python-скрипте: ${stderr}`);
    }

    try {
      const models = JSON.parse(stdout); // Парсим JSON
      callback(models);
    } catch (err) {
      console.error('Ошибка парсинга JSON:', err.message);
      callback([]);
    }
  });
}

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Ссылка на новый preload.js
    },
  });

  mainWindow.loadFile('index.html');
});

// IPC-обработчик для передачи данных
ipcMain.handle('fetch-models', async () => {
  return new Promise((resolve) => {
    fetchModels((models) => {
      resolve(models);
    });
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
