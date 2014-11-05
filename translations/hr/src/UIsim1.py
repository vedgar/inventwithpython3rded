# Reversi (Othello)

import random
import sys

def ispiši(ploča):
    # Ispisuje ploču. Ne vraća ništa.
    vodoravna = '  +---+---+---+---+---+---+---+---+'
    uspravne  = '  |   |   |   |   |   |   |   |   |'

    print(      '    1   2   3   4   5   6   7   8')
    print(vodoravna)
    for y in range(8):
        print(uspravne)
        print(y+1, end=' ')
        for x in range(8):
            print('| {}'.format(ploča[x][y]), end=' ')
        print('|')
        print(uspravne)
        print(vodoravna)


def isprazni(ploča):
    # Ispražnjuje ploču, osim originalne početne pozicije.
    for x in range(8):
        for y in range(8):
            ploča[x][y] = ' '

    # Početna pozicija:
    ploča[3][3] = 'X'
    ploča[3][4] = 'O'
    ploča[4][3] = 'O'
    ploča[4][4] = 'X'


def nova_ploča():
    # Stvara novu, praznu ploču kao strukturu podataka.
    ploča = []
    for i in range(8):
        ploča.append([' '] * 8)

    return ploča


def potez_valja(ploča, znak, xpoč, ypoč):
    # Vraća False ako igračev potez na mjesto xpoč, ypoč ne valja.
    # Inače vraća listu mjesta koja bi igrač osvojio kad bi tu igrao.
    if not na_ploči(xpoč, ypoč) or ploča[xpoč][ypoč] != ' ':
        return False

    ploča[xpoč][ypoč] = znak # privremeno postavi znak na ploču

    if znak == 'X':
        protuznak = 'O'
    else:
        protuznak = 'X'

    preokrenuti = []
    for xsmjer, ysmjer in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xpoč, ypoč
        x += xsmjer # prvi korak u tom smjeru
        y += ysmjer # prvi korak u tom smjeru
        if na_ploči(x, y) and ploča[x][y] == protuznak:
            # Do našeg mjesta postoji protivnički znak
            x += xsmjer
            y += ysmjer
            if not na_ploči(x, y):
                continue
            while ploča[x][y] == protuznak:
                x += xsmjer
                y += ysmjer
                if not na_ploči(x, y): # izađi iz while petlje, nastavi for petlju
                    break
            if not na_ploči(x, y):
                continue
            if ploča[x][y] == znak:
                # Treba preokrenuti neke znakove. Idi natrag do početnog položaja, pamteći sve položaje putem.
                while True:
                    x -= xsmjer
                    y -= ysmjer
                    if (x, y) == (xpoč, ypoč):
                        break
                    preokrenuti.append([x, y])

    ploča[xpoč][ypoč] = ' ' # vrati prazno mjesto
    if not preokrenuti: # Ako nema preokrenutih, potez ne valja.
        return False
    return preokrenuti


def na_ploči(x, y):
    # Vraća True ako koordinate leže na ploči.
    return 0 <= x <= 7 and 0 <= y <= 7


def ploča_s_mogućim_potezima(ploča, znak):
    # Vraća novu ploču s mogućim potezima igrača (znak) označenima točkom.
    nova_ploča = kopiraj(ploča)

    for x, y in dobri_potezi(nova_ploča, znak):
        nova_ploča[x][y] = '.'
    return nova_ploča


def dobri_potezi(ploča, znak):
    # Vraća listu [x, y] listi - valjanih poteza igrača (znak) na ploči.
    popis_dobrih_poteza = []

    for x in range(8):
        for y in range(8):
            if potez_valja(ploča, znak, x, y):
                popis_dobrih_poteza.append([x, y])
    return popis_dobrih_poteza


def boduj(ploča):
    # Odredi bodove brojeći znakove. Vraća rječnik s ključevima 'X' i 'O'.
    x_bodovi = 0
    o_bodovi = 0
    for x in range(8):
        for y in range(8):
            if ploča[x][y] == 'X':
                x_bodovi += 1
            if ploča[x][y] == 'O':
                o_bodovi += 1
    return {'X':x_bodovi, 'O':o_bodovi}


def odabir_znakova():
    # Neka igrač odabere koji znak želi biti.
    # Vraća listu [znak igrača, znak računala].
    znak = ''
    while znak not in ('X', 'O'):
        print('Želiš li biti X ili O?')
        znak = input().upper()

    # prvi znak u listi pripada igraču, drugi računalu
    if znak == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def tko_će_prvi():
    # Slučajno odaberi tko ima prvi potez.
    if random.randint(0, 1) == 0:
        return 'računalo'
    else:
        return 'igrač'


def ponovo():
    # Vraća True ili False ovisno o tome želi li igrač ponovo igrati.
    print('Želiš li novu igru? (da ili ne)')
    return input().lower().startswith('d')


def učini_potez(ploča, znak, xpoč, ypoč):
    # Stavi znak na ploču na mjesto xpoč, ypoč, te preokreni protivnikove znakove.
    # Vraća True ili False ovisno o tome je li potez valjan.
    preokrenuti = potez_valja(ploča, znak, xpoč, ypoč)

    if not preokrenuti:
        return False

    ploča[xpoč][ypoč] = znak
    for x, y in preokrenuti:
        ploča[x][y] = znak
    return True


def kopiraj(ploča):
    # Napravi i vrati duplikat ploče.
    kopija = nova_ploča()

    for x in range(8):
        for y in range(8):
            kopija[x][y] = ploča[x][y]

    return kopija


def u_kutu(x, y):
    # Vraća True ako je pozicija u jednom od 4 kuta.
    return {x, y} <= {0, 7}


def potez_igrača(ploča, znak_igrača):
    # Neka igrač unese svoj potez.
    # Vraća potez [x, y], ili 'savjet', ili 'izlaz'.
    znamenke_1_do_8 = set('1 2 3 4 5 6 7 8'.split())
    while True:
        print('Unesi potez, ili "izlaz" za prekid igre,\n ili "savjet" za uključivanje/isključivanje savjeta.')
        potez = input().lower()
        if potez == 'izlaz':
            return 'izlaz'
        if potez == 'savjet':
            return 'savjet'

        if len(potez) == 2 and set(move) <= znamenke_1_do_8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if not potez_valja(ploča, igračev_znak, x, y):
                continue
            else:
                break
        else:
            print('To nije dobar potez. Unesi x znamenku (1-8) pa y znamenku (1-8).')
            print('Recimo, 81 će biti gornji desni kut.')

    return [x, y]


def potez_računala(ploča, znak_računala):
    # Ako je zadana ploča i znak kojim računalo igra, odredi kamo igrati
    # i vrati taj potez kao [x, y] listu.
    mogući_potezi = dobri_potezi(ploča, znak_računala)

    # slučajno promiješaj moguće poteze
    random.shuffle(mogući_potezi)

    # uvijek igraj u kut ako je moguće
    for x, y in mogući_potezi:
        if u_kutu(x, y):
            return [x, y]

    # idi kroz sve moguće poteze i zapamti onaj koji daje najviše bodova
    najbolji_rezultat = -1
    for x, y in mogući_potezi:
        kopija = kopiraj(ploča)
        učini_potez(kopija, znak_računala, x, y)
        rezultat = boduj(kopija)[znak_računala]
        if rezultat > najbolji_rezultat:
            najbolji_potez = [x, y]
            najbolji_rezultat = rezultat
    return najbolji_potez


def rezultat(znak_igrača, znak_računala):
    # Ispisuje trenutni rezultat
    bodovi = boduj(glavna_ploča)
    print('Imaš {} bodova. Računalo ima {} bodova.'.format(bodovi[znak_igrača], bodovi[znak_računala]))



print('Dobrodošao u Reversi!')

while True:
    # Resetiraj ploču i igru.
    glavna_ploča = nova_ploča()
    isprazni(glavna_ploča)
    if tko_će_prvi() == 'igrač':
        na_redu = 'X'
    else:
        na_redu = 'O'
    print(na_redu, 'igra prvi.')

    while True:
         ispiši(glavna_ploča)
         bodovi = boduj(glavna_ploča)
         print('X ima {} bodova. O ima {} bodova.'.format(bodovi['X'], bodovi['O']))
         input('Pritisni Enter za nastavak.')

         if na_redu == 'X':
              # X-ov red.
              protuznak = 'O'
              x, y = potez_računala(glavna_ploča, 'X')
              učini_potez(glavna_ploča, 'X', x, y)
         else:
              # O-ov red.
              protuznak = 'X'
              x, y = potez_računala(glavna_ploča, 'O')
              učini_potez(glavna_ploča, 'O', x, y)

         if not dobri_potezi(glavna_ploča, protuznak):
              break
         else:
              na_redu = protuznak

    # Prikaz konačnog rezultata
    ispiši(glavna_ploča)
    bodovi = boduj(glavna_ploča)
    print('Konačni rezultat: X {} bodova, O {} bodova.'.format(bodovi['X'], bodovi['O']))

    if not ponovo():
         break
