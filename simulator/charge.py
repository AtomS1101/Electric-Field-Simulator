import pygame

from . import config as cfg
from .mouse import Mouse, MouseState


class Charge:
	def __init__(self, screen: pygame.Surface, x: int, y: int):
		self._screen: pygame.Surface = screen
		self._x: int = x
		self._y: int = y
		self._q: int = -1
		self._offsetX: int = 0
		self._offsetY: int = 0
		self._mouse: Mouse = Mouse()
		self._rect = pygame.Rect(
			self._x - cfg.CHARGE_SIZE / 2, self._y - cfg.CHARGE_SIZE / 2,
			cfg.CHARGE_SIZE, cfg.CHARGE_SIZE
		)

	@property
	def pos(self) -> tuple[int, int]:
		return self._x, self._y

	def move(self, event: pygame.event.Event) -> None:
		status = self._mouse.getState(self._rect.center, cfg.CHARGE_SIZE, event)
		if status == MouseState.CLICKED:
			self._offsetX = self._rect.x - event.pos[0]
			self._offsetY = self._rect.y - event.pos[1]
		elif status == MouseState.DRAGGING:
			self._rect.x = event.pos[0] + self._offsetX
			self._rect.y = event.pos[1] + self._offsetY
			self._x, self._y = self._rect.center

	def draw(self) -> None:
		isDragging = self._mouse.isHolding()
		positiveColor = cfg.POSITIVE_COLOR_CLICKED if isDragging else cfg.POSITIVE_COLOR
		negativeColor = cfg.NEGATIVE_COLOR_CLICKED if isDragging else cfg.NEGATIVE_COLOR
		color = positiveColor if self._q > 0 else negativeColor
		pygame.draw.circle(self._screen, color, self._rect.center, cfg.CHARGE_SIZE / 2)
