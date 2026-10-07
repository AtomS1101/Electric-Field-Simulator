import pygame

from . import config as cfg
from .charge import Charge
from .coordinate import crdToWin, setOffset
from .flux import Flux
from .mouse import Mouse


class Window:
	def __init__(self, x: int, y: int):
		self._x: int = x
		self._y: int = y
		self._screen: pygame.Surface
		self._clock: pygame.time.Clock
		self._charges: list[Charge] = []
		self._mouse: Mouse = Mouse()

	def setup(self) -> None:
		pygame.init()
		self._screen = pygame.display.set_mode((self._x, self._y))
		self._clock = pygame.time.Clock()
		pygame.display.set_caption("Electric Field Simulator")

	def run(self) -> None:
		flux = Flux(self._screen)
		self._charges.append(Charge(self._screen,  50,  0, 1))
		self._charges.append(Charge(self._screen, -50,  0, -1))
		self._charges.append(Charge(self._screen,   0, 30, -3))
		# self._charges.append(Charge(self._screen,  -50, 30,-4))
		# # self._charges.append(Charge(self._screen,   50, 40, 3))
		while True:
			self._screen.fill(cfg.BACKGROUND)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				for charge in self._charges:
					charge.move(event)
					setOffset(*self._mouse.getScroll(event)) # Update every frame
			pygame.draw.line(self._screen, cfg.AXIS_COLOR, crdToWin(-500, 0), crdToWin(500, 0), width=cfg.AXIS_WIDTH) #　X Axis
			pygame.draw.line(self._screen, cfg.AXIS_COLOR, crdToWin(0, -500), crdToWin(0, 500), width=cfg.AXIS_WIDTH) #　Y Axis
			flux.draw(self._charges)
			for charge in self._charges:
				charge.draw()
			pygame.display.update()
			self._clock.tick(cfg.FPS)
