import pygame


class Board:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(10)]


class PlayWithFriend(Board):
    pass


class PlayWithBot(Board):
    pass


class Play(PlayWithBot):
    pass
