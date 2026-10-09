import pygame

from . import config as cfg
from .charge import Charge
from .flux import Flux
from .gui import Gui
from .mouse import Mouse
from .viewport import Viewport


class Window:
	def __init__(self, x: int, y: int):
		self._x: int = x
		self._y: int = y
		self._screen: pygame.Surface
		self._clock: pygame.time.Clock
		self._charges: list[Charge] = []
		self._mouse: Mouse = Mouse()
		self._viewport: Viewport = Viewport()
		self._lastChargePos: int = 0

	def setup(self) -> None:
		pygame.init()
		self._screen = pygame.display.set_mode((self._x, self._y))
		self._clock = pygame.time.Clock()
		pygame.display.set_caption("Electric Field Simulator")

	def _drawAxis(self) -> None:
		pygame.draw.line(self._screen, cfg.AXIS_COLOR, self._viewport.crdToWin(-500, 0), self._viewport.crdToWin(500, 0), width=cfg.AXIS_WIDTH) #　X Axis
		pygame.draw.line(self._screen, cfg.AXIS_COLOR, self._viewport.crdToWin(0, -500), self._viewport.crdToWin(0, 500), width=cfg.AXIS_WIDTH) #　Y Axis

	def _addCharge(self) -> None:
		self._charges.append(Charge(self._screen, self._viewport, self._lastChargePos, -self._lastChargePos))
		self._lastChargePos += 10

	def run(self) -> None:
		gui = Gui(self._screen)
		flux = Flux(self._screen, self._viewport)
		self._addCharge()
		while True:
			self._screen.fill(cfg.BACKGROUND)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				for charge in self._charges:
					charge.move(event)
					if gui.listen(event):
						self._addCharge()
					self._viewport.scroll(*self._mouse.getScroll(event)) # Update every fram
			self._drawAxis()
			flux.draw(self._charges)
			for charge in self._charges:
				charge.draw()
			gui.showAddBtn()
			pygame.display.update()
			self._clock.tick(cfg.FPS)
