import json
import re
from typing import Any, Union

__all__ = (
    "deserialize",
    "serialize",
)


class FastSExprParser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def skip_whitespace(self):
        while self.pos < self.length and self.text[self.pos].isspace():
            self.pos += 1

    def parse_string(self):
        # Предполагаем, что уже на кавычке
        self.pos += 1  # пропускаем '"'
        start = self.pos

        while self.pos < self.length:
            if self.text[self.pos] == '"':
                result = self.text[start:self.pos]
                self.pos += 1  # пропускаем закрывающую '"'
                return result
            elif self.text[self.pos] == '\\':
                # Обработка escape-последовательностей потребует более сложной логики
                # Для простоты пропускаем
                self.pos += 2
            else:
                self.pos += 1

        # Незакрытая строка
        return self.text[start:]

    def parse_atom(self):
        start = self.pos

        # Читаем до разделителя
        while (self.pos < self.length and
               self.text[self.pos] not in '()," \t\n\r'):
            self.pos += 1

        token = self.text[start:self.pos]

        # Пропускаем запятую если есть
        if self.pos < self.length and self.text[self.pos] == ',':
            self.pos += 1

        # Быстрая проверка типов
        if token == 'null':
            return None
        elif token == 'true':
            return True
        elif token == 'false':
            return False
        elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            return int(token)
        elif '.' in token:
            try:
                return float(token)
            except ValueError:
                return token
        else:
            return token

    def parse_list(self):
        # Предполагаем, что уже на '('
        self.pos += 1  # пропускаем '('
        result = []

        while self.pos < self.length:
            self.skip_whitespace()

            if self.pos >= self.length:
                break

            if self.text[self.pos] == ')':
                self.pos += 1  # пропускаем ')'
                break

            result.append(self.parse_value())
            self.skip_whitespace()

            # Пропускаем запятую если есть
            if self.pos < self.length and self.text[self.pos] == ',':
                self.pos += 1

        return result

    def parse_value(self):
        self.skip_whitespace()

        if self.pos >= self.length:
            return None

        char = self.text[self.pos]

        if char == '(':
            return self.parse_list()
        elif char == '"':
            return self.parse_string()
        else:
            return self.parse_atom()


def deserialize(s: str) -> Any:
    parser = FastSExprParser(s)
    return parser.parse_value()


def serialize(obj: Any) -> str:
    def serialize_item(item, idx):
        if isinstance(item, str):
            if idx == 0 or item.startswith('#') or '.' in item or item in ['true', 'false', 'null']:
                return item
            else:
                return '"' + item.replace('"', '\\"') + '"'
        elif isinstance(item, bool):
            return "true" if item else "false"
        elif item is None:
            return "null"
        elif isinstance(item, (int, float)):
            return str(item)
        elif isinstance(item, list):
            return "(" + ", ".join(
                serialize_item(sub_item, i) for i, sub_item in enumerate(item)) + ")"
        else:
            raise ValueError(f"Cannot serialize item of type {type(item).__name__}")

    return serialize_item(obj, 0)


# Использование:
if __name__ == "__main__":
    with open('paste.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    result = deserialize(data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
