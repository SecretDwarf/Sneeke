import pygame
import time
import numpy.random as npr

global default_snake_speed, snake_speed, frames, tileSize, grid, corners, fruitSquares, fruit_position, score, level, nls
nls = 5
default_snake_speed = 2
frames = default_snake_speed

snake_speed = default_snake_speed
 
window_x = 600
window_y = 600
tileSize = 30

 
black = pygame.Color(49,54,57)
white = pygame.Color(250, 249, 246) 
red = pygame.Color(215, 0, 64)
green = pygame.Color(107,163,83)
blue = pygame.Color(86, 132, 174)
randomColor = pygame.Color(npr.randint(45,256), npr.randint(45,256), npr.randint(45,256))
 
pygame.init()
 
pygame.display.set_caption('Sneeke')
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
 
snake_position = [1,0]
 
snake_body = [0,0]
 
fruit_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0
level = 1
def show_menu(color, font, size, levelUp):
    global score, level
    score_font = pygame.font.SysFont(font, size)
    menu_surface = score_font.render(f'Press space to pause | Rank Score : {str(score)} | Points to level up: {str(levelUp - score)} | Level {level}', True, color)
    menu_rect = menu_surface.get_rect()
    game_window.blit(menu_surface, menu_rect)
    
    if score >= levelUp:
        global tileSize, nls, frames, default_snake_speed, snake_speed
        level += 1
        score = 0
        nls +=1
        default_snake_speed = 2 + 0.25*level
        frames = default_snake_speed
        snake_speed = default_snake_speed
        newGrid()
 
# game over function
def game_over():
   
    my_font = pygame.font.SysFont('times new roman', 50)
    global level, score
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score + 10 * (level - 1)), True, red)
      
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

lineDensity = 0.9
stopProb = 0.75

grid = [[0]]
corners = [0]
fruitsquares = [[0]]
fruit_position = [0]

grid_x = int(window_x/tileSize)
grid_y = int(window_y/tileSize)
def newGrid():
    global grid, corners, snake_body, fruit_spawn, direction, snake_position
    
    snake_position = [0,0]
 
    snake_body = [[0,0]]
    
    fruit_spawn = True
    direction = 'RIGHT'
    grid = [[1]*grid_x, [1]+[0]*(grid_x-2)+[1]]
    corners = []
    while len(grid) < grid_y - 1:
        rand = npr.random(1)
        if rand < lineDensity:
            val = npr.randint(0,2)
            count = round(npr.normal(grid_x/3, grid_x/4))
            count = 1 if count < 1 else count
            count = grid_x-2 if count > grid_x-2 else count
            grid.append([1]+[val]*(count-1)+[1-val]*(grid_x - count - 1)+[1])
            corners.append([len(grid)-1, (count - 1) if val == 1 else count])
            if len(grid) < grid_y - 1:
                grid.append([1]+[0]*(grid_x-2)+[1])
        else: 
            grid.append([1]+[0]*(grid_x-2)+[1])
    grid.append([1]*grid_x)
    for corner in corners:
        row = corner[0]
        column = corner[1]
        colDirection = npr.randint(0,2)
        stop = False
        while not stop:
            row += 1 if colDirection == 0 else -1
            if row == 0 or row == grid_y:
                stop = True
                break
            if grid[row][column] == 1 and npr.random(1) < stopProb:
                stop = True
                break
            grid[row][column] = 1
    global fruitSquares, fruit_position
    fruitSquares = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                fruitSquares.append([j,i])
    fruitNum = npr.randint(0, len(fruitSquares))
    fruit_position = fruitSquares[fruitNum]
newGrid()
# Main Function
accumulator = 0
while True:
    accumulator += 1
    framesPerMove = round(frames/snake_speed)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_SPACE:
                snake_speed = 0.0000000001 if snake_speed != 0.0000000001 else default_snake_speed
            if event.key == pygame.K_q:
                game_over()
            if event.key == pygame.K_r:
                newGrid()
            if event.key == pygame.K_l:
                for i in range(1000):
                    newGrid()
                    fps.tick(100)
        elif event.type == pygame.QUIT:
            game_over()
 
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    if accumulator % int(framesPerMove) == 0:
        if direction == 'UP':
            snake_position[1] -= 1
        elif direction == 'DOWN':
            snake_position[1] += 1
        elif direction == 'LEFT':
            snake_position[0] -= 1
        elif direction == 'RIGHT':
            snake_position[0] += 1
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            default_snake_speed *= 1.07
            frames = default_snake_speed
            snake_speed = default_snake_speed
            randomColor = pygame.Color(npr.randint(0,256), npr.randint(0,256), npr.randint(0,256))
            fruit_spawn = False
        else:
            snake_body.pop()
        if not fruit_spawn:
            fruitNum = npr.randint(0, len(fruitSquares))
            fruit_position = fruitSquares[fruitNum]
        if snake_position[0] < 0 or snake_position[0] > grid_x-1:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > grid_y-1:
            game_over()
        if grid[snake_position[1]][snake_position[0]] == 0:
            game_over()
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()
         
    fruit_spawn = True
    game_window.fill(green)
    for i in range(len(grid)):
        for j in range(len(grid[1])):
            if grid[i][j] == 1:
                pygame.draw.rect(game_window, black, 
                                 pygame.Rect(j*tileSize, i*tileSize, tileSize, tileSize));
                                 
    for pos in snake_body:
        pygame.draw.rect(game_window, randomColor,
                         pygame.Rect(pos[0] * tileSize + tileSize/20, pos[1] * tileSize+ tileSize/20, tileSize*0.9, tileSize*0.9))
        
    pygame.draw.rect(game_window, red, pygame.Rect(
        fruit_position[0] * tileSize+ tileSize/20, fruit_position[1] * tileSize+ tileSize/20, tileSize*0.9, tileSize*0.9))
 
    show_menu(white, 'times new roman', 20, nls)
    
    if snake_speed  == 0.0000000001:
        pause_font = pygame.font.SysFont('times new roman', 20)
        pause_surface = pause_font.render(f'Game Paused... Press space to continue.', True, white)
        pause_rect = pause_surface.get_rect(center = (window_x/2, window_y/2))
        game_window.blit(pause_surface, pause_rect)

        pause_surface = pause_font.render('Press "Q" to quit', True, white)
        pause_rect = pause_surface.get_rect(center = (window_x/2, (window_y/2) + 30))
        game_window.blit(pause_surface, pause_rect)

    pygame.display.update()
    fps.tick(frames)