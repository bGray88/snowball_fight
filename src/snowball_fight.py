import pygame, sys, time, random, player, level, projectile
from pygame.locals import *
from player import *
from level import *
from projectile import *
from time import sleep

pygame.init()

# needed colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (119, 136, 153)

# set up the window
SCREEN_MODES = pygame.display.list_modes(32)
try:
    MODE_INDEX = SCREEN_MODES.index((1280, 720))
except:
    MODE_INDEX = 1
DISPLAYSURF = pygame.display.set_mode(SCREEN_MODES[MODE_INDEX], FULLSCREEN, 32)
DISPLAYX = SCREEN_MODES[MODE_INDEX][0]
DISPLAYY = SCREEN_MODES[MODE_INDEX][1]
SCREEN_CENTER = ((DISPLAYX / 2), (DISPLAYY / 2))

# character types
SMALL_FRY = [int(DISPLAYX / 22), int(DISPLAYY / 7), 5, 12, 36]
BIG_GUY = [int(DISPLAYX / 10), int(DISPLAYY / 5), 2, 9, 45]
AVG_JOE = [int(DISPLAYX / 15), int(DISPLAYY / 6), 3, 10, 41]
CHAR_STATS = [SMALL_FRY, BIG_GUY, AVG_JOE]
CHAR_NAMES = ['SMALL_FRY', 'BIG_GUY', 'AVG_JOE']
CHAR_SELECT_IMGS = [
                    'imgs\\char01.png',
                    'imgs\\char02.png',
                    'imgs\\char03.png'
                    ]
SNOW_BOUND = [Rect((DISPLAYX / 2) - (DISPLAYX / 21), 0, (DISPLAYX / 21), DISPLAYY)]
LEVEL_STATS = [SNOW_BOUND]
LEVEL_NAMES = [
               'SNOW_BOUND'
               ]
LEVEL_SELECT_IMGS = [
                     'imgs\\bkgd_2split.png'
                     ]
SNOWBALL_IMGS = [
                'imgs\\snowball01.png',
                'imgs\\snowball02.png',
                'imgs\\snowball03.png'
                ]
SF_ART = [
          'imgs\\char01-player01.png',
		  'imgs\\char01-player02.png'
          ]
BG_ART = [
          # animations
          ]
AJ_ART = [
          # animations
          ]
CHAR_ANIMATIONS = [SF_ART, BG_ART, AJ_ART]
HEALTH_BAR_IMGS = [
                   'imgs\\HealthBarBkgd.png',
                   'imgs\\HealthBar.png',
                   'imgs\\HealthBarContainer.png'
                   ]

PREF_FONT = 'fnts\\Raleway-Black.ttf'
DEFAULT_FONT = 'fnts\\freesansbold.ttf'

def main():
    fps = 30
    fpsClock = pygame.time.Clock()
    
    pygame.display.set_caption('Snowball Fight')
    
    exitMain = None
    
    playersSelected = False
    player1Selected = None
    player2Selected = None
    
    levelSelected = False
    selectedLevel = None
    
    p1Snowball = []
    p2Snowball = []
    
    refresh_screen()
    
    # run the game loop
    while True:
        # Main Menu display
        while exitMain == None:
            exitMain = screen_main_menu()
            if exitMain == 'Settings':
                exitMain = None
                
        # Select the characters
        while playersSelected == False:
            if player1Selected == None:
                player1Selected = screen_select_char('1')
            elif player2Selected == None:
                player2Selected = screen_select_char('2')
            else:
                player1 = set_char('1', player1Selected)
                player2 = set_char('2', player2Selected)
                playersSelected = True
                
        while levelSelected == False:
            if selectedLevel == None:
                selectedLevel = screen_select_level()
            else:
                currentLevel = set_level(selectedLevel)
                levelSelected = True
        
        screen_play_ball(currentLevel, player1, player2, p1Snowball, p2Snowball)
        
        fpsClock.tick(fps)

def build_health_bar(charName, playerNum, playerMaxHealth, playerCurrentHealth):
    barStart = None
    X = 0
    Y = 1
    displayedName = charName
    barMaxDisplay = playerMaxHealth
    barCurrentDisplay = playerCurrentHealth
    charNameFont = pygame.font.Font(PREF_FONT, int(DISPLAYX / 10))
    if playerNum % 2 == 0:
        barStart = (SCREEN_CENTER[X] + \
                    (SCREEN_CENTER[X] - \
                     (int(DISPLAYX / 20) + (int(SCREEN_CENTER[X]) - (int(DISPLAYX / 15))))), 
                    DISPLAYY - int(DISPLAYY / 10))
    else:
        barStart = (int(DISPLAYX / 20), DISPLAYY - int(DISPLAYY / 10))
    charNameLabel = charNameFont.render(displayedName, True, BLACK)
    charLabelLoc = (barStart[0], barStart[1] + int(DISPLAYY / 20))
    DISPLAYSURF.blit(pygame.transform.scale(
                                            pygame.image.load(HEALTH_BAR_IMGS[0]), 
                                            (int(SCREEN_CENTER[X]) - int(DISPLAYX / 15),
                                             int(DISPLAYY / 15))
                                            ), 
                     barStart)

def end_program():
    pygame.quit()
    sys.exit()

def input_button():
    LEFT_BUTTON = 1
    MIDDLE_BUTTON = 2
    RIGHT_BUTTON = 3
    for event in pygame.event.get():
        if event.type == QUIT:
            return 'wQuit'
        if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'kEsc'
                if event.key == K_RETURN:
                    return 'kReturn'
                if event.key == K_TAB:
                    return 'kTab'
                if event.key == K_KP_PLUS:
                    return 'kp+'
        if event.type == KEYUP:
            if event.key == K_w or event.key == K_s:
                return 'lkYRelease'
            if event.key == K_a or event.key == K_d:
                return 'lkXRelease'
            if event.key == K_KP8 or event.key == K_KP5:
                return 'kpYRelease'
            if event.key == K_KP4 or event.key == K_KP6:
                return 'kpXRelease'
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_BUTTON:
            return 'mButton1'
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE_BUTTON:
            return 'mButton2'
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_BUTTON:
            return 'mButton3'
       
def input_motion():
    mouseLoc = pygame.mouse.get_pos()
    return mouseLoc
    
def load_image(imgName):
    loadedImg = pygame.image.load(imgName)
    return loadedImg

def refresh_screen():
    DISPLAYSURF.fill(BLACK)
    pygame.display.flip()

def reset_game():
    main()
    
def screen_main_menu():
    DISPLAYSURF.fill(WHITE)
    screenXCenter = SCREEN_CENTER[0]
    screenYCenter = SCREEN_CENTER[1]
    menuTitleFont = pygame.font.Font(PREF_FONT, int(DISPLAYX / 10))
    startMenuFont = pygame.font.Font(DEFAULT_FONT, int(DISPLAYX / 22))
    startMenuStrings = ['START', 'SETTINGS']
    menuLabel = menuTitleFont.render('SNOWBALL FIGHT!', True, BLACK)
    startLabel = startMenuFont.render(startMenuStrings[0], True, BLACK)
    settingsLabel = startMenuFont.render(startMenuStrings[1], True, BLACK)
    mainMenuLabels = [startLabel, settingsLabel]
    DISPLAYSURF.blit(
                     menuLabel,
                     (screenXCenter - (menuLabel.get_rect().width / 2),
                     screenYCenter / 5)
                    )
    mainMenuLabelRects = [
                         (Rect(screenXCenter - (menuLabel.get_rect().width / 2),
                          screenYCenter / 8 * 9,
                          startLabel.get_rect().width,
                          startLabel.get_rect().height)),
                         (Rect(screenXCenter - (menuLabel.get_rect().width / 2),
                          screenYCenter / 8 * 11,
                          settingsLabel.get_rect().width,
                          settingsLabel.get_rect().height))
                         ]
    bPressed = input_button()
    mLocation = input_motion()
    for i in range(0, len(mainMenuLabels)):
        if mainMenuLabelRects[i].collidepoint(mLocation):
            mainMenuLabels[i] = startMenuFont.render(startMenuStrings[i], True, GRAY)
            if bPressed == 'mButton1' and mainMenuLabelRects[0].collidepoint(mLocation):
                refresh_screen()
                return True
            if bPressed == 'mButton1' and mainMenuLabelRects[1].collidepoint(mLocation):
                refresh_screen()
                return 'Settings'
        else:
            mainMenuLabels[i] = startMenuFont.render(startMenuStrings[i], True, BLACK)
        DISPLAYSURF.blit(mainMenuLabels[i], (mainMenuLabelRects[i].left, mainMenuLabelRects[i].top))
        pygame.display.update(mainMenuLabelRects[i])
    pygame.display.flip()
    if bPressed == 'kReturn':
        refresh_screen()
        return True
    elif bPressed == 'kEsc' or bPressed == 'wQuit':
        end_program()

def screen_play_ball(ballLevel, ballPlayer1, ballPlayer2, ballSnowballP1, ballSnowballP2):
    screenXCenter = SCREEN_CENTER[0]
    screenYCenter = SCREEN_CENTER[1]
    
    #Screen build
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(
                     pygame.transform.scale(ballLevel.bkgdImg,
                                            (DISPLAYX, DISPLAYY)), 
                                            (ballLevel.levelBorder.left, ballLevel.levelBorder.top)
                     )
    ballPlayer1.check_internal_bounds(ballLevel.levelBorder)
    ballPlayer2.check_internal_bounds(ballLevel.levelBorder)
    ballPlayer1.check_external_bounds(ballLevel.walls)
    ballPlayer2.check_external_bounds(ballLevel.walls)
    
    #Character build
    DISPLAYSURF.blit(pygame.transform.scale(ballPlayer1.currentAnimateImg, 
                                            (ballPlayer1.playerRect.width, ballPlayer2.playerRect.height)), 
                                            (ballPlayer1.playerRect.left, 
                                             ballPlayer1.playerRect.top))
    DISPLAYSURF.blit(pygame.transform.scale(pygame.transform.flip(ballPlayer2.currentAnimateImg, True, False), 
                                            (ballPlayer1.playerRect.width, ballPlayer2.playerRect.height)), 
                                            (ballPlayer2.playerRect.left, 
                                             ballPlayer2.playerRect.top))
    bPressed = input_button()
    
    # End scenario
    winStatus = None
    winFont = pygame.font.Font(PREF_FONT, int(DISPLAYX / 10))
    if bPressed == 'kEsc' or bPressed == 'wQuit':
        end_program()
    if ballPlayer1.currentHealth == 0:
        winStatus = 'Player 2 Wins!'
        winLabel = winFont.render(winStatus, True, BLACK)
    elif ballPlayer2.currentHealth == 0:
        winStatus = 'Player 1 Wins!'
        winLabel = winFont.render(winStatus, True, BLACK)
    if winStatus != None:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(
                         winLabel,
                        (screenXCenter - (winLabel.get_rect().width / 2),
                         screenYCenter / 5)
                         )
        pygame.display.flip()
        winStatus = None
        sleep(3)
        reset_game()
    
    # Character movement
    if bPressed == 'lkYRelease':
        ballPlayer1.reset_speed('yRelease')
    if bPressed == 'lkXRelease':
        ballPlayer1.reset_speed('xRelease')
    if bPressed == 'kpYRelease':
        ballPlayer2.reset_speed('yRelease')
    if bPressed == 'kpXRelease':
        ballPlayer2.reset_speed('xRelease')
    keyPressed = pygame.key.get_pressed()
    if keyPressed[K_d]:
        ballPlayer1.move_player('Up')
        ballPlayer1.animate_player(-1)
    if keyPressed[K_s]:
        ballPlayer1.move_player('Down')
        ballPlayer1.animate_player(1)
    if keyPressed[K_w]:
        ballPlayer1.move_player('Left')
        ballPlayer1.animate_player(-1)
    if keyPressed[K_x]:
        ballPlayer1.move_player('Right')
        ballPlayer1.animate_player(1)
    if keyPressed[K_KP4]:
        ballPlayer2.move_player('Up')
        ballPlayer2.animate_player(-1)
    if keyPressed[K_KP5]:
        ballPlayer2.move_player('Down')
        ballPlayer2.animate_player(1)
    if keyPressed[K_KP2]:
        ballPlayer2.move_player('Left')
        ballPlayer2.animate_player(1)
    if keyPressed[K_KP8]:
        ballPlayer2.move_player('Right')
        ballPlayer2.animate_player(-1)
    
    # Snowball throwing
    if bPressed == 'kTab':
        ballSnowballP1.append(snow_ball(ballPlayer1.throw_projectile(1), ballPlayer1, ballPlayer2))
    for thrownP1 in ballSnowballP1:
        DISPLAYSURF.blit(pygame.transform.scale(thrownP1.projImg, (int(DISPLAYX / 80), int(DISPLAYY / 45))), 
                         (thrownP1.rect.left, thrownP1.rect.top))
        thrownP1.move_projectile()
        if thrownP1.rect.colliderect(ballPlayer2.playerRect):
            removeSnowBall1 = None
            while removeSnowBall1 != 'removeProj':
                removeSnowBall1 = thrownP1.animate_proj()
                DISPLAYSURF.blit(pygame.transform.scale(thrownP1.projImg, 
                                                        (int(DISPLAYX / 80), int(DISPLAYY / 45))), 
                                 (thrownP1.rect.left, thrownP1.rect.top))
                pygame.display.flip()
            removeSnowBall1 = None
            ballPlayer2.get_hit_reaction(2, ballPlayer1.throwSpeed)
            ballSnowballP1.remove(thrownP1)
        if not Rect(0, 0, DISPLAYX, DISPLAYY).contains(thrownP1):
            if thrownP1.rect.top <= 0:
                thrownP1.reverse_projY_direction()
            elif thrownP1.rect.bottom >= DISPLAYY:
                thrownP1.reverse_projY_direction()
            else:
                ballSnowballP1.remove(thrownP1)
    if bPressed == 'kp+':
        ballSnowballP2.append(snow_ball(ballPlayer2.throw_projectile(2), ballPlayer2, ballPlayer1))
    for thrownP2 in ballSnowballP2:
        DISPLAYSURF.blit(pygame.transform.scale(pygame.transform.flip(thrownP2.projImg, True, False),
                                                (int(DISPLAYX / 80), int(DISPLAYY / 45))), 
                         (thrownP2.rect.left, thrownP2.rect.top))
        thrownP2.move_projectile()
        if thrownP2.rect.colliderect(ballPlayer1.playerRect):
            removeSnowBall2 = None
            while removeSnowBall2 != 'removeProj':
                removeSnowBall2 = thrownP2.animate_proj()
                DISPLAYSURF.blit(pygame.transform.scale(pygame.transform.flip(thrownP2.projImg, True, False),
                                                (int(DISPLAYX / 80), int(DISPLAYY / 45))), 
                                 (thrownP2.rect.left, thrownP2.rect.top))
                pygame.display.flip()
            removeSnowBall2 = None
            ballPlayer1.get_hit_reaction(1, ballPlayer2.throwSpeed)
            ballSnowballP2.remove(thrownP2)
        if not Rect(0, 0, DISPLAYX, DISPLAYY).contains(thrownP2):
            if thrownP2.rect.top <= 0:
                thrownP2.reverse_projY_direction()
            elif thrownP2.rect.bottom >= DISPLAYY:
                thrownP2.reverse_projY_direction()
            else:
                ballSnowballP2.remove(thrownP2)
    
    build_health_bar(ballPlayer1.name, 1, ballPlayer1.maxHealth, ballPlayer1.currentHealth)
    build_health_bar(ballPlayer2.name, 2, ballPlayer2.maxHealth, ballPlayer2.currentHealth)
    
    # Refresh screen
    pygame.display.flip()

def screen_select_char(playerNum):
    DISPLAYSURF.fill(WHITE)
    winWidth, winHeight = DISPLAYX, DISPLAYY
    numChars = len(CHAR_SELECT_IMGS)
    charLayout = ((numChars + 1) * 2)
    imgHeight =  (winHeight / 3)
    imgWidth = winWidth / (charLayout - 1)
    charImgRects = []
    for i in range(1, charLayout):
        if (i % 2) != 0:
            charImgRects.append(Rect(i * imgWidth, imgHeight,
                                    imgWidth, imgHeight))
    for i in range(0, len(CHAR_SELECT_IMGS)):
        loadedImg = load_image(CHAR_SELECT_IMGS[i])
        DISPLAYSURF.blit(
                         pygame.transform.scale(loadedImg, 
                                                (int(imgWidth), int(imgHeight))), 
                        (charImgRects[i].left, charImgRects[i].top)
                        )
    titleFont = pygame.font.Font(PREF_FONT, int(DISPLAYX / 12))
    titleLabel = titleFont.render('Select Player ' + playerNum, True, BLACK)
    DISPLAYSURF.blit(titleLabel, (SCREEN_CENTER[0] - (titleLabel.get_rect().width / 2), (DISPLAYX / 20)))
    pygame.display.flip()
    bPressed = input_button()
    mLocation = input_motion()
    for i in range(0, len(charImgRects)):
        if bPressed == 'mButton1' and charImgRects[i].collidepoint(mLocation):
            return i
    if bPressed == 'kEsc':
        reset_game()

def screen_select_level():
    DISPLAYSURF.fill(WHITE)
    winWidth, winHeight = DISPLAYX, DISPLAYY
    numLevels = len(LEVEL_SELECT_IMGS)
    levelLayout = ((numLevels + 1) * 2)
    imgHeight = (winHeight / 3)
    imgWidth = (winWidth / (levelLayout - 1))
    levelImgRects = []
    for i in range(1, levelLayout):
        if (i % 2) != 0:
            levelImgRects.append(Rect(i * imgWidth, imgHeight,
                                    imgWidth, imgHeight))
    for i in range(0, numLevels):
        loadedImg = load_image(LEVEL_SELECT_IMGS[i])
        DISPLAYSURF.blit(
                         pygame.transform.scale(loadedImg, 
                                                (int(imgWidth), int(imgHeight))), 
                        (levelImgRects[i].left, levelImgRects[i].top)
                        )
    titleFont = pygame.font.Font(PREF_FONT, int(DISPLAYX / 12))
    titleLabel = titleFont.render('Select Level', True, BLACK)
    DISPLAYSURF.blit(titleLabel, (SCREEN_CENTER[0] - (titleLabel.get_rect().width / 2), (DISPLAYX / 20)))
    pygame.display.flip()
    bPressed = input_button()
    mLocation = input_motion()
    for i in range(0, len(levelImgRects)):
        if bPressed == 'mButton1' and levelImgRects[i].collidepoint(mLocation):
            return i
    if bPressed == 'kEsc':
        reset_game()

def set_char(playerNum, selectNum):
    chosenChar = CHAR_STATS[selectNum]
    chosenCharName = CHAR_NAMES[selectNum]
    charWidth = chosenChar[0]
    charHeight = chosenChar[1]
    charSpeed = chosenChar[2]
    charMaxSpeed = chosenChar[3]
    charThrowSpeed = chosenChar[4]
    if playerNum == '1':
        charStartPos = (int(DISPLAYX / 20), int(DISPLAYY / 15))
    elif playerNum == '2':
        charStartPos = ((DISPLAYX - (charWidth + int(DISPLAYX / 20))), int(DISPLAYY / 15))
    charPortrait = CHAR_SELECT_IMGS[selectNum]
    player = Player(
                    charWidth,
                    charHeight,
                    charSpeed,
                    charMaxSpeed,
                    charStartPos,
                    charThrowSpeed,
                    chosenCharName,
                    charPortrait
                    )
    charAnimate = CHAR_ANIMATIONS[selectNum]
    player.set_player_animate(charAnimate)
    return player

def set_level(selectNum):
    chosenLevel = LEVEL_STATS[selectNum]
    chosenLevelName = LEVEL_NAMES[selectNum]
    levelWindow = (DISPLAYX, DISPLAYY)
    levelPortrait = LEVEL_SELECT_IMGS[selectNum]
    level = Level(
                  chosenLevelName, 
                  levelWindow, 
                  levelPortrait,
                  chosenLevel
                  )
    return level

def snow_ball(snowballStats, pRectA, pRectB):
    throwSpeed = snowballStats[0]
    throwDirection = snowballStats[1]
    ballStart = (pRectA.playerRect.left, pRectA.playerRect.top, pRectA.playerRect.width, pRectA.yMid)
    if throwDirection > 0:
        snowball = Projectile(Rect(ballStart[0] + ballStart[2], ballStart[1] + ballStart[3], 25, 25),
                              throwSpeed, 
                              throwDirection,
                              SNOWBALL_IMGS[0])
    else:
        snowball = Projectile(Rect(ballStart[0] - 10, ballStart[1] + ballStart[3], 25, 25), 
                              throwSpeed, 
                              throwDirection,
                              SNOWBALL_IMGS[0])
    snowball.set_proj_animate(SNOWBALL_IMGS)
    return snowball

if __name__ == '__main__':
    main()
