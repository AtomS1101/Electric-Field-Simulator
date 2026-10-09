from . import config as cfg

Y_LIMIT = (cfg.HEIGHT / cfg.WIDTH) * (cfg.X_MAX - cfg.X_MIN)
Y_MIN = -Y_LIMIT / 2
Y_MAX =  Y_LIMIT / 2

class Viewport:
	def __init__(self):
		self._offsetX = 0
		self._offsetY = 0

	def crdToWin(self, x: float, y: float) -> tuple[float, float]:
		windowCrdX = cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * x + cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * abs(cfg.X_MIN) - self._offsetX
		windowCrdY = -(cfg.HEIGHT / Y_LIMIT) * y + (cfg.HEIGHT / 2) + self._offsetY
		return (windowCrdX, windowCrdY)

	def winToCrd(self, x: int, y: int) -> tuple[int, int]:
		crdX = (cfg.X_MAX - cfg.X_MIN) / cfg.WIDTH * (x + self._offsetX) + cfg.X_MIN
		crdY = -(Y_LIMIT / cfg.HEIGHT) * (y - self._offsetY) + (Y_LIMIT / 2)
		return (int(crdX), int(crdY))

	def stillInScreen(self, x: float, y: float) -> bool:
		x, y = self.crdToWin(x, y)
		return x >= 0 and y >= 0 and x <= cfg.WIDTH and y <= cfg.HEIGHT

	def scroll(self, x: int, y: int) -> None:
		self._offsetX += x * cfg.SCROLL_SPEED
		self._offsetY += y * cfg.SCROLL_SPEED
