# velicina prozora (odnos 5:3)
sirina, visina = 1000, 600

import pygame
from math import sqrt
from random import random

pygame.init()

ekranX, ekranY = 1000, 600
velicinaEkrana = (ekranX, ekranY)
pygame.display.set_caption("igrica")
ekran = pygame.Surface(velicinaEkrana)
praviEkran = pygame.display.set_mode((sirina, visina))

duzinaShortPalice, duzinaNormalPalice, duzinaLongPalice = 100, 160, 250
duzinaPalice = duzinaNormalPalice
visinaPalice = 25
yPalice = ekranY - 30 - visinaPalice // 2
normalBrzinaPalice = 0.7
brzinaPalice = normalBrzinaPalice
promenaBrzinePalice = 0.3

precnikSmallLoptice, precnikNormalLoptice, precnikBigLoptice = 9, 13, 26
precnikLoptice = precnikNormalLoptice
normalBrzinaLoptice = 0.7
brzinaLoptice = normalBrzinaLoptice
usporenjeLoptice, ubrzanjeLoptice = 0.5, 1.4

xCigle, yCigle = 45, 87
duzinaCigle, visinaCigle = 94, 24
duzinaRazmaka, visinaRazmaka = 8, 16
duzinaRedaCigala, visinaRedaCigala = 9, 6
dozvoljenaGreska = 3

broj_Zivota = 3
vrednostZivota = 5000
slikaSrce = pygame.image.load("srce.png").convert_alpha()
razmakZivota = 4
duzinaZivota = 28

skorCigla = 500
skorCinilac = 1.11
fontSkor = pygame.font.SysFont("Courier New", 35, bold=True)
fontVeliki = pygame.font.Font("Comic Sans MS Bold.ttf", 120)
fontMali = pygame.font.Font("Comic Sans MS.ttf", 35)

slikaUpitnik = pygame.image.load("upitnik.png").convert_alpha()
brzinaUpitnika = 0.1
ucestalostUpitnika = 0.1
trajanjeUpitnika = 9000
precnikUpitnika = 43
powerup = 0
pozadina = pygame.image.load("background.png").convert_alpha()


class Palica(pygame.sprite.Sprite):
    def __init__(self, x=(ekranX - duzinaPalice) // 2):
        super().__init__()
        self.x = x
        self.slikaNormal = pygame.Surface((duzinaNormalPalice, visinaPalice))
        self.slikaNormal.set_colorkey(pygame.Color(0, 0, 0))
        self.promeniBoju((10, 255, 10), (0, 150, 0))
        self.slikaShort = pygame.Surface((duzinaShortPalice, visinaPalice))
        self.slikaShort.set_colorkey(pygame.Color(0, 0, 0))
        pygame.draw.ellipse(self.slikaShort, (10, 255, 10), (0, 0, duzinaShortPalice, visinaPalice))
        pygame.draw.ellipse(self.slikaShort, (0, 150, 0), (0, 0, duzinaShortPalice, visinaPalice), 7)
        self.slikaLong = pygame.Surface((duzinaLongPalice, visinaPalice))
        self.slikaLong.set_colorkey(pygame.Color(0, 0, 0))
        pygame.draw.ellipse(self.slikaLong, (10, 255, 10), (0, 0, duzinaLongPalice, visinaPalice))
        pygame.draw.ellipse(self.slikaLong, (0, 150, 0), (0, 0, duzinaLongPalice, visinaPalice), 7)
        self.slika = self.slikaNormal
        self.mask = pygame.mask.from_surface(self.slika)
        self.brzina = 0

    def stampaj(self):
        ekran.blit(self.slika, (self.x, yPalice))

    def loop(self, tick):
        self.x = max(min((self.x + self.brzina * tick), ekranX - duzinaPalice), 0)
        self.stampaj()

    def promeniBoju(self, bojaUnutra, bojaSpolja):
        pygame.draw.ellipse(self.slikaNormal, bojaUnutra, (0, 0, duzinaNormalPalice, visinaPalice))
        pygame.draw.ellipse(self.slikaNormal, bojaSpolja, (0, 0, duzinaNormalPalice, visinaPalice), 7)


class Loptica(pygame.sprite.Sprite):
    def __init__(self, x=(ekranX - duzinaPalice) // 2, y=yPalice - 10 - 2 * precnikLoptice):
        super().__init__()
        self.x = x
        self.y = y
        self.ispaljena = False
        self.slikaNormal = pygame.Surface((2 * precnikNormalLoptice, 2 * precnikNormalLoptice))
        self.slikaNormal.set_colorkey(pygame.Color(0, 0, 0))
        self.promeniBoju((10, 10, 255), (0, 0, 150))
        self.slikaBig = pygame.Surface((2 * precnikBigLoptice, 2 * precnikBigLoptice))
        self.slikaBig.set_colorkey(pygame.Color(0, 0, 0))
        pygame.draw.circle(self.slikaBig, pygame.Color(10, 10, 255), (precnikBigLoptice, precnikBigLoptice),
                           precnikBigLoptice)
        pygame.draw.circle(self.slikaBig, pygame.Color(0, 0, 150), (precnikBigLoptice, precnikBigLoptice),
                           precnikBigLoptice, 5)
        self.slikaSmall = pygame.Surface((2 * precnikSmallLoptice, 2 * precnikSmallLoptice))
        self.slikaSmall.set_colorkey(pygame.Color(0, 0, 0))
        pygame.draw.circle(self.slikaSmall, pygame.Color(10, 10, 255), (precnikSmallLoptice, precnikSmallLoptice),
                           precnikSmallLoptice)
        pygame.draw.circle(self.slikaSmall, pygame.Color(0, 0, 150), (precnikSmallLoptice, precnikSmallLoptice),
                           precnikSmallLoptice, 5)
        self.slika = self.slikaNormal
        global precnikLoptice, brzinaLoptice, powerup
        if powerup > 4:
            powerup = 0
        precnikLoptice = precnikNormalLoptice
        brzinaLoptice = normalBrzinaLoptice
        self.mask = pygame.mask.from_surface(self.slika)
        self.brzinaX = 0
        self.brzinaY = 0
        self.streak = 0

    def ispali(self):
        self.ispaljena = True
        self.brzinaX = brzinaLoptice / sqrt(2)
        self.brzinaY = -self.brzinaX

    def stampaj(self):
        ekran.blit(self.slika, (self.x, self.y))

    def loop(self, tick, xPalice):
        if self.ispaljena:
            self.x += self.brzinaX * tick
            self.y += self.brzinaY * tick
            if self.x < 0:
                self.x = 0
                self.brzinaX = -self.brzinaX
            elif self.x + 2 * precnikLoptice > ekranX:
                self.x = ekranX - 2 * precnikLoptice
                self.brzinaX = -self.brzinaX
            if self.y < 0:
                self.y = 0
                self.brzinaY = -self.brzinaY
            elif self.y > ekranY:
                del self
                return False
        else:
            self.x = xPalice + duzinaPalice / 2 - precnikLoptice
            self.y = yPalice - 2 * precnikLoptice - 10
        self.stampaj()
        return True

    def odbijOdPalice(self, x):
        self.streak = 0
        self.brzinaX = brzinaLoptice * 2 * (x / duzinaPalice - 0.5)
        self.brzinaY = -brzinaLoptice * sqrt(1 - 4 * (x / duzinaPalice - 0.5) ** 2)

    def promeniBoju(self, bojaUnutra, bojaSpolja):
        pygame.draw.circle(self.slikaNormal, bojaUnutra, (precnikNormalLoptice, precnikNormalLoptice),
                           precnikNormalLoptice)
        pygame.draw.circle(self.slikaNormal, bojaSpolja, (precnikNormalLoptice, precnikNormalLoptice),
                           precnikNormalLoptice, 5)


class Cigle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mask = None
        self.slika = pygame.Surface(velicinaEkrana)
        self.slika.set_colorkey(pygame.Color(0, 0, 0))
        self.cigle = [[1] * duzinaRedaCigala for _ in range(visinaRedaCigala)]
        self.brojCigli = visinaRedaCigala * duzinaRedaCigala
        self.skor = 0
        self.azuriraj(broj_Zivota)

    def azuriraj(self, brojZivota):
        self.slika.fill(pygame.Color(0, 0, 0))
        for i in range(visinaRedaCigala):
            for j in range(duzinaRedaCigala):
                if self.cigle[i][j] == 1:
                    pygame.draw.rect(self.slika, pygame.Color(255, 255, 255), (
                        xCigle + j * (duzinaCigle + duzinaRazmaka), yCigle + i * (visinaCigle + visinaRazmaka),
                        duzinaCigle,
                        visinaCigle))
                    pygame.draw.rect(self.slika, pygame.Color(175, 175, 175), (
                        xCigle + j * (duzinaCigle + duzinaRazmaka), yCigle + i * (visinaCigle + visinaRazmaka),
                        duzinaCigle,
                        visinaCigle), 3)
        self.mask = pygame.mask.from_surface(self.slika)
        skorTekst = fontSkor.render('{0: >10}'.format(str(round(self.skor, -2))), True, (255, 255, 255))
        self.slika.blit(skorTekst, (770, 0))
        for i in range(brojZivota):
            self.slika.blit(slikaSrce, (razmakZivota + i * (razmakZivota + duzinaZivota), razmakZivota))

    def stampaj(self):
        ekran.blit(self.slika, (0, 0))

    def loop(self):
        self.stampaj()


class Upitnik(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.slika = slikaUpitnik
        self.mask = pygame.mask.from_surface(self.slika)
        self.brzinaY = brzinaUpitnika

    def stampaj(self):
        ekran.blit(self.slika, (self.x, self.y))

    def loop(self, tick):
        self.y += self.brzinaY * tick
        if self.y > ekranY + 20:
            return False
        self.stampaj()
        return True


def crtaj():
    praviEkran.blit(pygame.transform.scale(ekran, (sirina, visina)), (0, 0))
    pygame.display.flip()


def gameover(skor, zivoti, pobeda):
    skor += vrednostZivota * zivoti
    if pobeda:
        s = "POBEDA!"
    else:
        s = "PORAZ!!"
    porazTekst = fontVeliki.render(s, True, (255, 255, 255))
    tvojSkorTekst = fontMali.render("Tvoj rezultat je: ", True, (255, 255, 255))
    skorTekst = fontSkor.render('{0: >10}'.format(str(round(skor, -2))), True, (255, 255, 255))
    unesiImeTekst = fontMali.render("Unesi svoje ime: ", True, (255, 255, 255))
    ekran.blit(pozadina, (0, 0))
    ekran.blit(porazTekst, (250, 50))
    ekran.blit(tvojSkorTekst, (250, 220))
    ekran.blit(skorTekst, (500, 230))
    ekran.blit(unesiImeTekst, (350, 350))
    crtaj()
    ime = ""
    unos = True
    while unos:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    unos = False
                elif event.key == pygame.K_BACKSPACE or len(ime) > 15:
                    ekran.blit(pozadina, (0, 0))
                    ekran.blit(porazTekst, (250, 50))
                    ekran.blit(tvojSkorTekst, (250, 220))
                    ekran.blit(skorTekst, (500, 230))
                    ekran.blit(unesiImeTekst, (350, 350))
                    ime = ime[:-1]
                    ekran.blit(fontMali.render(ime, True, (255, 255, 255)), (350, 400))
                    crtaj()
                else:
                    ekran.blit(pozadina, (0, 0))
                    ekran.blit(porazTekst, (250, 50))
                    ekran.blit(tvojSkorTekst, (250, 220))
                    ekran.blit(skorTekst, (500, 230))
                    ekran.blit(unesiImeTekst, (350, 350))
                    ime += event.unicode
                    ekran.blit(fontMali.render(ime, True, (255, 255, 255)), (350, 400))
                    crtaj()
    dodajRang(ime, skor)


def dodajRang(ime, skor):
    with open("ranglista.txt", "r") as f:
        fread = f.read()
        if len(fread) < 2:
            lista = []
        else:
            lista = eval(fread)
    lista.append([ime, skor])
    lista.sort(key=lambda x: x[1], reverse=True)
    with open("ranglista.txt", "w") as f:
        f.write(str(lista))


def ranglista():
    with open("ranglista.txt", "r") as f:
        fread = f.read()
        if len(fread) < 2:
            lista = []
        else:
            lista = eval(fread)
    naslovTekst = fontMali.render("RANG LISTA", True, (255, 255, 255))
    ekran.blit(pozadina, (0, 0))
    ekran.blit(naslovTekst, (370, 0))
    for i in range(min(15, len(lista))):
        if i == 0:
            boja = (212, 175, 55)
        elif i == 1:
            boja = (192, 192, 192)
        elif i == 2:
            boja = (205, 127, 50)
        else:
            boja = (255, 255, 255)
        ekran.blit(fontMali.render((" " if i < 9 else "") + str(i + 1) + ". " + lista[i][0], True, boja),
                   (220, 40 + i * 35))
        ekran.blit(fontSkor.render('{0: >10}'.format(str(round(lista[i][1], -2))), True, boja), (550, 50 + i * 35))
    for i in range(len(lista), 15):
        if i == 0:
            boja = (212, 175, 55)
        elif i == 1:
            boja = (192, 192, 192)
        elif i == 2:
            boja = (205, 127, 50)
        else:
            boja = (255, 255, 255)
        ekran.blit(fontMali.render((" " if i < 9 else "") + str(i + 1) + ". ", True, boja),
                   (220, 40 + i * 35))
    crtaj()
    unos = True
    while unos:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                unos = False


def runda():
    global brzinaPalice, precnikLoptice, duzinaPalice, brzinaLoptice, powerup
    powerup = 0
    brojZivota = broj_Zivota
    palica = Palica()
    loptica = Loptica()
    sat = pygame.time.Clock()
    cigle = Cigle()
    levoPritisnuto = False
    desnoPritisnuto = False
    upitnici = []
    while True:
        tik = sat.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            elif event.type == pygame.KEYDOWN:
                if not loptica.ispaljena and event.key == pygame.K_UP:
                    loptica.ispali()
                elif not loptica.ispaljena and event.key == pygame.K_l:
                    ranglista()
                elif event.key == pygame.K_LEFT:
                    levoPritisnuto = True
                    palica.brzina = -brzinaPalice
                elif event.key == pygame.K_RIGHT:
                    desnoPritisnuto = True
                    palica.brzina = brzinaPalice
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    levoPritisnuto = False
                elif event.key == pygame.K_RIGHT:
                    desnoPritisnuto = False
                if not (levoPritisnuto or desnoPritisnuto):
                    palica.brzina = 0
        ekran.blit(pozadina, (0, 0))
        palica.loop(tik)
        if not loptica.loop(tik, palica.x):
            del loptica
            brojZivota -= 1
            cigle.azuriraj(brojZivota)
            if brojZivota <= 0:
                gameover(cigle.skor, 0, False)
                break
            else:
                loptica = Loptica()
        if cigle.brojCigli <= 0:
            gameover(cigle.skor, brojZivota, True)
            break
        # provera sudara loptice i palice
        kolizija = palica.mask.overlap(loptica.mask, (loptica.x - palica.x, loptica.y - yPalice))
        if kolizija is not None:
            loptica.odbijOdPalice(kolizija[0])
        # provera sudara loptice i cigala
        kolizija = cigle.mask.overlap(loptica.mask, (loptica.x, loptica.y))
        if kolizija is not None:
            jSudara = (kolizija[0] - xCigle) // (duzinaCigle + duzinaRazmaka)
            iSudara = (kolizija[1] - yCigle) // (visinaCigle + visinaRazmaka)
            cigle.cigle[iSudara][jSudara] = 0
            cigle.brojCigli -= 1
            cigle.skor += int(skorCigla * (skorCinilac ** loptica.streak))
            loptica.streak += 1
            cigle.azuriraj(brojZivota)
            gore = (iSudara + 1) * (visinaCigle + visinaRazmaka) - visinaRazmaka - kolizija[1] + yCigle
            dole = kolizija[1] - yCigle - iSudara * (visinaCigle + visinaRazmaka)
            levo = kolizija[0] - xCigle - jSudara * (duzinaCigle + duzinaRazmaka)
            desno = (jSudara + 1) * (duzinaCigle + duzinaRazmaka) - duzinaRazmaka - kolizija[0] + xCigle
            mini = min([gore, dole, levo, desno])

            if mini == gore or mini == dole:
                loptica.brzinaY = -loptica.brzinaY
            else:
                loptica.brzinaX = -loptica.brzinaX

            randBroj = random() / ucestalostUpitnika
            if randBroj <= 1:
                noviUp = Upitnik(xCigle + jSudara * (duzinaCigle + duzinaRazmaka) + (duzinaCigle - precnikUpitnika) / 2,
                                 yCigle + iSudara * (visinaCigle + visinaRazmaka))
                upitnici.append(noviUp)
        # upitnici
        for i in range(len(upitnici)):
            upitnici[i].loop(tik)
            kolizija = palica.mask.overlap(upitnici[i].mask, (upitnici[i].x - palica.x, upitnici[i].y - yPalice))
            if kolizija is not None:
                del upitnici[i]
                if powerup == 7:
                    loptica.brzinaX /= ubrzanjeLoptice
                    loptica.brzinaY /= ubrzanjeLoptice
                    brzinaLoptice /= ubrzanjeLoptice
                    loptica.promeniBoju((10, 10, 255), (0, 0, 150))
                elif powerup == 8:
                    loptica.brzinaX /= usporenjeLoptice
                    loptica.brzinaY /= usporenjeLoptice
                    brzinaLoptice /= usporenjeLoptice
                    loptica.promeniBoju((10, 10, 255), (0, 0, 150))
                elif powerup > 0:
                    palica.slika = palica.slikaNormal
                    loptica.slika = loptica.slikaNormal
                    precnikLoptice = precnikNormalLoptice
                    duzinaPalice = duzinaNormalPalice
                    brzinaPalice = normalBrzinaPalice
                    palica.promeniBoju((10, 255, 10), (0, 150, 0))

                randBroj = random()*8.3
                powerup = randBroj//1+1
                if randBroj <= 1:
                    print("uvecanje palice")
                    palica.slika = palica.slikaLong
                    duzinaPalice = duzinaLongPalice
                elif randBroj <= 2:
                    print("umanjenje palice")
                    palica.slika = palica.slikaShort
                    duzinaPalice = duzinaShortPalice
                elif randBroj <= 3:
                    print("ubrzanje palice")
                    brzinaPalice *= (1 + promenaBrzinePalice)
                    palica.promeniBoju((255, 255, 10), (150, 150, 0))
                elif randBroj <= 4:
                    print("usporenje palice")
                    brzinaPalice *= (1 - promenaBrzinePalice)
                    palica.promeniBoju((255, 10, 10), (150, 0, 0))
                elif randBroj <= 5:
                    print("uvecanje loptice")
                    loptica.slika = loptica.slikaBig
                    precnikLoptice = precnikBigLoptice
                elif randBroj <= 6:
                    print("umanjenje loptice")
                    loptica.slika = loptica.slikaSmall
                    precnikLoptice = precnikSmallLoptice
                elif randBroj <= 7:
                    print("ubrzanje loptice")
                    loptica.brzinaX *= ubrzanjeLoptice
                    loptica.brzinaY *= ubrzanjeLoptice
                    brzinaLoptice *= ubrzanjeLoptice
                    loptica.promeniBoju((255, 255, 10), (150, 150, 0))
                elif randBroj <= 8:
                    print("usporenje loptice")
                    loptica.brzinaX *= usporenjeLoptice
                    loptica.brzinaY *= usporenjeLoptice
                    brzinaLoptice *= usporenjeLoptice
                    loptica.promeniBoju((255, 10, 10), (150, 0, 0))
                else:
                    print("dodatni zivot")
                    powerup = 0
                    brojZivota += 1
                if powerup != 0:
                    pwTimer = pygame.time.get_ticks()
                palica.mask = pygame.mask.from_surface(palica.slika)
                loptica.mask = pygame.mask.from_surface(loptica.slika)
                break
        if powerup != 0 and pygame.time.get_ticks()-pwTimer > trajanjeUpitnika:
            if powerup == 7:
                loptica.brzinaX /= ubrzanjeLoptice
                loptica.brzinaY /= ubrzanjeLoptice
                brzinaLoptice /= ubrzanjeLoptice
                loptica.promeniBoju((10, 10, 255), (0, 0, 150))
            elif powerup == 8:
                loptica.brzinaX /= usporenjeLoptice
                loptica.brzinaY /= usporenjeLoptice
                brzinaLoptice /= usporenjeLoptice
                loptica.promeniBoju((10, 10, 255), (0, 0, 150))
            elif powerup > 0:
                palica.slika = palica.slikaNormal
                loptica.slika = loptica.slikaNormal
                precnikLoptice = precnikNormalLoptice
                duzinaPalice = duzinaNormalPalice
                brzinaPalice = normalBrzinaPalice
                palica.promeniBoju((10, 255, 10), (0, 150, 0))
            palica.mask = pygame.mask.from_surface(palica.slika)
            loptica.mask = pygame.mask.from_surface(loptica.slika)
            powerup = 0
        cigle.loop()
        crtaj()
    return True


if __name__ == '__main__':
    while True:
        if not runda():
            break
        powerup = 0
        brzinaPalice = normalBrzinaPalice
        duzinaPalice = duzinaNormalPalice
        ranglista()
