# import json
# from datetime import datetime
#
# from bloks_parser import BloksParser
# from src.infrastructure.instagram.bloks_utils.utils import find_action, deserialize_bloks_action
# from tools.bloks_tools.bloks_processor import ExpansionContext, BloksExpander
#
# import json
# import re
#
# from tools.bloks_tools.parser import deserialize
#
# # # Загружаем тестовые данные
# with open(
#         r"C:\Python\Мои проекты\insta-bot\tools\bloks_tools\response_with_challenge.json",
#         "r", encoding="utf-8") as file:
#     response = json.loads(file.read())
#
# def test_expansion():
#     """Тестирование развертывания Bloks структур"""
#
#     parser = BloksParser(response)
#     structure = parser.parse_action()
#     print(structure)
#
#
# if __name__ == "__main__":
#     start = datetime.now()
#     for i in range(1):
#         test_expansion()
#     print(datetime.now()-start)
