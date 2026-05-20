from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox,
    QInputDialog
)

from api.client import ApiClient


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 CRUD App")
        self.resize(700, 500)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()

        self.btn_load = QPushButton("Load Users")
        self.btn_add = QPushButton("Add User")
        self.btn_update = QPushButton("Update Selected")
        self.btn_delete = QPushButton("Delete Selected")

        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

        self.btn_load.clicked.connect(self.load_users)
        self.btn_add.clicked.connect(self.add_user)
        self.btn_update.clicked.connect(self.update_user)
        self.btn_delete.clicked.connect(self.delete_user)

        self.users = []

    def load_users(self):
        try:
            self.users.clear()
            self.users = ApiClient.get_users()

            self.list_widget.clear()

            for user in self.users:
                self.list_widget.addItem(
                    f"{user['id']} - {user['name']}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_user(self):
        name, ok = QInputDialog.getText(
            self,
            "Add User",
            "Enter user name:"
        )

        if ok and name:
            try:
                user = ApiClient.create_user({
                    "name": name
                })

                self.users.append(user)
                self.list_widget.addItem(f"{user['id']} - {user['name']}")

                QMessageBox.information(
                    self,
                    "Success",
                    f"Created user: {user['name']}"
                )

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def update_user(self):
        row = self.list_widget.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to update.")
            return

        selected_user = self.users[row]

        name, ok = QInputDialog.getText(
            self,
            "Update User",
            "New name:",
            text=selected_user["name"]
        )

        if ok and name:
            try:
                updated_user = ApiClient.update_user(
                    selected_user["id"],
                    {"name": name}
                )

                self.users[row] = updated_user
                self.list_widget.item(row).setText(f"{updated_user['id']} - {updated_user['name']}")

                QMessageBox.information(
                    self,
                    "Success",
                    "User updated"
                )

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def delete_user(self):
        row = self.list_widget.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")
            return

        selected_user = self.users[row]

        try:
            ApiClient.delete_user(selected_user["id"])

            self.users.pop(row)
            self.list_widget.takeItem(row)

            QMessageBox.information(
                self,
                "Success",
                "User deleted"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))