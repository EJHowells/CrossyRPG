import pygame

#screen details
SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

#colours according to RBG codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

#clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class GameObject:
    
    def __init__(self, img_path, x, y, w, h):
        #load player img and scale
        object_image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(object_image, (w, h))
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        
    #draw object by blitting it onto background (game screen)   
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

#character controlled by player
class PlayerCharacter(GameObject):
    
    #tiles moved per second
    SPEED = 10
    
    def __init__(self, img_path, x, y, w, h):
        super().__init__(img_path, x, y, w, h)
        
    def move(self, direction, max_h):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction <0:
            self.y_pos += self.SPEED
        
        #bounds for player
        if self.y_pos >= max_h - 20:
            self.y_pos = max_h - 20
            
    #return false (no collision) if x and y positions do not overlap
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.h:
            return False
        elif self.y_pos + self.h < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.w:
            return False
        elif self.x_pos + self.w < other_body.x_pos:
            return False
        
        return True
        
#Class to represent the enemies moving left to right and right to left
class NonPlayerCharacter(GameObject):
 
    # How many tiles the character moves per second
    SPEED = 5
 
    def __init__(self, img_path, x, y, w, h):
        super().__init__(img_path, x, y, w, h)
 
    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_w):
        if self.x_pos <= 5:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >=  max_w - 50:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

class Game:
    #typical rate of 60, equiv to FPS
    TICK_RATE = 60
    
    #initialiser for the game class 
    def __init__(self, img_path, title, w, h):
        self.title = title
        self.w = w
        self.h = h
        
        #create window and set colour
        self.game_screen = pygame.display.set_mode((w, h))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        
        #load up and scale background image
        background_image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(background_image, (w, h))
        
    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0
        
        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        
        enemy_0 = NonPlayerCharacter('enemy.png', 20, 550, 50, 50)
        enemy_0.SPEED *= level_speed
        
        enemy_1 = NonPlayerCharacter('enemy.png', self.w - 50, 400, 50, 50)
        enemy_1.SPEED *= level_speed
        
        enemy_2 = NonPlayerCharacter('enemy.png', 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed
        
        enemies = [enemy_0, enemy_1, enemy_2]
        
        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        
        #main game loop to update all gameplay
        #runs until is_game_over = True
        while not is_game_over:

            #loop to get all events occuring at any given time
            #events like mouse movement, button clicks, exit etc.
            for event in pygame.event.get():
                #quit event leads to exit
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN: #detect key press
                    if event.key == pygame.K_UP: #move up
                        direction = 1
                    elif event.key == pygame.K_DOWN: #move down
                        direction = -1
                elif event.type == pygame.KEYUP: #detect key press stopped
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: #stop movement
                        direction = 0

                print(event)
                
            #redraw background screen
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))
            
            #draw trasure
            treasure.draw(self.game_screen)
            
            #move and draw player
            player_character.move(direction, self.h)
            player_character.draw(self.game_screen)
            
            #move and draw enemy0
            enemy_0.move(self.w)
            enemy_0.draw(self.game_screen)
            
            #move and draw more enemies at higher levels
            if level_speed > 1:
                enemy_1.move(self.w)
                enemy_1.draw(self.game_screen)
                
            if level_speed > 2:
                enemy_2.move(self.w)
                enemy_2.draw(self.game_screen)
            
            #detect collision and quit game
            if player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You Won!', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            
            else:
                for enemy in enemies:
                    if player_character.detect_collision(enemy):
                        is_game_over = True
                        did_win = False
                        text = font.render('You Lose!', True, BLACK_COLOR)
                        self.game_screen.blit(text, (300, 350))
                        pygame.display.update()
                        clock.tick(1)
                        break

            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)
        
        #restart game loop if won, quit game if lose
        if did_win:
            self.run_game_loop(level_speed + 0.5) #recurrsion    
        else:
            return

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

#quit pygame and program
pygame.quit()
quit()

    
