from config import TEXT_LENGTHS, SCORE_MULTIPLIERS, ERROR_PENALTY


def calc_rank(accuracy: float, errors: int) -> str:
    if accuracy == 100 and errors == 0:
        return 'S'
    elif accuracy >= 95:
        return 'A'
    elif accuracy >= 85:
        return 'B'
    elif accuracy >= 75:
        return 'C'
    elif accuracy >= 60:
        return 'D'
    return 'E'


def get_difficulty(content_length: int) -> str:
    if content_length < TEXT_LENGTHS['easy']:
        return 'easy'
    elif content_length <= TEXT_LENGTHS['medium']:
        return 'medium'
    return 'hard'


def check_char_match(expected: str, actual: str) -> bool:
    if expected == actual:
        return True
    if expected in 'ёЁ' and actual in 'еЕ':
        return True
    return False
