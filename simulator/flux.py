import math

import pygame

from . import config as cfg
from .charge import Charge
from .coordinate import crdToWin, stillInScreen


class Flux:
	def __init__(self, screen: pygame.Surface):
		self._screen: pygame.Surface = screen

	def _getElectricField(self, pos, charges: list[Charge]) -> tuple[float, float]:
		Ex = Ey = 0
		for charge in charges:
			dx, dy = pos[0] - charge.pos[0], pos[1] - charge.pos[1]
			if dx == 0 and dy == 0:
				return 0, 0
			R3 = (dx**2 + dy**2) ** 1.5
			Ex += cfg.K * charge.q * dx / R3
			Ey += cfg.K * charge.q * dy / R3
		magnitude = (Ex ** 2 + Ey ** 2) ** 0.5
		angle = math.atan2(Ey, Ex)
		return magnitude, angle

	def _hitCharge(self, x: float, y: float, charges: list[Charge], selfPos: tuple[int, int]) -> bool:
		for charge in charges:
			if charge.pos == selfPos: continue
			if (x - charge.pos[0])**2 + (y - charge.pos[1])**2 <= cfg.CHARGE_SIZE / 2:
				return True
		return False

	def draw(self, charges: list[Charge]) -> None:
		steps = 2
		chargeSum = 0
		for charge in charges:
			chargeSum += charge.q
			if charge.q == 0: continue
			density = abs(charge.q) * cfg.DENSITY
			for n in range(density):
				angle = 2 * math.pi / density * n
				x, y = charge.pos
				path = []
				for _ in range(cfg.MAX_STEPS):
					dx = steps * math.cos(angle) * (-1 if charge.q < 0 else 1)
					dy = steps * math.sin(angle) * (-1 if charge.q < 0 else 1)
					# pygame.draw.line(self._screen, math.log10(mag), crdToWin(x, y), crdToWin(x+dx, y+dy), width=cfg.FLUX_WIDTH)
					x, y = x + dx, y + dy
					path.append(crdToWin(x, y))
					_, angle = self._getElectricField((x, y), charges)
					if not stillInScreen(x, y) or self._hitCharge(x, y, charges, charge.pos): break
				if (len(path) >= 2): pygame.draw.lines(self._screen, cfg.FLUX_COLOR, False, path, width=cfg.FLUX_WIDTH)
