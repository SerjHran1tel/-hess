# -hess

-hess — это простая шахматная игра, написанная на Python с использованием библиотеки Pygame. Поддерживает базовые шахматные правила, включая рокировку, взятие на проходе и превращение пешек.

## Требования

- **Python**: 3.6 или выше
- **Pygame**: 2.0.0 или выше (см. `requirements.txt`)

## Установка

Следуйте этим шагам, чтобы установить и запустить игру:

### 1. Клонирование репозитория
Склонируйте репозиторий на свой компьютер:

```bash
  git clone https://github.com/SerjHran1tel/-hess
```

### 2. Установка зависимостей
Установите необходимые библиотеки из `requirements.txt`:

```bash
  pip install -r requirements.txt
```

### 3. Проверка структуры проекта
Убедитесь, что структура проекта выглядит так:
```
pychess/
├── board.py         # Логика шахматной доски и ходов
├── figures.py       # Классы шахматных фигур
├── params.py        # Константы и параметры игры
├── game.py          # Основной файл с игровым циклом
├── requirements.txt # Список зависимостей
├── sprites/         # Папка с изображениями фигур
│   ├── whiteKing.png
│   ├── blackKing.png
│   ├── whiteQueen.png
│   ├── blackQueen.png
│   └── ... (другие фигуры: Pawn, Rook, Knight, Bishop)
└── README.md
```

**Примечание**: Папка `sprites/` должна содержать изображения всех фигур в формате PNG (например, `whitePawn.png`, `blackRook.png`). Если их нет, добавьте свои изображения с соответствующими именами.

### 4. Запуск игры
Запустите игру:

```bash
  python game.py
```

## Управление
- **Левая кнопка мыши**: Выбор фигуры и выполнение хода.
- **Выход**: Нажмите крестик на окне игры.

## Особенности
- Базовые шахматные правила.
- Визуализация доступных ходов и шаха.
- Выбор фигуры при превращении пешки (ферзь, ладья, слон, конь).

## Известные ограничения
- Нет AI-оппонента (игра только для одного игрока).
- Начальная расстановка фигур нестандартная: короли и ферзи перепутаны местами.
- Низкий FPS (60 кадров/с), что может сделать игру менее плавной.
- Не все специальные ходы полностью протестированы.