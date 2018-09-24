#!/usr/bin/env python3

import os
import configparser
import itertools

import tkinter
from tkinter.constants import *

from Board import Board
from Engine import Engine
from Point import Point


class UIGame(object):
    """Game for the UI"""

    # index to column conversion
    _idx_to_col = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

    def __init__(self, canvas, statustext):
        # self.board = Board('1GG1G/1GGGT/1GGGG/GGTGG/GTGTG t g0 c3 mA3')
        self.board = Board()

        self.canvas = canvas
        self.statustext = statustext

        self.cids = []
        self.from_idx = None

        self.tiger_radius = 20
        self.goat_radius = 20

        self.board_grid_x = [30, 130, 230, 330, 430]
        self.board_grid_y = [30, 130, 230, 330, 430]
        self.board_rect = [2, 2, 462, 462]

        self.game = None
        self.win = ''
        self.ai_turn = True

        self.config = configparser.ConfigParser(defaults={
            'goatcolor': 'gray',
            'tigercolor': 'yellow'
        })
        self.config.add_section('ui')
        self.goat_color = self.config.get('ui', 'goatcolor')
        self.tiger_color = self.config.get('ui', 'tigercolor')

        self.draw_board()

    def calc_board_pos(self):
        self.canvas.winfo_width()
        self.canvas.winfo_height()

    def draw_board(self):
        self.calc_board_pos()
        self.canvas.create_rectangle(*self.board_rect, fill='white')

        board_min_x = self.board_grid_x[0]
        board_max_x = self.board_grid_x[-1]
        board_min_y = self.board_grid_y[0]
        board_max_y = self.board_grid_y[-1]
        board_center_x = self.board_grid_x[2]
        board_center_y = self.board_grid_y[2]

        for x in self.board_grid_x:
            self.canvas.create_line(x, board_min_y, x, board_max_y)

        for y in self.board_grid_y:
            self.canvas.create_line(board_min_x, y, board_max_x, y)

        self.canvas.create_line(board_min_x, board_min_y,
                                board_max_x + 1, board_max_y + 1)
        self.canvas.create_line(board_min_x, board_max_y,
                                board_max_x, board_min_y)

        self.canvas.create_line(board_center_x, board_min_y,
                                board_max_x, board_center_y)
        self.canvas.create_line(board_max_x, board_center_y,
                                board_center_x, board_max_y)
        self.canvas.create_line(board_center_x, board_max_y,
                                board_min_x, board_center_y)
        self.canvas.create_line(board_min_x, board_center_y,
                                board_center_x, board_min_y)

    def canvas_to_logical(self, x, y):
        ri, rj = None, None

        for i, gx in enumerate(self.board_grid_x):
            for j, gy in enumerate(self.board_grid_y):
                if (x - gx) ** 2 + (y - gy) ** 2 < 100:
                    ri, rj = i, j

        if (ri, rj) == (None, None):
            raise Exception()

        return ri, rj

    @staticmethod
    def get_ui_coord(x, y):
        return "%s%s" % (UIGame._idx_to_col[x], y + 1)

    def move_goat(self, ev):
        i, j = self.canvas_to_logical(ev.x, ev.y)
        self.from_idx = Point.get_index(UIGame.get_ui_coord(i, j))

    def move_goat2(self, ev):
        if self.from_idx is not None:

            i, j = self.canvas_to_logical(ev.x, ev.y)
            to_idx = Point.get_index(UIGame.get_ui_coord(i, j))

            if (
                    self.board.is_movable(self.from_idx, to_idx) and
                    self.board.points[self.from_idx].get_state() == Point.State.G
            ):
                move = Board.Move(f=self.from_idx, t=to_idx, mt=Board.MoveType.M)
            else:
                move = None

            self.from_idx = None
            self.apply_move(move)

    def move_tiger(self, ev):
        i, j = self.canvas_to_logical(ev.x, ev.y)
        self.from_idx = Point.get_index(UIGame.get_ui_coord(i, j))

    def move_tiger2(self, ev):
        if self.from_idx is not None:

            i, j = self.canvas_to_logical(ev.x, ev.y)
            to_idx = Point.get_index(UIGame.get_ui_coord(i, j))

            # determine if this is a move or a capture
            if (
                    self.board.is_movable(self.from_idx, to_idx) and
                    self.board.points[self.from_idx].get_state() == Point.State.T
            ):
                move = Board.Move(f=self.from_idx, t=to_idx, mt=Board.MoveType.M)
            elif self.board.can_capture(self.from_idx, to_idx):
                move = Board.Move(f=self.from_idx, t=to_idx, mt=Board.MoveType.C)
            else:
                move = None

            self.from_idx = None
            self.apply_move(move)

    def place_goat(self, ev):
        i, j = self.canvas_to_logical(ev.x, ev.y)
        idx = Point.get_index(UIGame.get_ui_coord(i, j))

        if self.board.points[idx].get_state() == Point.State.E:
            move = Board.Move(f=idx, t=idx, mt=Board.MoveType.P)
        else:
            move = None

        self.apply_move(move)

    def apply_move(self, move):
        if not move:
            self.statustext.set('Invalid move!')
        else:
            self.board.make_move(move)
            self.check_win()
            self.ai_turn = not self.ai_turn
        self.draw()

    def draw(self):
        # here we could scale the canvas for a nice fit of the board
        # to the window size
        self.canvas.unbind('<Button-1>')
        for cid in self.cids:
            self.canvas.delete(cid)

        if not self.board.winner:
            self.statustext.set('Turn: %s | R: %d | D: %d' %
                                (self.board.turn, self.board.goatsToBePlaced, self.board.deadGoats))

            if not self.ai_turn:
                if self.board.turn == Board.Player.G:
                    if self.board.goatsToBePlaced > 0:
                        self.canvas.bind('<Button-1>', self.place_goat)
                    else:
                        self.canvas.bind('<ButtonPress-1>', self.move_goat)
                        self.canvas.bind('<ButtonRelease-1>', self.move_goat2)
                elif self.board.turn == Board.Player.T:
                    self.canvas.bind('<ButtonPress-1>', self.move_tiger)
                    self.canvas.bind('<ButtonRelease-1>', self.move_tiger2)
            else:
                self.statustext.set('Thinking')
                # self.canvas.bind('<Button-1>', self.make_ai_move)
                self.make_ai_move()

        tr = self.tiger_radius
        sr = self.goat_radius

        # display the tigers and goats on the ui board
        for entry, (y, x) in zip(Board._get_full_position(self.board.position.split()[0]),
                                 itertools.product(self.board_grid_x,
                                                   self.board_grid_y)):
            if entry == "T":
                self.cids.append(self.canvas.create_oval(x - tr, y - tr,
                                                         x + tr, y + tr,
                                                         fill=self.tiger_color))

            elif entry == "G":
                self.cids.append(self.canvas.create_oval(x - sr, y - sr,
                                                         x + sr, y + sr,
                                                         fill=self.goat_color))

    def check_win(self):
        # read the current board position
        if self.board.winner == Board.Player.T:
            # self.game.wait()
            # self.game = None
            self.statustext.set('Tigers win!')
            self.win = 'tigers'
            return

        elif self.board.winner == Board.Player.G:
            # self.game.wait()
            # self.game = None
            self.statustext.set('Goats win!')
            self.win = 'goats'
            return

    def new(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.expanduser('uiconf'))

        if self.config.has_option('game', 'ai'):
            if self.config.get('game', 'ai').lower() == 'goat':
                self.ai_turn = True
            elif self.config.get('game', 'ai').lower() == 'tiger':
                self.ai_turn = False
        else:
            pass

        if self.config.has_option('game', 'aistrength'):
            aistrength = self.config.get('game', 'aistrength')
        else:
            aistrength = 6

        # self.win = ''
        self.init_ai(int(aistrength))
        # self.engine.make_best_move()
        # self.check_win()
        self.draw()

    def init_ai(self, aistrength):
        self.ai_vs_ai = False
        self.board = Board()
        self.engine = Engine(self.board, depth=aistrength)

    def make_ai_move(self, ev=None):
        move = self.engine.get_best_move()
        self.apply_move(move)


def configure():
    config = configparser.ConfigParser()
    config.add_section('game')
    config.read(os.path.expanduser('uiconf'))

    conftoplevel = tkinter.Toplevel(tk)
    conftoplevel.title('Configuration')

    tkinter.Label(conftoplevel, text='Computer plays:').pack()

    aivar = tkinter.StringVar()

    if config.has_option('game', 'ai'):
        if config.get('game', 'ai').lower() == 'goat':
            aivar.set('goat')
        elif config.get('game', 'ai').lower() == 'tiger':
            aivar.set('tiger')

    goat = tkinter.Radiobutton(conftoplevel, text='Goat', variable=aivar,
                               value='goat')
    tiger = tkinter.Radiobutton(conftoplevel, text='Tiger', variable=aivar,
                                value='tiger')

    goat.pack()
    tiger.pack()

    tkinter.Label(conftoplevel, text='AI depth').pack()
    aistrengthvar = tkinter.IntVar()

    if config.has_option('game', 'aistrength'):
        aistrengthvar.set(config.getint('game', 'aistrength'))
    else:
        aistrengthvar.set(3)

    tkinter.Entry(conftoplevel, textvariable=aistrengthvar).pack()

    def save():
        config.set('game', 'ai', aivar.get())
        config.set('game', 'aistrength', str(aistrengthvar.get()))
        with open(os.path.expanduser('uiconf'), 'w') as fp:
            config.write(fp)
        conftoplevel.destroy()

    def cancel():
        conftoplevel.destroy()

    savebutton = tkinter.Button(conftoplevel, text='Save', command=save)
    cancelbutton = tkinter.Button(conftoplevel, text='Cancel', command=cancel)
    savebutton.pack()
    cancelbutton.pack()


def about():
    abouttext = """\
This is the graphical frontend for the baghchal
baghchal engine."""
    toplevel = tkinter.Toplevel(tk)
    tkinter.Label(toplevel, text=abouttext, justify=LEFT).pack()


def rules():
    import webbrowser
    webbrowser.open("https://en.wikipedia.org/wiki/Bagh_Chal")


tk = tkinter.Tk()
tk.title('BaghChal')

tk.resizable(0, 0)

frame = tkinter.Frame(tk)
frame.pack(fill=BOTH, expand=1)

canvas = tkinter.Canvas(frame, width=460, height=460)
canvas.pack(fill=BOTH, expand=1, side=TOP, padx=1, pady=1)

statustext = tkinter.StringVar()
status = tkinter.Label(frame, textvariable=statustext,
                       borderwidth=2, relief=RIDGE)
status.pack(expand=1, side=BOTTOM, fill=X)

game = UIGame(canvas, statustext)
tk.bind('<Control-n>', lambda event: game.new())
# tk.bind('<Control-u>', lambda event: game.undo())

menu = tkinter.Menu(tk)
tk['menu'] = menu

gamemenu = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label='Game', menu=gamemenu)

gamemenu.add_command(label='New Game', command=game.new)
gamemenu.add_separator()
gamemenu.add_command(label='Undo')
gamemenu.add_separator()
gamemenu.add_command(label='Quit', command=tk.destroy)

settings = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label='Settings', menu=settings)

settings.add_command(label='Preferences', command=configure)

hhelp = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=hhelp)

hhelp.add_command(label='Rules', command=rules)
hhelp.add_command(label='About', command=about)

game.new()
tk.mainloop()
