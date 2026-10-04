import pygame

from . import config as cfg
from .charge import Charge
from .flux import Flux


class Window:
	def __init__(self, x: int, y: int):
		self._x: int = x
		self._y: int = y
		self._screen: pygame.Surface
		self._clock: pygame.time.Clock
		self._charges: list[Charge] = []

	def setup(self) -> None:
		pygame.init()
		self._screen = pygame.display.set_mode((self._x, self._y))
		self._clock = pygame.time.Clock()
		pygame.display.set_caption("Electric Field Simulator")

	def run(self) -> None:
		flux = Flux(self._screen)
		self._charges.append(Charge(self._screen, 400, 350))
		self._charges.append(Charge(self._screen, 600, 350))
		while True:
			self._screen.fill((45, 45, 49))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				for charge in self._charges:
					charge.move(event)
			for charge in self._charges:
				charge.draw()
			flux.draw(self._charges[0].pos, self._charges[1].pos)
			pygame.display.update()
			self._clock.tick(cfg.FPS)
