document.querySelector('.model-button').addEventListener('click', () => {
  document.querySelector('.sidebar').classList.toggle('open');

  // Вызов fetchModels для обновления списка моделей
  window.api.fetchModels((models) => {
    const modelsList = document.querySelector('.models-list');
    modelsList.innerHTML = ''; // Очистить список перед обновлением

    models.forEach((model) => {
      const li = document.createElement('li');
      li.textContent = model;
      modelsList.appendChild(li);
    });
  });
});
