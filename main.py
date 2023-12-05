import numpy as np
import pygame as pg
from collections import deque
from random import randrange

# import numba


class MainApp:
    """главное приложения
    """
    def __init__(self, WIDTH=512, HEIGHT=512, CELL_SIZE=8) -> None:
        """Инициализация приложения

        Args:
            WIDTH (int, optional):  Высота окна. Defaults to 512.
            HEIGHT (int, optional): Ширина окна. Defaults to 512.
            CELL_SIZE (int, optional): Размер клетки (самого автомата). Defaults to 8.
        """
        pg.init()
        
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.screen.fill((255, 255, 255))

        self.font = pg.font.Font(None, 30)
        

        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

        self.grid = np.zeros((self.COLS, self.ROWS))

        self.surface_count = pg.Surface((50, 50))
        self.surface_count.fill((255, 255, 255))

        self.__ant = Ant(app=self, pos=[self.COLS // 2, self.ROWS // 2], color=(0, 0, 0))


    @staticmethod
    def get_color() -> tuple:
        """Вернет рандомный цвет в формате RGB (255, 255, 255)

        Returns:
            tuple: RGB (255, 255, 255) случайный цвет
        """
        channel = lambda: randrange(30, 220)
        return channel(), channel(), channel()
    

    @property
    def ant(self):
        return self.__ant


    @ant.setter
    def ant(self, ant):
        self.__ant = ant


    def run(self):
        while True:
            self.ant.run()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]

            pg.display.flip()
            self.clock.tick()

            self.text = self.font.render(f'{self.ant.count}', True, (0, 100, 0))
            self.place = self.text.get_rect()

            self.surface_count.blit(self.text, self.place)
            self.screen.blit(self.surface_count, (50, 50))
            self.surface_count.fill((255, 255, 255))


class Ant:
    """Класс Муравья
    """

    def __init__(self, app: MainApp , pos: tuple | list, color: tuple) -> None:
        """Метод инициалзации

        Args:
            app (App): главное приложение
            pos (tuple | list): начальная точка появления муравья, в середине экрана по умолчанию
            color (tuple): цвет в формате RGB (255, 255, 255)
        """
        self.count: int = 1
        self.app: MainApp = app
        self.color: tuple = color
        self.x, self.y = pos
        
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])


    def run(self) -> None:
        """логика клеточного автомата (муравья), его движения
        """
        value = self.app.grid[self.y][self.x]           # получаем значение из матрицы главного приложения (координаты)
        self.app.grid[self.y][self.x] = not value       # если 0 даст True

        SIZE = self.app.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, SIZE - 1, SIZE - 1
        if value:                                                               
            pg.draw.rect(self.app.screen, pg.Color('white'), rect)
            self.count  -= 1
        else:
            pg.draw.rect(self.app.screen, self.color, rect)
            self.count  += 1

        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[2]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS



if __name__ == '__main__':
    app = MainApp(WIDTH=1024, HEIGHT=1024, CELL_SIZE=4)
    app.run()
