import Welzl
import  math

def je_CCW(p, q, r):
    "Vrne TRUE, če gredo vektorji pq,qr v nasprotno smer urinega kazalca"
    assert p != q and q != r and p != r

    if Welzl.vektorski_produkt(p, q, r) >= 0:
        return True
    else:
        return False


def je_v_Polygonu(t, P):
    "Vrne True, če je točka t vsebovana v Polygonu P"

    # Predvidevamo, da je Polygon podan z zaporedjem točk v pozitivni smeri

    for i in range(len(P[:-1])):
        p, q = P[i], P[i + 1]
        if not je_CCW(p, q, t):
            return False  # je zunaj

    return True


def min_pravokotnik(P):
    "Vrne najmanjsi pravokotnik, ki vsebuje poygon P"

    X = []  # x-koordinate
    Y = []  # y-koordinate

    for x, y in P:
        X.append(x)
        Y.append(y)

    maxX = max(X)
    minX = min(X)
    maxY = max(Y)
    minY = min(Y)

    return (minX, maxX, minY, maxY)


from random import uniform

def randomTocke(n, P):
    "Vrne n-naključnih točk znotraj polygona P"

    tocke = []
    minX, maxX, minY, maxY = min_pravokotnik(P)

    while len(tocke) < n:
        (X, Y) = (uniform(minX, maxX), uniform(minY, maxY))
        p = (X, Y)
        if je_v_Polygonu(p, P):
            tocke.append(p)

    return tocke

def randomTockeKrog(n, c):
    "Vrne n-naključnih točk znotraj kroga c"

    tocke = []
    minX, maxX, minY, maxY = c[0] - c[2], c[0] + c[2], c[1] - c[2], c[1] + c[2]
    while len(tocke) < n:
        (X, Y) = (uniform(minX, maxX), uniform(minY, maxY))
        p = (X, Y)
        if Welzl.je_v_krogu(c, p):
            tocke.append(p)

    return tocke


def je_v_elipsi(e, p):
    "vrne True, če je točka p v elipsi e"
    F1x, F1y = e[0]  # 1.gorišče
    F2x, F2y = e[1]  # 2.gorišče

    if math.hypot(F1x - p[0], F1y - p[1]) + math.hypot(F2x - p[0], F2y - p[1]) <= e[2]:
        return True
    else:
        return False


def randomTockeElipsa(n, e):
    "Vrne n-naključnih točk znotraj elipse e s središčem v (0,0)"
    F1x, F1y = e[0]  # 1.gorišče
    F2x, F2y = e[1]  # 2.gorišče
    d = e[2]
    E = abs(F2x)

    b = (d ** 2 / 4 - E ** 2) ** (0.5)
    a = (E ** 2 + b ** 2) ** (0.5)

    tocke = []
    minX, maxX, minY, maxY = -a, a, -b, b

    while len(tocke) < n:
        (X, Y) = (uniform(minX, maxX), uniform(minY, maxY))
        p = (X, Y)
        if je_v_elipsi(e, p):
            tocke.append(p)

    return tocke


# Oblike ##################################################################
#Dolg_pravokotnik
Dolg_pravokotnik = [(-10000, -1), (10000, -1), (10000, 1), (-10000, 1)]


r = 50

# Pravokotnik
Pravokotnik = [(-r,-(math.pi* r)/4),(r,-(math.pi* r)/4),(r,(math.pi* r)/4),(-r,(math.pi* r)/4)] #ploščina pravokotnika enaka kot ploščina kroga
# Elipsa
Elipsa = [(-r, 0), (r, 0), 3*r]
# Kvadrat
Kvadrat = [(-r, -r), (r, -r), (r, r), (-r, r)]
# Trikotnik
Trikotnik = [(-r, -r), (r, -r), (0, r)]
# Krog
Krog = (0, 0, r)


# Eksperiment #####################################################################
oblike1 = [Pravokotnik, Kvadrat, Trikotnik]
imena = ["Pravokotnik", "Kvadrat", "Trikotnik"]

import time

def eksperiment(oblike):
    Slovar_casov = {}
    for (i, oblika) in enumerate(oblike):
        casi = []
        for n in (100, 1000,10000,100000):
            cas_n = []            
            for _ in range(100):
                tocke = randomTocke(n, oblika)
                to = time.time()
                Welzl.Welzl(tocke)
                t1 = time.time()
                cas_n.append(t1 - to)
            casi.append(sum(cas_n) / 100)

        Slovar_casov[imena[i]] = casi
    return Slovar_casov

def eksperiment_krog(c):
    casi = []
    for n in (100, 1000,10000,100000):
        cas_n = []        
        for _ in range(100):
            tocke = randomTockeKrog(n, c)
            to = time.time()
            Welzl.Welzl(tocke)
            t1 = time.time()
            cas_n.append(t1 - to)
        casi.append(sum(cas_n) / 100)
    Slovar_casov["Krog"] = casi
    return Slovar_casov

def eksperiment_elipsa(e):
    casi = []
    for n in (100, 1000,10000,100000):
        cas_n = []
        for _ in range(100):
            tocke = randomTockeElipsa(n, e)
            to = time.time()
            Welzl.Welzl(tocke)
            t1 = time.time()
            cas_n.append(t1 - to)
        casi.append(sum(cas_n) / 100)

    Slovar_casov["Elipsa"] = casi
    return Slovar_casov
