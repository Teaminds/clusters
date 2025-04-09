from levels.testo_3 import get_level

import arcade
from ui import game_view


def main():
    window = arcade.Window(1200, 720, "Clusters")
    view = game_view.GameView(level=get_level())
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    # cProfile.run("main()", sort="cumtime")
    main()
