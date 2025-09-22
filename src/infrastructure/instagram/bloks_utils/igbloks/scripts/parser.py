import pyparsing as pp

__all__ = (
    "deserialize",
    "serialize",
)

# Определить элементы базового парсера
LPAREN, RPAREN = map(pp.Suppress, "()")

# Числа с плавающей точкой (включая отрицательные)
float_number = pp.Regex(r"[+-]?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?")
float_number.setParseAction(lambda t: float(t[0]))

# Целые числа (включая отрицательные)
integer = pp.Regex(r"[+-]?\d+(?![.\d])")
integer.setParseAction(lambda t: int(t[0]))

# Объединяем числа
number = float_number | integer

# Строки
string = pp.QuotedString('"', escChar="\\")

# Идентификаторы - включая те, что начинаются с #
# # обозначает ссылку на функцию в Bloks
identifier = pp.Regex(r"[#a-zA-Z_][a-zA-Z0-9_.:]*")

# Ключевые слова
true = pp.Keyword("true").setParseAction(pp.replaceWith(True))
false = pp.Keyword("false").setParseAction(pp.replaceWith(False))
null = pp.Keyword("null").setParseAction(pp.replaceWith(None))

# Forward reference для рекурсивных структур
value = pp.Forward()

# Массивы/вызовы функций
array = pp.Group(LPAREN + pp.Optional(pp.delimitedList(value)) + RPAREN)

# Определение value - порядок важен!
value <<= true | false | null | number | string | identifier | array

# Главный парсер
parser = value


def deserialize(__s: str) -> list[str | int | float | bool | None | list]:
    result = parser.parseString(__s, parseAll=True)
    return result.asList()[0] if result else []


def serialize(__l: list[str | int | float | bool | None | list]) -> str:
    def serialize_item(item, i):
        if isinstance(item, str):
            # Проверяем, начинается ли строка с # (это ссылка на функцию)
            # или это идентификатор (содержит точки или начинается с букв)
            if (
                i == 0
                or item.startswith("#")
                or "." in item
                or item in ["true", "false", "null"]
            ):
                # Это идентификатор или ссылка на функцию - не заключаем в кавычки
                return item
            else:
                # Это строковый литерал - заключаем в кавычки
                return '"' + item.replace('"', '\\"') + '"'
        elif isinstance(item, bool):
            return "true" if item else "false"
        elif item is None:
            return "null"
        elif isinstance(item, (int, float)):
            return str(item)
        elif isinstance(item, list):
            return (
                "("
                + ", ".join(
                    serialize_item(sub_item, idx) for idx, sub_item in enumerate(item)
                )
                + ")"
            )
        else:
            raise ValueError(f"Cannot serialize item of type {type(item).__name__}")

    return serialize_item(__l, 0)
