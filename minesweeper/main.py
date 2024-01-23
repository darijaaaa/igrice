stranica = 25 # stranica jednog polja
x, y = 30, 20 # dimenzije table
brMina = 60   # broj mina

import pygame
import random

pygame.init()

mine = []
prikaz = []
strPolja = 75
praviEkran = pygame.display.set_mode((stranica * x, stranica * (y + 1)))
ekran = pygame.Surface((strPolja * x, strPolja * (y + 1)))
pygame.display.set_caption("igrica")
polje = pygame.image.load("polje.png").convert_alpha()
zPolje = pygame.image.load("zatvoreno.png").convert_alpha()
zastava = pygame.image.load("zastava.png").convert_alpha()
mina = pygame.image.load("mina.png").convert_alpha()
pobMina = pygame.image.load("pobMina.png").convert_alpha()
font = pygame.font.Font("Comic Sans MS Bold.ttf", 60)
brojacMina = brMina
brojacPolja = x*y - brMina
krajIgre = False
pobeda = False
rez = ""


def generisi_mine(brMine):
    global mine
    global prikaz
    prikaz = [[0 for i in range(x)] for j in range(y)]
    mine = [[0 for i in range(x)] for j in range(y)]
    uzorak = random.sample(range(x * y), brMine)
    for u in uzorak:
        inI = u // x
        inJ = u % x
        mine[inI][inJ] = -1
        for i in range(inI - 1, inI + 2):
            for j in range(inJ - 1, inJ + 2):
                if 0 <= i < y and 0 <= j < x:
                    if mine[i][j] != -1:
                        mine[i][j] += 1


def crtaj():
    ekran.fill((0, 0, 0))
    for i in range(len(mine)):
        for j in range(len(mine[i])):
            if prikaz[i][j] == 1:
                if mine[i][j] == -1:
                    if pobeda:
                    	ekran.blit(pobMina, (strPolja * j, strPolja * i))
                    else:
                    	ekran.blit(mina, (strPolja * j, strPolja * i))
                elif mine[i][j] == 0:
                    ekran.blit(polje, (strPolja * j, strPolja * i))
                else:
                    ekran.blit(polje, (strPolja * j, strPolja * i))
                    txBroj = font.render(str(mine[i][j]), True, (0, 0, 0))
                    ekran.blit(txBroj, (strPolja * j + 15, strPolja * i - 9))
            elif prikaz[i][j] == -1:
                ekran.blit(zastava, (strPolja * j, strPolja * i))
            else:
                ekran.blit(zPolje, (strPolja * j, strPolja * i))
    txBrojacMina = font.render("Mine: "+str(brojacMina), True, (255, 255, 255))
    ekran.blit(txBrojacMina, (15, strPolja * y - 9))
    txRez = font.render(rez, True, (255, 255, 255))
    ekran.blit(txRez, (strPolja * 4 + 15, strPolja * y - 9))
    praviEkran.blit(pygame.transform.scale(ekran, (stranica * x, stranica * (y + 1))), (0, 0))
    pygame.display.flip()


def otvori_polje(pi, pj):
    prikaz[pi][pj] = 1
    global brojacPolja
    brojacPolja -= 1
    if mine[pi][pj] == 0:
        for i in range(pi - 1, pi + 2):
            for j in range(pj - 1, pj + 2):
                if 0 <= i < y and 0 <= j < x and prikaz[i][j] == 0:
                    otvori_polje(i, j)
    elif mine[pi][pj] == -1:
        kraj()
        global rez
        rez = "GUBITAK!"


def kraj():
    global prikaz
    prikaz = [[1 for i in range(x)] for j in range(y)]
    crtaj()
    global krajIgre
    krajIgre = True


generisi_mine(brMina)
crtaj()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
        elif event.type == pygame.KEYUP or (krajIgre and event.type == pygame.MOUSEBUTTONUP):
            generisi_mine(brMina)
            brojacMina = brMina
            brojacPolja = x * y - brMina
            krajIgre = False
            rez = ""
            pobeda = False
            crtaj()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousetime = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP:
            mousetime = (pygame.time.get_ticks() - mousetime)
            ex, ey = event.pos
            ex = ex * strPolja // stranica
            ey = ey * strPolja // stranica
            ei = ey // strPolja
            ej = ex // strPolja
#            if prikaz[ei][ej] == 1:
#                for i in range(ei - 1, ei + 2):
#                    for j in range(ej - 1, ej + 2):
#                        if 0 <= i < y and 0 <= j < x and prikaz[i][j] == 0:
#                            otvori_polje(i, j)
            if mousetime < 250:
                if prikaz[ei][ej] == 0:
                    otvori_polje(ei, ej)
            else:
                if prikaz[ei][ej] == 0:
                    prikaz[ei][ej] = -1
                    brojacMina -= 1
                else:
                    prikaz[ei][ej] = 0
                    brojacMina += 1
            crtaj()
    if brojacMina == 0 and brojacPolja == 0:
        pobeda = True
        kraj()
        rez = "POBEDA!!"
