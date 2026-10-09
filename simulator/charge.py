import pygame

from . import config as cfg
from .mouse import Mouse, MouseState
from .viewport import Viewport


class Charge:
	def __init__(self, screen: pygame.Surface, viewport: Viewport, x: int, y: int, q: int):
		self._screen: pygame.Surface = screen
		self._viewport: Viewport = viewport
		self._q: int = q
		self._x: int = x
		self._y: int = y
		self._offsetX: int = 0
		self._offsetY: int = 0
		self._mouse: Mouse = Mouse()
		start = self._viewport.crdToWin(self._x, self._y)
		self._rect = pygame.Rect(
			start[0] - cfg.CHARGE_SIZE / 2,	start[1] - cfg.CHARGE_SIZE / 2,
			cfg.CHARGE_SIZE, cfg.CHARGE_SIZE,
		)

	@property
	def pos(self) -> tuple[int, int]:
		return self._x, self._y

	@property
	def q(self) -> int:
		return self._q

	def move(self, event: pygame.event.Event) -> None:
		status = self._mouse.getState(self._rect.center, cfg.CHARGE_SIZE, event)
		if status == MouseState.CLICKED:
			eventPos = self._viewport.winToCrd(*event.pos)
			self._offsetX = self._x - eventPos[0]
			self._offsetY = self._y - eventPos[1]
		elif status == MouseState.DRAGGING:
			eventPos = self._viewport.winToCrd(*event.pos)
			self._x = eventPos[0] + self._offsetX
			self._y = eventPos[1] + self._offsetY
			if abs(self._x) < cfg.SNAP:	self._x = 0
			if abs(self._y) < cfg.SNAP:	self._y = 0

	def draw(self) -> None:
		self._rect.x, self._rect.y = self._viewport.crdToWin(self._x, self._y)
		self._rect.x -= int(cfg.CHARGE_SIZE / 2)
		self._rect.y -= int(cfg.CHARGE_SIZE / 2)
		isDragging = self._mouse.isHolding()
		positiveColor = cfg.POSITIVE_COLOR_CLICKED if isDragging else cfg.POSITIVE_COLOR
		negativeColor = cfg.NEGATIVE_COLOR_CLICKED if isDragging else cfg.NEGATIVE_COLOR
		color = positiveColor if self._q > 0 else negativeColor if self._q < 0 else (0, 0, 0)
		pygame.draw.circle(self._screen, color, self._rect.center, cfg.CHARGE_SIZE / 2) # Draw charge
		textBackground = self._viewport.crdToWin(self._x + cfg.TEXT_OFFSET[0], self._y + cfg.TEXT_OFFSET[1])
		textRect = pygame.Rect(textBackground[0] - 1, textBackground[1] - 1, 40, 23)
		pygame.draw.rect(self._screen, cfg.BACKGROUND, textRect)
		font = pygame.font.SysFont("Times New Roman", 15)
		text = font.render(f"{self._q} [C]", False, cfg.FONT_COLOR)
		self._screen.blit(text, textBackground)
