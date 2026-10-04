from . import config as cfg
from .window import Window


def main():
    window = Window(cfg.WIDTH, cfg.HEIGHT)
    window.setup()
    window.run()

if __name__ == "__main__":
    main()
