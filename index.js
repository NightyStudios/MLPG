document.querySelector('.model-button').addEventListener('click', () => {
  document.querySelector('.sidebar').classList.toggle('open');
});

// Функция обновления списка моделей
function updateModelList() {
  window.api.fetchModels((models) => {
    const modelsList = document.querySelector('.models-list');
    modelsList.innerHTML = ''; // Очистка списка перед обновлением

    models.forEach((model) => {
      const li = document.createElement('li');
      li.textContent = model;
      li.classList.add('model-item');
      modelsList.appendChild(li);

      // Добавляем обработчик клика для открытия окна действий
      li.addEventListener('click', () => {
        openActionModal(model);
      });
    });
  });
}

// Установка интервала для обновления списка каждую секунду
setInterval(updateModelList, 1000);

// Обработчик кнопки Download
document.querySelector('.search-bar button').addEventListener('click', () => {
  const input = document.querySelector('.search-bar input');
  const modelName = input.value.trim();

  if (!modelName) {
    alert('Please enter a model name.');
    return;
  }

  window.api.downloadModel(modelName, (success) => {
    if (success) {
      alert(`Model "${modelName}" downloaded successfully!`);
      input.value = ''; // Очищаем поле ввода
    } else {
      alert(`Failed to download model "${modelName}".`);
    }
  });
});

// Открытие модального окна действий
function openActionModal(modelName) {
  const modal = document.querySelector('.modal');
  const modelTitle = document.querySelector('.modal-model-name');
  const deleteButton = document.querySelector('.delete-button');

  // Устанавливаем название модели
  modelTitle.textContent = modelName;

  // Добавляем обработчик для кнопки "Delete"
  deleteButton.onclick = () => {
    window.api.deleteModel(modelName, (success) => {
      if (success) {
        alert(`Model "${modelName}" deleted successfully!`);
        modal.style.display = 'none'; // Закрываем окно
      } else {
        alert(`Failed to delete model "${modelName}".`);
      }
    });
  };

  // Показываем модальное окно
  modal.style.display = 'block';
}

// Закрытие модального окна при нажатии на фон
document.querySelector('.modal').addEventListener('click', (event) => {
  if (event.target === document.querySelector('.modal')) {
    document.querySelector('.modal').style.display = 'none';
  }
});
