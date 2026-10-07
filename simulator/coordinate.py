from . import config as cfg

Y_LIMIT = (cfg.HEIGHT / cfg.WIDTH) * (cfg.X_MAX - cfg.X_MIN)
Y_MIN = -Y_LIMIT / 2
Y_MAX =  Y_LIMIT / 2
offsetX = 0
offsetY = 0

def crdToWin(x: float, y: float) -> tuple[int, int]:
	windowCrdX = cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * x + cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * abs(cfg.X_MIN) - offsetX
	windowCrdY = (cfg.HEIGHT / Y_LIMIT) * y + (cfg.HEIGHT / 2) + offsetY
	return (int(windowCrdX), int(windowCrdY))

def winToCrd(x: int, y: int) -> tuple[int, int]:
	crdX = (cfg.X_MAX - cfg.X_MIN) / cfg.WIDTH * (x - offsetX) + cfg.X_MIN
	crdY = (Y_LIMIT / cfg.HEIGHT) * (y + offsetY) - (Y_LIMIT / 2)
	return (int(crdX), int(crdY))

def stillInScreen(x: float, y: float) -> bool:
	x, y = crdToWin(x, y)
	return x >= 0 and y >= 0 and x <= cfg.WIDTH and y <= cfg.HEIGHT

def setOffset(x: int, y: int) -> None:
	global offsetX, offsetY
	offsetX += x
	offsetY += y
