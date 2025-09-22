import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap


class DraggableCard(QFrame):

    def __init__(self, text, container):
        super().__init__()
        self.container = container
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setFixedHeight(60)
        self.setStyleSheet("background-color: white; border: 1px solid #888; border-radius: 5px;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.setFixedSize(60, 30)
        self.delete_btn.clicked.connect(self.delete_self)
        layout.addWidget(self.delete_btn)

    def delete_self(self):
        self.container.layout.removeWidget(self)
        self.setParent(None)
        self.deleteLater()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.hide()  # Скрываем исходную карточку
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.label.text())
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            result = drag.exec_(Qt.MoveAction)
            self.show()  # Показываем обратно после завершения drag


class PlaceholderCard(QFrame):
    def __init__(self, height):
        super().__init__()
        self.setFixedHeight(height)
        self.setStyleSheet(
            "border: 2px dashed #aaa; background-color: #fdfdfd; border-radius: 5px;")


class CardContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #f5f0e1;")  # бежевый фон

        self.cards = []
        for i in range(5):
            card = DraggableCard(f"Карточка {i + 1}", self)
            self.layout.addWidget(card)
            self.cards.append(card)

        self.placeholder = None

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        pos = event.pos()
        source = event.source()
        source_height = source.height()
        source_center_y = pos.y()  # позиция курсора относительно контейнера

        insert_index = None
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget == source:
                continue
            widget_center_y = widget.y() + widget.height() / 2

            if source_center_y < widget_center_y:
                insert_index = i
                break

        if insert_index is None:
            insert_index = self.layout.count()

        if self.placeholder is None:
            self.placeholder = PlaceholderCard(source.height())
            self.layout.addWidget(self.placeholder)
        current_index = self.layout.indexOf(self.placeholder)
        if current_index != insert_index:
            self.layout.removeWidget(self.placeholder)
            self.layout.insertWidget(insert_index, self.placeholder)

        event.acceptProposedAction()

    def dropEvent(self, event):
        source = event.source()
        index = self.layout.indexOf(self.placeholder)
        self.layout.removeWidget(source)
        self.layout.insertWidget(index, source)

        self.layout.removeWidget(self.placeholder)
        self.placeholder.deleteLater()
        self.placeholder = None

        event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("MVP Drag & Drop с кнопкой удаления")
    layout = QVBoxLayout(window)

    container = CardContainer()
    layout.addWidget(container)

    window.resize(350, 450)
    window.show()
    sys.exit(app.exec_())
