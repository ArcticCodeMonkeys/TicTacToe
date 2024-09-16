import pygame
import sys
import random

def checkRows(grid):
    for row in grid:
        if row[0] == row[1] == row[2] != None:
            return row[0]
    return None

def checkDiagonals(grid):
    if grid[0][0] == grid[1][1] == grid[2][2] != None:
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != None:
        return grid[0][2]
    return None

def checkTie(grid):
    for row in grid:
        if None in row:
            return False
    return True

def draw_text(text, font, color, surface, x, y):
    renderObj = font.render(text, True, color)
    textbox = renderObj.get_rect()
    textbox.topleft = (x, y)
    surface.blit(renderObj, textbox)

# Goldfish AI (Random move)
def goldfish_ai(grid, player):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if grid[i][j] is None]
    if empty_cells:
        return random.choice(empty_cells)

# Medium AI (Looks for a win or block)
def medium_ai(grid, player):
    opponent = 'O' if player == 'X' else 'X'
    
    # Check if AI can win
    for i in range(3):
        for j in range(3):
            if grid[i][j] is None:
                grid[i][j] = player
                if checkRows(grid) or checkRows([list(reversed(col)) for col in zip(*grid)]) or checkDiagonals(grid):
                    return (i, j)
                grid[i][j] = None
    
    # Check if it needs to block player
    for i in range(3):
        for j in range(3):
            if grid[i][j] is None:
                grid[i][j] = opponent
                if checkRows(grid) or checkRows([list(reversed(col)) for col in zip(*grid)]) or checkDiagonals(grid):
                    grid[i][j] = None
                    return (i, j)
                grid[i][j] = None

    # Otherwise, pick a random move
    return goldfish_ai(grid, player)

# Impossible AI (Perfect strategy with minimax algorithm)
def minimax(grid, depth, is_maximizing, player):
    opponent = 'O' if player == 'X' else 'X'
    
    winner = checkRows(grid) or checkRows([list(reversed(col)) for col in zip(*grid)]) or checkDiagonals(grid)
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif all(grid[i][j] is not None for i in range(3) for j in range(3)):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if grid[i][j] is None:
                    grid[i][j] = player
                    score = minimax(grid, depth + 1, False, player)
                    grid[i][j] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if grid[i][j] is None:
                    grid[i][j] = opponent
                    score = minimax(grid, depth + 1, True, player)
                    grid[i][j] = None
                    best_score = min(score, best_score)
        return best_score

def impossible_ai(grid, player):
    best_move = None
    best_score = -float('inf')
    for i in range(3):
        for j in range(3):
            if grid[i][j] is None:
                grid[i][j] = player
                score = minimax(grid, 0, False, player)
                grid[i][j] = None
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move


def main():
    grid = [[None, None, None] for _ in range(3)]
    
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("TicTacToe")

    tilesize = 180
                  
    font = pygame.font.SysFont(None, 256)
    medFont = pygame.font.SysFont(None, 128)
    smallFont = pygame.font.SysFont(None, 36)
    
    ai_brain = goldfish_ai
    player = 'X'
    ai_player = 'O'
    gameState = "Start"
    running = True
    clickReady = True
    ai_move_time = 0
    ai_delay = 1000  # 1 second delay for AI move

    while running:
        if checkRows(grid) or checkRows([list(reversed(col)) for col in zip(*grid)]) or checkDiagonals(grid) or checkTie(grid):
            if checkTie(grid):
                gameState = 'tie'
            elif player == 'X':
                gameState = 'lose'
            else:
                gameState = 'win'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and clickReady:
                clickReady = False
                if gameState == "Start":
                    x_button = pygame.Rect(0, 200, tilesize, tilesize)
                    o_button = pygame.Rect(400, 200, tilesize, tilesize)
                    if x_button.collidepoint(event.pos):
                        player = 'X'
                        ai_player = 'O'
                        gameState = 'Difficulty'
                    if o_button.collidepoint(event.pos):
                        player = 'O'
                        ai_player = 'X'
                        gameState = 'Difficulty'
                elif gameState == 'Difficulty':
                    goldfish = pygame.Rect(0, 200, tilesize, tilesize)
                    average = pygame.Rect(200, 200, tilesize, tilesize)
                    impossible = pygame.Rect(400, 200, tilesize, tilesize)
                    if goldfish.collidepoint(event.pos):
                        ai_brain = goldfish_ai
                        gameState = 'Playing'
                    if average.collidepoint(event.pos):
                        ai_brain = medium_ai
                        ai_player = 'X'
                        gameState = 'Playing'
                    if impossible.collidepoint(event.pos):
                        ai_brain = impossible_ai
                        ai_player = 'X'
                        gameState = 'Playing'
                elif gameState == "Playing" and player == 'X':  # Player turn
                    col = event.pos[0] // 200
                    row = event.pos[1] // 200
                    if grid[col][row] is None:
                        grid[col][row] = player
                        player = 'O'
                        ai_move_time = pygame.time.get_ticks()  # Set AI move timer
                elif gameState == "lose" or gameState == "win" or gameState == 'tie':
                    yesButton = pygame.Rect(40, 220, 100, 160)
                    noButton = pygame.Rect(440, 220, 100, 160)
                    if yesButton.collidepoint(event.pos):
                        grid = [[None, None, None] for _ in range(3)]
                        gameState = 'Start'
                    if noButton.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                clickReady = True

        # AI move after 1 second delay
        if gameState == "Playing" and player == 'O':
            if pygame.time.get_ticks() - ai_move_time >= ai_delay:
                pos = ai_brain(grid, player)
                print(pos)
                grid[pos[0]][pos[1]] = player
                player = 'X'  # Switch back to human player

        # Draw the Grid
        screen.fill((0, 0, 0))
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, (255, 255, 255), (10 + 200 * i, 10 + 200 * j, tilesize, tilesize))
        
        # Conditional Displays
        if gameState == 'Start':
            pygame.draw.rect(screen, (0, 0, 0), (160, 100, 300, 45))
            draw_text("Select who goes first!", smallFont, (0, 0, 255), screen, tilesize, 110)
            draw_text('You', medFont, (0, 0, 0), screen, 20, 260)
            draw_text('AI', medFont, (0, 0, 0), screen, 450, 260)
        elif gameState == 'Difficulty':
            pygame.draw.rect(screen, (0, 0, 0), (160, 100, 300, 45))
            draw_text("Select your difficulty!", smallFont, (0, 0, 255), screen, tilesize, 110)
            draw_text('Goldfish', smallFont, (0, 0, 0), screen, 45, 300)
            draw_text('Average', smallFont, (0, 0, 0), screen, 255, 300)
            draw_text('Impossible', smallFont, (0, 0, 0), screen, 440, 300)
        elif gameState == 'Playing':
            for i in range(3):
                for j in range(3):
                    if grid[i][j] is not None:
                        draw_text(grid[i][j], font, (0, 0, 0), screen, 40 + i * 200, 20 + j * 200)
        elif gameState == 'lose' or gameState == "win" or gameState == 'tie':
            pygame.draw.rect(screen, (0, 0, 0), (160, 100, 300, 45))
            draw_text("You " + gameState + "! Play Again?", smallFont, (0, 0, 255), screen, tilesize, 110)
            draw_text('Yes', medFont, (0, 0, 0), screen, 20, 260)
            draw_text('No', medFont, (0, 0, 0), screen, 450, 260)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
