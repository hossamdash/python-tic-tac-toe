import sys
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
import socket, threading


class SocketChat:
    def __init__(self):
        self.nickname = "Hossam"
        # Server Ip and Port
        self.IP = "127.0.0.1"
        self.PORT = 55555
        self.client_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        self.connection = True

    def receive(self):
        message = self.client_socket.recv(1024).decode("utf-8")
        return message

    def write(self, msg: str):
        message = msg
        self.client_socket.send(message.encode("utf-8"))
        if message.startswith("/"):
            self.handleCommand(message[1:])

    def handleCommand(self, command: str):
        if command == "exit":
            return 404  # status code for exit


class Example(QWidget):

    winning_states = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def __init__(self):
        super().__init__()
        self.turn = "X"
        self.initUI()
        self.x_score = 0
        self.y_score = 0
        self.chat_object = SocketChat()
        self.chat_object.client_socket.connect(
            (self.chat_object.IP, self.chat_object.PORT)
        )

    def initUI(self):
        self.game_size = 3
        self.buttons = [
            [],
            [],
            [],
        ]
        grid = QGridLayout()
        self.setLayout(grid)

        # buttons
        for i in range(self.game_size):
            for j in range(self.game_size):
                button = QPushButton()
                button.setFixedSize(200, 200)
                button.clicked.connect(self.takeTurn(button))
                font = button.font()
                font.setPointSize(60)
                button.setFont(font)
                grid.addWidget(button, i, j)
                self.buttons[i].append(button)

        # turn label
        self.turn_label = QLabel("{}\nTurn".format(self.turn))
        font = self.turn_label.font()
        font.setPointSize(20)
        self.turn_label.setFont(font)
        grid.addWidget(self.turn_label, self.game_size + 1, 0)
        self.turn_label.setAlignment(Qt.AlignCenter)

        # newgame button
        button = QPushButton("New Game / Reset")
        font = button.font()
        font.setPointSize(15)
        button.setFont(font)
        button.clicked.connect(self.newGame)
        grid.addWidget(button, self.game_size + 1, 1)

        # who wins label
        self.player_won_label = QLabel()
        font = self.player_won_label.font()
        font.setPointSize(15)
        self.player_won_label.setFont(font)
        grid.addWidget(self.player_won_label, self.game_size + 1, 2)
        self.player_won_label.setAlignment(Qt.AlignCenter)

    def newGame(self):
        for row in self.buttons:
            for btn in row:
                btn.setText("")

    def checkGame(self):
        win = ""
        for win_state in Example.winning_states:
            i, j = win_state[0]
            state = self.buttons[i][j].text()
            if state == "":
                continue
            for i, j in win_state:
                if state != self.buttons[i][j].text():
                    break
            else:
                win = state
                print(f"'{win}' wins")
                self.player_won_label.setText("{} has won".format(win))
                self.newGame()

        if win == "":
            empty = False
            for row in self.buttons:
                for btn in row:
                    if btn.text() == "":
                        empty = True

            if not empty:
                print("draw")
                self.newGame()

    def endTurn(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        message = self.chat_object.receive()
        index = ''.join(char for char in message if char.isdigit())
        self.buttons[index[0], index[1]].setText(self.turn)
        self.turn_label.setText("{}\nTurn".format(self.turn))
        self.checkGame()

    def takeTurn(self, button):
        def action():
            if button.text() == "":
                button.setText(self.turn)
                tuple = [
                    (index, row.index(button))
                    for index, row in enumerate(self.buttons)
                    if button in row
                ]
                print(tuple)
                self.chat_object.write(str(tuple))
                self.endTurn()

        return action


def main():
    app = QApplication([])
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
