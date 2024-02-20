import os


class User:
    def __init__(self, password):
        self.password = password
        self.my_files = [
            [
                "Single Line Calculator",
                f"{cur_path}\\Calculator- single-line.py",
                (0, 0),
            ],
            ["Tic-Tac-Toe", f"{cur_path}\\Tic-Tac-Toe.py", (1, 0)],
        ]

        self.settheme("light")

    def my_buttons(self, my_files):
        self.buttons = {}
        for x in my_files:
            if x[2] != None:
                self.buttons[x[2]] = {"state": "active", "fname": x[0], "address": x[1]}
        for i in range(8):
            for j in range(10):
                if (i, j) not in self.buttons:
                    self.buttons[(i, j)] = {
                        "state": "disabled",
                        "fname": "",
                        "address": "",
                    }
        return self.buttons

    def settheme(self, theme):
        if theme == "light":
            self.theme = "light"
            self.appbg = "white"
            self.iconbg = "RoyalBlue3"
            self.taskbg = "orange"
            self.textbg = "black"
        else:
            self.theme = "dark"
            self.appbg = "black"
            self.iconbg = "RoyalBlue3"  # TBA
            self.taskbg = "orange"  # TBA
            self.textbg = "white"


users = ["Guest", "Admin"]
cur_path = os.path.dirname(os.path.abspath(__file__))
Admin = User("admin")

Guest = User("")
