import pygame

from . import config as cfg
from .coordinate import crdToWin, winToCrd
from .mouse import Mouse, MouseState


class Charge:
	def __init__(self, screen: pygame.Surface, x: int, y: int, q: int):
		self._screen: pygame.Surface = screen
		self._q: int = q
		self._x: int = x
		self._y: int = y
		self._offsetX: int = 0
		self._offsetY: int = 0
		self._mouse: Mouse = Mouse()
		start = crdToWin(self._x, self._y)
		self._rect = pygame.Rect(
			start[0] - cfg.CHARGE_SIZE / 2, start[1] - cfg.CHARGE_SIZE / 2,
			cfg.CHARGE_SIZE, cfg.CHARGE_SIZE
		)

	@property
	def pos(self) -> tuple[int, int]:
		self._x, self._y = winToCrd(*self._rect.center)
		return self._x, self._y

	@property
	def q(self) -> int:
		return self._q

	def move(self, event: pygame.event.Event) -> None:
		status = self._mouse.getState(self._rect.center, cfg.CHARGE_SIZE, event)
		if status == MouseState.CLICKED:
			self._offsetX = self._rect.x - event.pos[0]
			self._offsetY = self._rect.y - event.pos[1]
		elif status == MouseState.DRAGGING:
			self._rect.x = event.pos[0] + self._offsetX
			self._rect.y = event.pos[1] + self._offsetY
			if abs(self.pos[0]) < cfg.SNAP:
				self._rect.x = int(cfg.WIDTH / 2 - cfg.CHARGE_SIZE / 2)
			if abs(self.pos[1]) < cfg.SNAP:
				self._rect.y = int(cfg.HEIGHT / 2 - cfg.CHARGE_SIZE / 2)

	def draw(self) -> None:
		isDragging = self._mouse.isHolding()
		positiveColor = cfg.POSITIVE_COLOR_CLICKED if isDragging else cfg.POSITIVE_COLOR
		negativeColor = cfg.NEGATIVE_COLOR_CLICKED if isDragging else cfg.NEGATIVE_COLOR
		color = positiveColor if self._q > 0 else negativeColor
		pygame.draw.circle(self._screen, color, self._rect.center, cfg.CHARGE_SIZE / 2)
