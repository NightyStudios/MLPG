document.querySelector('.model-button').addEventListener('click', () => {
  document.querySelector('.sidebar').classList.toggle('open');
});

// ������� ���������� ������ �������
function updateModelList() {
  window.api.fetchModels((models) => {
    const modelsList = document.querySelector('.models-list');
    modelsList.innerHTML = ''; // ������� ������ ����� �����������

    models.forEach((model) => {
      const li = document.createElement('li');
      li.textContent = model;
      li.classList.add('model-item');
      modelsList.appendChild(li);

      // ��������� ���������� ����� ��� �������� ���� ��������
      li.addEventListener('click', () => {
        openActionModal(model);
      });
    });
  });
}

// ��������� ��������� ��� ���������� ������ ������ �������
setInterval(updateModelList, 1000);

// ���������� ������ Download
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
      input.value = ''; // ������� ���� �����
    } else {
      alert(`Failed to download model "${modelName}".`);
    }
  });
});

// �������� ���������� ���� ��������
function openActionModal(modelName) {
  const modal = document.querySelector('.modal');
  const modelTitle = document.querySelector('.modal-model-name');
  const deleteButton = document.querySelector('.delete-button');

  // ������������� �������� ������
  modelTitle.textContent = modelName;

  // ��������� ���������� ��� ������ "Delete"
  deleteButton.onclick = () => {
    window.api.deleteModel(modelName, (success) => {
      if (success) {
        alert(`Model "${modelName}" deleted successfully!`);
        modal.style.display = 'none'; // ��������� ����
      } else {
        alert(`Failed to delete model "${modelName}".`);
      }
    });
  };

  // ���������� ��������� ����
  modal.style.display = 'block';
}

// �������� ���������� ���� ��� ������� �� ���
document.querySelector('.modal').addEventListener('click', (event) => {
  if (event.target === document.querySelector('.modal')) {
    document.querySelector('.modal').style.display = 'none';
  }
});
