def game(player_money):
    # 0. Игрок делает ставку
    player_money -= rate_value
    # 1. В начале игры перемешиваем колоду
    deck.shuffle()
    # 2. Игроку выдаем две карты
    player_cards = deck.draw(2)
    # 3. Дилер берет одну карту
    dealer_cards = deck.draw(1)
    # 4. Отображаем в консоли карты игрока и дилера
    print(f'Player cards: {player_cards}')
    print(f'Dealer cards: {dealer_cards}')
    # 5. Проверяем нет ли у игрока блэкджека (21 очко)
    if sum_points(player_cards) == 21:
        # Выплачиваем выигрышь 3 и 2
        player_money += rate_value * 1.5
        print(f"Black Jack!!! Игрок победил {player_money=}")
        in_circle = False
        return

    if sum_points(player_cards) > 21:
        print("Casino wins, you loose")
        in_circle = False
        return


    # Если нет блэкджека, то
    while True:  # Игрок добирает карты пока не скажет "достаточно" или не сделает перебор (>21)
        player_choice = input("еще(1)/достаточно(0): ")
        if player_choice == "1":
            # Раздаем еще одну карту
            player_cards += deck.draw(1)
            print(f'Player cards  now: {player_cards}')
            # Если перебор (>21), заканчиваем добор
        if sum_points(player_cards) > 21:
            print(f"Перебор: {sum_points(player_cards)} очков \n Casino wins {player_money=}")
            in_circle = False
            return

        if sum_points(player_cards) == 21:
            player_money += rate_value * 1.5
            print(f"Black Jack!!! Игрок победил \n {player_money=}")
            in_circle = False
            return

        if player_choice == "0":
            # Заканчиваем добирать карты
            break

    # Если у игрока не 21(блэкджек) и нет перебора, то
    if sum_points(player_cards) < 21:
        print("Диллер добирает карты")
        while True:  # дилер начинает набирать карты.
            if sum_points(dealer_cards) < 17:
                dealer_cards += deck.draw(1)
                print("Dealer cards now:", dealer_cards)
            if sum_points(dealer_cards) >= 17:
                break

    # Выясняем кто набрал больше очков. Выплачиваем/забираем ставку
    if sum_points(player_cards) > sum_points(dealer_cards):
        player_money += rate_value * 1.5
        print(f"Black Jack!!! Игрок победил {player_money=}")
        in_circle = False
        return

    if sum_points(player_cards) == sum_points(dealer_cards):
        player_money += rate_value
        print(f"There is a draw {player_money=}")
        in_circle = False

    else:
        print("You've lost your money, Casino wins")
        out_of_circle = False
        return