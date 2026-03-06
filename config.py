import os

APP_DATA_PATH = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(APP_DATA_PATH, 'typing_trainer.db')
TEXTS_FILE = os.path.join(APP_DATA_PATH, 'texts.json')
SESSION_FILE = os.path.join(APP_DATA_PATH, 'session.txt')
CUSTOM_TEXTS_FILE = os.path.join(APP_DATA_PATH, 'custom_texts.json')
WINDOW_SIZE_FILE = os.path.join(APP_DATA_PATH, 'window_size.txt')

TEXT_LENGTHS = {'easy': 100, 'medium': 250}
MIN_TEXT_LENGTH = 50
SCORE_MULTIPLIERS = {'easy': 1, 'medium': 2, 'hard': 3, 'custom': 1}
ERROR_PENALTY = 10
TIMER_INTERVAL_MS = 100
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 550

THEME = {
    'bg': '#1a1a1a', 'card': '#2a2a2a', 'light': '#3a3a3a',
    'red': '#d32f2f', 'red_light': '#ef5350', 'green': '#4caf50',
    'text': '#e0e0e0', 'text_muted': '#9e9e9e',
    'ranks': {'S': '#ffd700', 'A': '#c0c0c0', 'B': '#cd7f32', 'C': '#8b4513', 'D': '#696969', 'E': '#4a4a4a'},
    'rank_descs': {'S': 'Идеально!', 'A': 'Отлично!', 'B': 'Хорошо!', 'C': 'Неплохо', 'D': 'Можно лучше', 'E': 'Нужно тренироваться'},
    'diff_names': {'easy': 'Лёгкий', 'medium': 'Средний', 'hard': 'Сложный', 'custom': 'Пользовательский'},
    'diff_colors': {'easy': '#4caf50', 'medium': '#f57c00', 'hard': '#d32f2f', 'custom': '#9e9e9e'},
    'diff_icons': {'easy': '●', 'medium': '●', 'hard': '●', 'custom': '★'}
}
