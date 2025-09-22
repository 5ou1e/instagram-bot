from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
)
import qdarkstyle
import sys


def main():
    app = QApplication(sys.argv)

    # Изначально тёмная тема
    dark_theme = True
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    # Главное окно
    window = QWidget()
    window.setWindowTitle("PySide6: динамическая смена темы")
    window.resize(400, 300)

    layout = QVBoxLayout()

    label = QLabel("Пример текста")
    layout.addWidget(label)

    line_edit = QLineEdit()
    line_edit.setPlaceholderText("Введите текст")
    layout.addWidget(line_edit)

    text_edit = QTextEdit()
    text_edit.setPlaceholderText("Многострочный текст")
    layout.addWidget(text_edit)

    button1 = QPushButton("Кнопка 1")
    layout.addWidget(button1)

    button2 = QPushButton("Кнопка 2")
    layout.addWidget(button2)

    # Кнопка для переключения темы
    toggle_button = QPushButton("Сменить тему")
    layout.addWidget(toggle_button)

    def toggle_theme():
        nonlocal dark_theme
        dark_theme = not dark_theme
        if dark_theme:
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            app.setStyleSheet("")  # пустой стиль → дефолтная светлая тема

    toggle_button.clicked.connect(toggle_theme)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
