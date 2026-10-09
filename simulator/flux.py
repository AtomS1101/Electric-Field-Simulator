import math

import pygame

from . import config as cfg
from .charge import Charge
from .viewport import Viewport


class Flux:
	def __init__(self, screen: pygame.Surface, viewport: Viewport):
		self._screen: pygame.Surface = screen
		self._viewport: Viewport = viewport

	def _getElectricField(self, pos, charges: list[Charge]) -> tuple[float, float]:
		Ex = Ey = 0
		for charge in charges:
			dx, dy = pos[0] - charge.pos[0], pos[1] - charge.pos[1]
			if dx == 0 and dy == 0:	return 0, 0
			R3 = (dx**2 + dy**2) ** 1.5
			Ex += cfg.K * charge.q * dx / R3
			Ey += cfg.K * charge.q * dy / R3
		magnitude = (Ex ** 2 + Ey ** 2) ** 0.5
		angle = math.atan2(Ey, Ex)
		return magnitude, angle

	def _hitCharge(self, x: float, y: float, charges: list[Charge], selfPos: tuple[float, float]) -> bool:
		for charge in charges:
			if charge.pos == selfPos: continue
			if (x - charge.pos[0])**2 + (y - charge.pos[1])**2 <= cfg.CHARGE_SIZE / 2:
				return True
		return False

	def draw(self, charges: list[Charge]) -> None:
		for xBlock in range(0, cfg.WIDTH, cfg.SPACE):
			for yBlock in range(0, cfg.HEIGHT, cfg.SPACE):
				x, y = self._viewport.winToCrd(xBlock, yBlock)
				path = []
				for _ in range(cfg.MAX_BL_STEPS):
					_, angle = self._getElectricField((x, y), charges)
					dx = cfg.STEP * math.cos(angle)
					dy = cfg.STEP * math.sin(angle)
					# pygame.draw.line(self._screen, cfg.FLUX_COLOR, crdToWin(x, y), crdToWin(x+dx, y+dy), width=cfg.FLUX_WIDTH)
					path.append(self._viewport.crdToWin(x, y))
					x, y = x + dx, y + dy
					if self._hitCharge(x, y, charges, (x, y)): break
				if (len(path) >= 2): pygame.draw.lines(self._screen, cfg.FLUX_COLOR, False, path, width=cfg.FLUX_WIDTH)

		for charge in charges:
			if charge.q <= 0: continue
			density = abs(charge.q) * cfg.DENSITY
			for n in range(density):
				angle = 2 * math.pi / density * n
				x, y = charge.pos
				path = []
				for _ in range(cfg.MAX_CH_STEPS):
					dx = cfg.STEP * math.cos(angle) * (-1 if charge.q < 0 else 1)
					dy = cfg.STEP * math.sin(angle) * (-1 if charge.q < 0 else 1)
					# pygame.draw.line(self._screen, cfg.FLUX_COLOR, crdToWin(x, y), crdToWin(x+dx, y+dy), width=cfg.FLUX_WIDTH)
					x, y = x + dx, y + dy
					path.append(self._viewport.crdToWin(x, y))
					_, angle = self._getElectricField((x, y), charges)
					if self._hitCharge(x, y, charges, charge.pos): break
				if (len(path) >= 2): pygame.draw.lines(self._screen, cfg.FLUX_COLOR, False, path, width=cfg.FLUX_WIDTH)
