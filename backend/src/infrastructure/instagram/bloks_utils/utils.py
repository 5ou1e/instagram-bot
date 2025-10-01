import json

from src.infrastructure.instagram.bloks_utils.igbloks.scripts import parser


def find_action(action, action_name: str | None = None, arg_value: str | None = None):
    if not isinstance(action, list) or len(action) == 0:
        return None

    valid = True  # Начинаем с True

    # Проверяем action_name если передан
    if action_name:
        valid = action[0] == action_name

    # Проверяем arg_value если передан (и предыдущие проверки прошли)
    if arg_value and valid:
        valid = arg_value in action

    if valid:
        return action

    # Рекурсивно ищем во всех элементах списка
    for item in action:
        if isinstance(item, list):
            result = find_action(item, action_name, arg_value)  # Передаем оба параметра
            if result:
                return result

    return None


def find_action_by_arg(action, arg_value: str):
    if not isinstance(action, list) or len(action) == 0:
        return None

    # Проверяем текущий элемент
    if find_action_by_arg in action[:]:
        return action

    # Рекурсивно ищем во ВСЕХ элементах списка
    for item in action:
        if isinstance(item, list):
            result = find_action(item, arg_value)
            if result:
                return result

    return None


def parse_nested_json(data):
    """Рекурсивно парсит вложенные JSON-строки"""
    if isinstance(data, str):
        try:
            # Пробуем распарсить строку как JSON
            parsed = json.loads(data)
            # Рекурсивно обрабатываем результат
            return parse_nested_json(parsed)
        except json.JSONDecodeError:
            # Если не JSON - возвращаем как есть
            return data
    elif isinstance(data, dict):
        # Для словаря обрабатываем каждое значение
        return {k: parse_nested_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Для списка обрабатываем каждый элемент
        return [parse_nested_json(item) for item in data]
    else:
        # Для остальных типов возвращаем как есть
        return data


def deserialize_bloks_action(action: str):
    return parser.deserialize(action)
