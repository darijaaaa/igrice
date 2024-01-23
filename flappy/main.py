ekran_velicina = (400, 600)  # velicina ekrana (odnos 2:3)

stvX = 200
stvY = 50
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (stvX, stvY)

import pygame
import random

pygame.init()

fps = 30
aPfe = 1  # ubrzanje
sPfe = 20  # skok
cevRange = (-550, -200)
vCev = 10
hsFile = open("highscore.txt", "r")
highScore = int(hsFile.read())
hsFile.close()
hFile = open("holder.txt", "r")
holder = hFile.read()
hFile.close()
pygame.display.set_caption("igrica")
pygame.display.set_icon(pygame.image.load("pfeLogo.png"))
fontNaslov = pygame.font.Font("Comic Sans MS Bold.ttf", 70)
fontScore = pygame.font.Font("Comic Sans MS.ttf", 30)
naslov = fontNaslov.render("igrica", True, (255, 255, 255))
pravi_ekran = pygame.display.set_mode((500, 750))
ekran = pravi_ekran.copy()
pravi_ekran = pygame.display.set_mode(ekran_velicina)
pozadina = pygame.image.load("background.png").convert_alpha()
pfe = pygame.image.load("pfe.png").convert_alpha()
pfeCev = pygame.image.load("pfepipe.png").convert_alpha()
pfeMask = pygame.mask.from_surface(pfe)
cevMask = pygame.mask.from_surface(pfeCev)


def meni():
    ekran.blit(pozadina, (0, 0))
    ekran.blit(naslov, (100, 250))
    hsText = fontScore.render(("rekord: " + str(highScore)), True, (255, 255, 0))
    holderText = fontScore.render(("rekord drzi: " + holder), True, (255, 255, 0))
    ekran.blit(hsText, (170, 350))
    ekran.blit(holderText, (50, 400))
    ekran.blit(pygame.transform.scale(pygame.image.load("pfeLogo.png"), (295, 295)), (80, 450))
    crtaj()
    meniLoop = True
    while meniLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                meniLoop = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                meniLoop = False


def crtaj():
    pravi_ekran.blit(pygame.transform.scale(ekran, ekran_velicina), (0, 0))
    pygame.display.flip()


def runda():
    skok = False
    score = 0
    xPfe = 100
    yPfe = 300
    vPfe = 0  # brzina
    xCev = 800
    yCev = random.randrange(cevRange[0], cevRange[1])
    poen = False
    global highScore


    rundaLoop = True
    while rundaLoop:
        pocVreme = pygame.time.get_ticks()

        #  input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                rundaLoop = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if not skok:
                    vPfe = -sPfe
                    skok = True
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                skok = False

        #  fiska
        xCev -= vCev
        vPfe += aPfe
        yPfe += vPfe
        if yPfe < -20:
            yPfe = 745
        elif yPfe > 745:
            yPfe = 0
        if xCev < -50:
            xCev = 520
            yCev = random.randrange(cevRange[0], cevRange[1])
        elif xCev + 70 > xPfe and xCev < xPfe + 79:
            poen = True
            kolizija = pygame.mask.from_surface(pygame.transform.rotate(pfe, 10-vPfe*2)).overlap(cevMask, (xCev - xPfe, yCev - yPfe))
            if kolizija is not None:
                rundaLoop = False

        else:
            if poen:
                poen = False
                score += 1

        #  crtanje
        hsText = fontScore.render((str(highScore)), True, (255, 255, 0))
        scText = fontScore.render((str(score)), True, (255, 255, 0))
        ekran.blit(pozadina, (0, 0))
        ekran.blit(pfeCev, (xCev, yCev))
        ekran.blit(pygame.transform.rotate(pfe, 10-vPfe*2), (xPfe, yPfe))
        ekran.blit(hsText, (5, 0))
        ekran.blit(scText, (460, 0))
        crtaj()
        pygame.time.delay((1000 // fps) - pygame.time.get_ticks() + pocVreme)
        
    if score > highScore:
        rekord(score)
        highScore = score
        score = 0


def rekord(score):
    global highscore
    highScore = score
    file = open("highscore.txt", "w")
    file.write(str(highScore))
    file.close()
    text1 = fontScore.render("Rekord je oboren.", True, (255, 255, 0))
    text2 = fontScore.render("Unesi svoje ime: ", True, (255, 255, 0))
    crtaj()
    global holder
    holder = ""
    ekran.blit(pozadina, (0, 0))
    ekran.blit(text1, (150, 300))
    ekran.blit(text2, (150, 350))
    crtaj()
    unos = True
    while unos:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    unos = False
                elif event.key == pygame.K_BACKSPACE:
                    ekran.blit(pozadina, (0, 0))
                    ekran.blit(text1, (150, 300))
                    ekran.blit(text2, (150, 350))
                    holder = holder[:-1]
                    ekran.blit(fontScore.render(holder, True, (255, 255, 0)), (150, 400))
                    crtaj()
                else:
                    holder += event.unicode
                    ekran.blit(fontScore.render(holder, True, (255, 255, 0)), (150, 400))
                    crtaj()
    file = open("holder.txt", "w")
    file.write(holder)
    file.close()


#filer = open("highScore.txt", "w"); filer.write("0"); filer.close()

while True:
    meni()
    runda()
