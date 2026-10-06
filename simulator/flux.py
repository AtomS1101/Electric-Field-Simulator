import math

import pygame

from . import config as cfg
from .charge import Charge
from .coordinate import crdToWin, stillInScreen


class Flux:
	def __init__(self, screen: pygame.Surface):
		self._screen: pygame.Surface = screen

	def _getElectricField(self, pos, charges: list[Charge]) -> float:
		Ex = Ey = 0
		for charge in charges:
			dx, dy = pos[0] - charge.pos[0], pos[1] - charge.pos[1]
			if dx == 0 and dy == 0:
				return 0
			R3 = (dx**2 + dy**2) ** 1.5
			Ex += cfg.K * charge.q * dx / R3
			Ey += cfg.K * charge.q * dy / R3
		angle = math.atan2(Ey, Ex)
		return angle

	def _hitCharge(self, x: float, y: float, charges: list[Charge]) -> bool:
		for charge in charges:
			if charge.q > 0: continue
			if (x - charge.pos[0])**2 + (y - charge.pos[1])**2 <= cfg.CHARGE_SIZE / 2:
				return True
		return False

	def draw(self, charges: list[Charge]) -> None:
		steps = 2
		for charge in charges:
			if charge.q <= 0: continue
			density = abs(charge.q) * cfg.DENSITY
			for n in range(density):
				angle = 2 * math.pi / density * n
				x, y = charge.pos
				show = True
				while show:
					dx = steps * math.cos(angle)
					dy = steps * math.sin(angle)
					end = crdToWin(x + dx, y + dy)
					pygame.draw.line(self._screen, cfg.FLUX_COLOR, crdToWin(x, y), end, width=cfg.FLUX_WIDTH)
					x, y = x + dx, y + dy
					angle = self._getElectricField((x, y), charges)
					show = stillInScreen(x, y) and not self._hitCharge(x, y, charges)
