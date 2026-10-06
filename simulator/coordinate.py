from . import config as cfg

Y_LIMIT = (cfg.HEIGHT / cfg.WIDTH) * (cfg.X_MAX - cfg.X_MIN)
Y_MIN = -Y_LIMIT / 2
Y_MAX =  Y_LIMIT / 2

def crdToWin(x: float, y: float) -> tuple[int, int]:
	windowCrdX = cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * x + cfg.WIDTH / (cfg.X_MAX - cfg.X_MIN) * abs(cfg.X_MIN)
	windowCrdY = (cfg.HEIGHT / Y_LIMIT) * y + (cfg.HEIGHT / 2)
	return (int(windowCrdX), int(windowCrdY))

def winToCrd(x: int, y: int) -> tuple[int, int]:
	crdX = (cfg.X_MAX - cfg.X_MIN) / cfg.WIDTH * x + cfg.X_MIN
	crdY = (Y_LIMIT / cfg.HEIGHT) * y - (Y_LIMIT / 2)
	return (int(crdX), int(crdY))

def stillInScreen(x: float, y: float) -> bool:
	return x >= cfg.X_MIN and y >= Y_MIN and x <= cfg.X_MAX and y <= Y_MAX
