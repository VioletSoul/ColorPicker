# Advanced Color Picker Application

![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=flat&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-555555)
![GUI](https://img.shields.io/badge/GUI-PyQt6-41CD52)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9C%93-brightgreen)
![Repo Size](https://img.shields.io/github/repo-size/VioletSoul/ColorPicker)
![Code Size](https://img.shields.io/github/languages/code-size/VioletSoul/ColorPicker)
[![Stars](https://img.shields.io/github/stars/VioletSoul/ColorPicker.svg?style=social)](https://github.com/VioletSoul/ColorPicker)
[![Last Commit](https://img.shields.io/github/last-commit/VioletSoul/ColorPicker.svg)](https://github.com/VioletSoul/ColorPicker/commits/main)

Функциональный инструмент для выбора цвета с поддержкой нескольких цветовых пространств и управлением палитрами.

## Возможности ✨

### Выбор цвета
- **Встроенный системный диалог выбора цвета**
- **Три режима выбора цвета**:
    - RGB (Красный, Зелёный, Синий)
    - HSV (Оттенок, Насыщенность, Яркость)
    - HSL (Оттенок, Насыщенность, Светлота)
- Мгновенное **преобразование цветовых кодов** между пространствами

### Управление палитрой
- **Генерация пользовательской палитры** (7 случайных цветов)
- Сохранение цвета с отображением HEX-кода
- Очистка палитры одним кликом
- Выбор цвета из сохранённых одним нажатием

### Улучшения интерфейса
- Автоматическое копирование HEX-кода в буфер обмена
- Миниатюра выбранного цвета
- Адаптивный интерфейс с продуманным размещением элементов
- Единый стиль оформления всех компонентов

## Установка ⚙️

1. Убедитесь, что установлен **Python 3.9+**
2. Установите зависимости:
```
pip install PyQt6
```
3. Клонируйте репозиторий:
```
git clone https://github.com/VioletSoul/ColorPicker
```

## Использование 🖱️

1. Запустите приложение:
```
python main.py
```
2. Основные элементы управления:
- **Переключатель режима**: RGB/HSV/HSL
- **Поля ввода**: ручной ввод значений
- **Кнопки применения**: подтверждение введённых значений
- **Диалог цвета**: вызов системного выбора цвета
- **Генерация**: создание случайной палитры
- **Очистка**: сброс сохранённых цветов

## Разработка 🛠️

### Требования
- PyQt6 6.4.0+
- Python 3.9+

## Лицензия 📄
MIT License — см. файл [LICENSE](LICENSE) для подробностей

---

**Совет** 💡: Двойной клик по элементу палитры мгновенно скопирует HEX-код!
