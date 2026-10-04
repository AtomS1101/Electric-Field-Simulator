import pygame

from . import config as cfg


class Flux:
	def __init__(self, screen: pygame.Surface):
		self._screen : pygame.Surface = screen

	def draw(self, start: tuple[int, int], end: tuple[int, int]) -> None:
		pygame.draw.line(self._screen, cfg.FLUX_COLOR, start, end, width=cfg.FLUX_WIDTH)
		# pygame.draw.lines(screen, (255, 0, 0), False, points_v, 5)
