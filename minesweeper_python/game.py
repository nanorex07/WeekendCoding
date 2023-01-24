from tkinter import Frame, Tk, Canvas, IntVar, Label, StringVar
from config import Settings
import random


class Game(Canvas):
    def __init__(self, root):
        super(Game, self).__init__()
        self.master = root
        self.config(
            bg="#ffffff",
            highlightthickness=0,
            height=Settings.height * Settings.box_s,
            width=Settings.width * Settings.box_s,
            bd=0,
        )
        self._new()

    def _new(self):
        self.bind("<Button-1>", self._tile_click)
        self.bind("<Button-3>", self._add_marker)

        self.un_visited = Settings.width * Settings.height - Settings.bombs
        self.master.game_status.set("")
        self.master.flags_unplaced.set(Settings.bombs)
        self.grid = [[0 for _ in range(Settings.width)] for _ in range(Settings.height)]
        self.visited = [
            [0 for _ in range(Settings.width)] for _ in range(Settings.height)
        ]
        self._pop_grid()
        self._show_grid()

    def _add_marker(self, event):
        c, r = event.x // Settings.box_s, event.y // Settings.box_s
        if self.visited[r][c] == 0:
            self.visited[r][c] = 2
            if self.grid[r][c] == -1:
                self.master.flags_unplaced.set(self.master.flags_unplaced.get() - 1)
        elif self.visited[r][c] == 2:
            self.visited[r][c] = 0
            if self.grid[r][c] == -1:
                self.master.flags_unplaced.set(self.master.flags_unplaced.get() + 1)
        self._show_grid()

    def _pop_grid(self):
        count: int = Settings.bombs
        bombs: list = []
        while count:
            r = random.randint(0, Settings.height - 1)
            c = random.randint(0, Settings.width - 1)
            if self.grid[r][c] != -1:
                self.grid[r][c] = -1
                bombs.append([r, c])
                count -= 1
        for bomb in bombs:
            for rr in range(bomb[0] - 1, bomb[0] + 2):
                for cc in range(bomb[1] - 1, bomb[1] + 2):
                    if (
                        rr >= 0
                        and rr < Settings.height
                        and cc >= 0
                        and cc < Settings.width
                        and self.grid[rr][cc] != -1
                        and (rr != bomb[0] or cc != bomb[1])
                    ):
                        self.grid[rr][cc] += 1

    def _end(self):
        self.unbind("<Button-1>")
        self.unbind("<Button-3>")
        self.master.game_status.set("Done !!" if self.un_visited == 0 else "Oops!")

    def _tile_click(self, event):
        c, r = event.x // Settings.box_s, event.y // Settings.box_s

        def _dfs(r, c):
            if self.visited[r][c]:
                return
            self.visited[r][c] = 1
            self.un_visited -= 1
            if self.grid[r][c] > 0:
                return
            for rr in range(r - 1, r + 2):
                for cc in range(c - 1, c + 2):
                    if (
                        rr >= 0
                        and rr < Settings.height
                        and cc >= 0
                        and cc < Settings.width
                        and self.grid[rr][cc] != -1
                        and (rr != r or cc != c)
                        and self.visited[rr][cc] == 0
                    ):
                        _dfs(rr, cc)

        if self.grid[r][c] == -1:
            self.visited = [
                [1 for _ in range(Settings.width)] for _ in range(Settings.height)
            ]
            self._end()
        else:
            _dfs(r, c)

        if self.un_visited == 0:
            self._end()
        self._show_grid()

    def _draw_tile(self, r: int, c: int, x: int, y: int):
        if self.visited[r][c] == 0:
            self.create_rectangle(
                x,
                y,
                x + Settings.box_s,
                y + Settings.box_s,
                fill="#afb2b7",
                activefill="#d7d8da",
            )
            return
        if self.visited[r][c] == 2:
            self.create_rectangle(
                x,
                y,
                x + Settings.box_s,
                y + Settings.box_s,
                fill="#afb2b7",
                activefill="#d7d8da",
            )
            self.create_text(
                x + Settings.box_s // 2,
                y + Settings.box_s // 2,
                justify="center",
                text="⚑",
                font=Settings.font_block,
            )
            return

        text = str(self.grid[r][c])
        match self.grid[r][c]:
            case -1:
                fill = "#ffffff"
                text = "⬤"
            case _:
                fill = "#ffffff"
        self.create_rectangle(
            x,
            y,
            x + Settings.box_s,
            y + Settings.box_s,
            fill=fill,
            activefill="#ffffff",
        )
        self.create_text(
            x + Settings.box_s // 2,
            y + Settings.box_s // 2,
            justify="center",
            text=text,
            font=Settings.font_block,
        )

    def _show_grid(self):
        self.delete("all")
        x: int = 0
        y: int = 0
        while y <= Settings.height * Settings.box_s:
            x = 0
            while x <= Settings.width * Settings.box_s:
                r = y // Settings.box_s
                if r == Settings.height:
                    r -= 1
                c = x // Settings.box_s
                if c == Settings.width:
                    c -= 1
                self._draw_tile(r, c, x, y)
                x += Settings.box_s
            y += Settings.box_s


class MainFrame(Frame):
    def __init__(self, root):
        super(MainFrame, self).__init__()
        self.flags_unplaced: IntVar = IntVar()
        self.game_status: StringVar = StringVar()
        self.master = root

        self.tf: Frame = Frame(self, bg="#ffffff")
        Label(self.tf, textvariable=self.game_status, font=Settings.font_info).grid(
            row=0, column=0
        )
        Label(self.tf, text="⚑:", font=Settings.font_info).grid(row=0, column=1)
        lb = Label(self.tf, textvariable=self.flags_unplaced, font=Settings.font_info)
        lb.grid(row=0, column=2)
        self.tf.pack(expand=1, fill="y", side="top")

        self.canv: Canvas = Game(self)
        self.canv.pack(expand=1, fill="both", side="bottom")


class Minesweeper:
    @classmethod
    def play(cls):
        root: Tk = Tk()
        mainf: Frame = MainFrame(root)
        mainf.pack(expand=1, fill="both")
        root.title(Settings.title)
        root.resizable(0, 0)
        root.config(background="#ffffff")
        root.mainloop()
