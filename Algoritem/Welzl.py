import math
import random

#Točka je par (x,y), krog pa je trojček števil (središče x, središče y, polmer)
#vrne najmnajši krog, ki zajema vse dan točke
#VHOD: seznam točk npr.[(1,2),(-3.5,52)]
#IZHOD: trojček števil, ki predstavlja krog

#točko označimo s p - point, krog c-circle

#najprej definirajmo vse funkcije

#Vrne ploščino paralelegroama, ki ga določajao točke (x0,y0),(x1,y1) in (x2,y2)
def vektorski_produkt(p, q, r):
	return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

#vrne True, če je točka p v krogu c
#funkcija math.hypot(x,y) vrne evklidkso normo vektroja (x^2+y^2)^(0.5)
def je_v_krogu(c,p):
    return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2]

#funckija premer vrne krog, ki ga določata dve točki p0 in p1 torej je njuna razdalaja kar premer kroga
def premer(p0, p1):
    cx = (p0[0] + p1[0]) / 2.0
    cy = (p0[1] + p1[1]) / 2.0
    r = math.hypot(cx - p0[0], cy - p0[1])

    return (cx, cy, r)

#funkcija ocrtan krog vrne krog, ki ga določajo 3 točke oz. vrne trikotniku očratan krog
def ocrtan_krog(p0,p1,p2):
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
    oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
    ax -= ox;
    ay -= oy
    bx -= ox;
    by -= oy
    cx -= ox;
    cy -= oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - p0[0], y - p0[1])
    rb = math.hypot(x - p1[0], y - p1[1])
    rc = math.hypot(x - p2[0], y - p2[1])
    return (x, y, max(ra, rb, rc))

def sarus(matrika):
    "Vrne determinanto 3x3 matrike"
    vsota1 = matrika[0][0] * matrika[1][1] * matrika[2][2] + matrika[0][1] * matrika[1][2]*matrika[2][0] + matrika[0][2] * matrika[1][0]*matrika[2][1]
    vsota2 = matrika[2][0]*matrika[1][1]*matrika[0][2] + matrika[2][1]*matrika[1][2]*matrika[0][0] +matrika[2][2] * matrika[1][0]*matrika[0][1]
    return vsota1 - vsota2

def ocrtan_krog2(p0,p1,p2):
    "Algoritem iz Wikipedije: https://en.wikipedia.org/wiki/Circumscribed_circle"

    Ax,Ay = p0
    Bx,By = p1
    Cx,Cy = p2

    Sx = 0.5 * sarus([[Ax**2+Ay**2, Ay,1],[Bx**2+By**2,By,1],[Cx**2+Cy**2,Cy,1]])
    Sy = 0.5 * sarus([[Ax, Ax**2+Ay**2, 1],[Bx,Bx**2+By**2,1 ],[Cx,Cx**2+Cy**2,1 ]])
    a = sarus([[Ax,Ay,1],[Bx,By,1],[Cx,Cy,1]])
    b = sarus([[Ax,Ay,Ax**2+Ay**2],[Bx,By,Bx**2+By**2],[Cx,Cy,Cx**2+Cy**2]])

    if a == 0:
        return None
    else:
        return (Sx/a, Sy/a, ( b/a + (Sx**2+Sy**2)/(a**2) )**(0.5))



#Naslednje funkcije izračunaj krog, če poznamo sledeče # robnih točk

#poznamo dve robni točki p in q
def krog2(tocke, p, q):
    krog = premer(p,q)
    px, py = p
    qx, qy = q
    CCW = None
    CW = None
    #za vsako točko, ki ni v krogu dolčenem s p in q
    for r in tocke:
        if je_v_krogu(krog, r):
            continue
        vprod = vektorski_produkt(p,q,r)
        c = ocrtan_krog(p, q, r)

	if c is None:
            continue
        elif vprod > 0.0 and (CCW is None or vektorski_produkt(p,q,c) > vektorski_produkt(p,q,CCW)):
            CCW = c

        elif vprod< 0.0 and (CW is None or vektorski_produkt(p,q,c) < vektorski_produkt(p,q,CW)):
            CW = c
        #Izberemo kateri krog se vrne
    if CCW is None and CW is None:
        return krog
    elif CCW is None:
        return CW
    elif CW is None:
        return CCW
    else:
        return CCW if (CCW[2] <= CW[2]) else CW


#poznamo eno robno točko p
def krog1(tocke,p):
    c = (p[0],p[1],0.0)

    for (i,q) in enumerate(tocke):
        if not je_v_krogu(c,q):#tocke, ki niso v krogu
            if c[2] == 0.0:
                c = premer(p,q)
            else:
                c = krog2(tocke[:i+1],p,q) ##????????

    return c

#na zacetku ne poznmo robnih tock

def Welzl(tocke):
    #spremnimo v float in jih nakljucno razvrstimo
    tocke = [(float(x), float(y)) for (x, y) in tocke]
    random.shuffle(tocke)

    #iterativno dodajamo tocke in prepračunavamo krog
    c = None
    for (i,p) in enumerate(tocke):
        if c is None or not je_v_krogu(c,p):
            c = krog1(tocke[: i+1],p) ##??
    return c
