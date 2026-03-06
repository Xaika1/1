import json
import os
from config import TEXTS_FILE, CUSTOM_TEXTS_FILE, SESSION_FILE, WINDOW_SIZE_FILE


def load_texts() -> dict:
    if os.path.exists(TEXTS_FILE):
        with open(TEXTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'easy': [], 'medium': [], 'hard': []}


def copy_default_texts() -> None:
    if not os.path.exists(TEXTS_FILE):
        with open(TEXTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'easy': [], 'medium': [], 'hard': []}, f, ensure_ascii=False, indent=2)


def save_texts(texts: dict) -> None:
    with open(TEXTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)


def load_custom_texts() -> list:
    if os.path.exists(CUSTOM_TEXTS_FILE):
        with open(CUSTOM_TEXTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_custom_texts(texts: list) -> None:
    with open(CUSTOM_TEXTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)


def save_window_size(width: int, height: int, is_fullscreen: bool) -> None:
    with open(WINDOW_SIZE_FILE, 'w', encoding='utf-8') as f:
        f.write(f"{width}|{height}|{1 if is_fullscreen else 0}")


def load_window_size():
    if os.path.exists(WINDOW_SIZE_FILE):
        with open(WINDOW_SIZE_FILE, 'r', encoding='utf-8') as f:
            data = f.read().strip().split('|')
            if len(data) == 3:
                return int(data[0]), int(data[1]), bool(int(data[2]))
    return None, None, None


def save_session(user_id: int, username: str, password: str) -> None:
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        f.write(f"{user_id}|{username}|{password}")


def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r', encoding='utf-8') as f:
            data = f.read().strip().split('|')
            if len(data) == 3:
                return int(data[0]), data[1], data[2]
    return None, None, None


def clear_session() -> None:
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
