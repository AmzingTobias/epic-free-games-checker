from product_decode import EpicFreeGames

if __name__ == '__main__':
    manager = EpicFreeGames()
    manager.make_request()
    for game in manager.free_games:
        game.display()
