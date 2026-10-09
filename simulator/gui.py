import pygame

from . import config as cfg
from .mouse import Mouse, MouseState


class Gui:
	def __init__(self, screen: pygame.Surface):
		self._screen: pygame.Surface = screen
		self._clicked: bool = False
		self._rect: pygame.Rect = pygame.Rect(
			cfg.WIDTH - cfg.BUTTON_DIAMETER - cfg.BUTTON_MARGIN, cfg.HEIGHT - cfg.BUTTON_DIAMETER - cfg.BUTTON_MARGIN,
			cfg.BUTTON_DIAMETER, cfg.BUTTON_DIAMETER
		)
		self._mouse: Mouse = Mouse()
		self._isHovering: bool = False

	def listen(self, event: pygame.event.Event) -> bool:
		status = self._mouse.getState(self._rect.center, cfg.BUTTON_DIAMETER, event)
		if status == MouseState.CLICKED:
			self._clicked = True
		elif status == MouseState.RELEASED and self._clicked:
			self._clicked = False
			return True
		elif status == MouseState.HOVER:
			self._isHovering = True
		else:
			self._isHovering = False
		return False


	def showAddBtn(self):
		plusMargin = 7
		shadowPos = 4 if self._isHovering else 2
		color = (10, 10, 70) if self._clicked else (30, 30, 90)
		pygame.draw.circle(self._screen, (20, 20, 80), (self._rect.center[0]+shadowPos, self._rect.center[1]+2), cfg.BUTTON_DIAMETER / 2)
		pygame.draw.circle(self._screen, color, self._rect.center, cfg.BUTTON_DIAMETER / 2)
		pygame.draw.line(self._screen, (90, 90, 100), (self._rect.left+plusMargin, self._rect.top+cfg.BUTTON_DIAMETER/2), (self._rect.left+cfg.BUTTON_DIAMETER-plusMargin, self._rect.top+cfg.BUTTON_DIAMETER/2), 3)
		pygame.draw.line(self._screen, (90, 90, 100), (self._rect.left+cfg.BUTTON_DIAMETER/2, self._rect.top+plusMargin), (self._rect.left+cfg.BUTTON_DIAMETER/2, self._rect.top+cfg.BUTTON_DIAMETER-plusMargin), 3)
