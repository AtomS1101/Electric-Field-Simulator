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
		for xBlock in range(0, cfg.WIDTH, cfg.GRID):
			for yBlock in range(0, cfg.HEIGHT, cfg.GRID):
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



# import math
#
# import pygame
#
# from . import config as cfg
# from .charge import Charge
# from .viewport import Viewport
#
# space = 10
#
#
# class Flux:
# 	def __init__(self, screen: pygame.Surface, viewport: Viewport):
# 		self._screen: pygame.Surface = screen
# 		self._viewport: Viewport = viewport
#
# 	# unit tangent of the field (sign=+1: along E, sign=-1: against E)
# 	def _direction(self, x, y, charges, sign):
# 		Ex = Ey = 0.0
# 		for c in charges:
# 			dx, dy = x - c.pos[0], y - c.pos[1]
# 			r2 = dx * dx + dy * dy
# 			if r2 < 1e-12:
# 				return None  # sitting exactly on a charge
# 			r3 = r2 ** 1.5
# 			Ex += cfg.K * c.q * dx / r3
# 			Ey += cfg.K * c.q * dy / r3
# 		m = math.hypot(Ex, Ey)
# 		if m == 0:
# 			return None  # E = 0 (saddle point)
# 		return sign * Ex / m, sign * Ey / m
#
# 	# any charge, positive OR negative, ends a line
# 	def _hitCharge(self, x, y, charges) -> bool:
# 		r = cfg.CHARGE_SIZE / 2
# 		for c in charges:
# 			dx, dy = x - c.pos[0], y - c.pos[1]
# 			if dx * dx + dy * dy <= r * r:
# 				return True
# 		return False
#
# 	# coarse grid cell (in window pixels) used for spacing control
# 	def _cell(self, x, y):
# 		wx, wy = self._viewport.crdToWin(x, y)
# 		return int(wx // space), int(wy // space)
#
# 	def _trace(self, x, y, charges, sign, grid, own, avoid, h=2.0, maxSteps=2000):
# 		path = [(x, y)]
# 		for _ in range(maxSteps):
# 			d1 = self._direction(x, y, charges, sign)
# 			if d1 is None: break
# 			d2 = self._direction(x + d1[0] * h / 2, y + d1[1] * h / 2, charges, sign)
# 			if d2 is None: break
# 			x += d2[0] * h
# 			y += d2[1] * h
# 			path.append((x, y))
# 			if not self._viewport.stillInScreen(x, y) or self._hitCharge(x, y, charges):
# 				break
# 			cell = self._cell(x, y)
# 			if avoid and cell in grid and cell not in own:
# 				break  # ran into another line's territory
# 			own.add(cell)
# 		return path
#
# 	def _drawPath(self, path):
# 		if len(path) >= 2:
# 			pts = [self._viewport.crdToWin(x, y) for x, y in path]
# 			pygame.draw.lines(self._screen, cfg.FLUX_COLOR, False, pts, width=cfg.FLUX_WIDTH)
#
# 	def draw(self, charges: list[Charge]) -> None:
# 		grid: set = set()
# 		r0 = cfg.CHARGE_SIZE  # start slightly away from the center (avoids 1/0)
#
# 		# 1) lines born at charges: + goes forward, - goes BACKWARD (so lines from infinity reach it)
# 		for c in charges:
# 			if c.q == 0: continue
# 			sign = 1 if c.q > 0 else -1
# 			count = int(abs(c.q) * cfg.DENSITY)
# 			for n in range(count):
# 				a = 2 * math.pi * n / count
# 				x = c.pos[0] + r0 * math.cos(a)
# 				y = c.pos[1] + r0 * math.sin(a)
# 				own = {self._cell(x, y)}
# 				path = self._trace(x, y, charges, sign, grid, own, avoid=False)
# 				grid |= own
# 				self._drawPath(path)
#
# 		# 2) fill the empty screen, streamplot style: seed in empty cells, trace both ways
# 		s = space
# 		for wx in range(s // 2, cfg.WIDTH, s):
# 			for wy in range(s // 2, cfg.WIDTH, s):
# 				if (wx // s, wy // s) in grid: continue
# 				x, y = self._viewport.winToCrd(wx, wy)
# 				own = {self._cell(x, y)}
# 				fwd = self._trace(x, y, charges, +1, grid, own, avoid=True)
# 				bwd = self._trace(x, y, charges, -1, grid, own, avoid=True)
# 				grid |= own
# 				self._drawPath(bwd[::-1] + fwd[1:])
