# Это MLPG!
## MLPG расшифровывается как Machine Learning PlayGround (песочница для машинного обучения)

Этот проект будет полезен для для начинающих ML-инженеров и продвинутых пользователей, которые хотят начать тестировать собственные модели ИИ и модели сообщества!

> [!NOTE]
> Учтите, что проект все еще активно разрабатывается и поддержка моделей вводится постепенно. Их список доступен в файле `list_models.py`.

## Инструкция по установке

MLPG поставляется в двух видах: настольное приложение и консольная утилита.

1. Склонируйте репозиторий GitHub на ваш компьютер
`git clone https://github.com/NightyStudios/MLPG`
2. Создайте виртуальное conda-окружение:
`conda create --name MLPG python=3.12`
И активируйте его:
`conda activate MLPG`
3. Установите sentencepiece:
`conda install conda-forge::sentencepiece`
4. Установите необходимые библиотеки:
`pip install -r requirements.txt`

> [!NOTE]
> Данный проект рассчитан на использование технологии CUDA. Если вы хотите запускать модели на процессоре - установите PyTorch для CPU. (Замените torch==2.6.0+cu126 --extra-index-url https://download.pytorch.org/whl/cu126 на torch в requirements.txt)
### Запустите графический интерфейс:
`python UI.py`
### Или воспользуйтесь консольной утилитой:
* Windows
`mlpg -h`
* Linux/MacOS
`mlpg.py -h`
