import pygame

from . import config as cfg
from .mouse import Mouse, MouseState


class Gui:
	def __init__(self, screen: pygame.Surface):
		self._screen: pygame.Surface = screen
		self._clicked: bool = False
		self._rect: pygame.Rect = pygame.Rect(
			cfg.WIDTH - cfg.ADD_BTN_DIAMETER - cfg.ADD_BTN_MARGIN, cfg.HEIGHT - cfg.ADD_BTN_DIAMETER - cfg.ADD_BTN_MARGIN,
			cfg.ADD_BTN_DIAMETER, cfg.ADD_BTN_DIAMETER
		)
		self._mouse: Mouse = Mouse()

	def listen(self, event: pygame.event.Event) -> bool:
		status = self._mouse.getState(self._rect.center, cfg.ADD_BTN_DIAMETER, event)
		if status == MouseState.CLICKED:
			self._clicked = True
		elif status == MouseState.RELEASED and self._clicked:
			self._clicked = False
			return True
		return False


	def showAddBtn(self):
		plusMargin = 7
		pygame.draw.circle(self._screen, (30, 30, 90), self._rect.center, cfg.ADD_BTN_DIAMETER / 2)
		pygame.draw.line(self._screen, (100, 100, 100), (self._rect.left+plusMargin, self._rect.top+cfg.ADD_BTN_DIAMETER/2), (self._rect.left+cfg.ADD_BTN_DIAMETER-plusMargin, self._rect.top+cfg.ADD_BTN_DIAMETER/2), 3)
		pygame.draw.line(self._screen, (100, 100, 100), (self._rect.left+cfg.ADD_BTN_DIAMETER/2, self._rect.top+plusMargin), (self._rect.left+cfg.ADD_BTN_DIAMETER/2, self._rect.top+cfg.ADD_BTN_DIAMETER-plusMargin), 3)
