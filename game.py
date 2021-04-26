import random
import curses
import logging
from curses import textpad


# Ok! I know... I must clean this house. It's a mess.
def main(screen):
    logger = logging.getLogger('snake')

    file_log_handler = logging.FileHandler('log')
    logger.addHandler(file_log_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_log_handler.setFormatter(formatter)
    logger.setLevel('DEBUG')

    logger.info('Game Started')

    height, width = screen.getmaxyx()
    start_screen(height, width)

    curses.curs_set(0)

    box = [[3, 3], [height - 3, width - 3]]
    textpad.rectangle(screen, box[0][0], box[0][1], box[1][0], box[1][1])

    screen.nodelay(1)
    screen.timeout(100)

    pos_x = width / 4
    pos_y = height / 2

    # Snake start position
    snake = [
        [pos_y, pos_x],
        [pos_y, pos_x - 1],
        [pos_y, pos_x - 2]
    ]

    food = [height / 2, width / 3]

    screen.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    screen.scrollok(0)
    key = curses.KEY_RIGHT

    score = 0

    while True:
        next_key = screen.getch()
        key = key if next_key == -1 else next_key

        if collision(snake, box):
            msg = "GAME OVER!"

            screen.addstr(height // 2, width // 2 - len(msg) // 2, msg)
            screen.nodelay(0)
            screen.getch()

            logger.info('Game Over!')

            break

        new_head = [int(snake[0][0]), int(snake[0][1])]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # Score
        scoreboard = "Score: {} Food: [{}, {}] Snake {}".format(score, int(food[0]), int(food[1]), snake[0])
        screen.addstr(1, width // 2 - len(scoreboard) // 2, scoreboard)

        # If snake find the food
        if snake[0] == food:

            logger.info('Food ate @ [{}, {}]'.format(food[0], food[1]))

            # Create a new food
            food = new_food(snake, box)

            screen.addch(int(food[0]), int(food[1]), curses.ACS_PI)

            # increase snake length
            snake.append([pos_y, pos_x - len(snake)])

            # Update score
            score += 1
            scoreboard = "Score: {} Food: [{}, {}] Snake {}".format(score, int(food[0]), int(food[1])
                                                                    , snake[0])
            screen.addstr(1, width // 2 - len(scoreboard) // 2, scoreboard)

            # Increase speed
            screen.timeout(100 - (len(snake) // 3) % 90)

        else:
            tail = snake.pop()
            try:
                screen.addch(int(tail[0]), int(tail[1]), ' ')

            except:
                logger.error(screen)
                pass

        try:
            screen.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

        except:
            logger.error("2")
            logger.error(curses.setupterm())
            pass


def collision(object, area):
    event = False

    if (object[0][0] in [area[0][0], area[1][0]] or
            object[0][1] in [area[0][1], area[1][1]] or
            object[0] in object[1:]):
        event = True

    return event


def new_food(object, area):
    position = None

    while position is None:
        new_position = set_new_position(area)

        position = new_position if new_position not in object else None

    return position


def set_new_position(area):
    return [
        random.randint(area[0][0] + 1, area[1][0] - 1),
        random.randint(area[0][1] + 1, area[1][1] - 1)
    ]


def start_screen(y, x):
    screen = curses.initscr()
    curses.curs_set(0)
    title = "SNAKE"
    version = "Ver: 0.1.1"
    instruction = "[ Press Any Button to Start ]"

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

    screen.addstr(y // 2, x // 2 - len(title) // 2, title, curses.A_BOLD)
    screen.addstr((y // 2 + 1), x // 2 - len(version) // 2, version)
    screen.addstr((y // 2 + 2), x // 2 - len("") // 2, "")
    screen.addstr((y // 2 + 3), x // 2 - len(instruction) // 2, instruction, curses.color_pair(1) | curses.A_BLINK)

    screen.getch()
    screen.refresh()
    screen.clear()
    curses.curs_set(1)
    curses.endwin()


curses.wrapper(main)
