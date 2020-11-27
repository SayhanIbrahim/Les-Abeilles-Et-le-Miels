import pandas as pd
from random import shuffle, choice
import copy
import itertools
import random
import sys
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from openpyxl import Workbook

sys.setrecursionlimit(10 ** 9)

cordinatlist = []
abeillelist = []
lengthlist = []
gennnlist = []
fitnesavrdict = {}
bebenum = 10

wb = Workbook()
ws = wb.active
ws.title = "Abeilles et Fleurs"
ws.append(['name', 'lenght', 'gen'])
ws1 = wb.create_sheet("Generation")
ws1.append(['Generations Length Average'])


def CoordiateListPlants():
    global cordinatlist
    df = pd.read_excel(
        r'Champ de pissenlits et de sauge des pres.xlsx', engine='openpyxl')
    listx = df['x'].tolist()
    listy = df['y'].tolist()
    cordinatlist = dict(zip(range(len(listx)), list(zip(listx, listy))))


class Abeille(object):
    name = 'abeille'


def generationg():
    generation = 0

    while generation < 1500:
        if generation == 0:
            namelist = namegenerator(100, generation)
            createAbeille(namelist)
            createRootAbeille()
            lenRootAbeille()
            mutasyonLenghtlist()
            avrfitnessdict(generation)
        else:
            namelist = namegenerator(bebenum, generation)
            createAbeille(namelist)
            crossover(generation)
            mutasyonLenghtlist()
            avrfitnessdict(generation)
            selection()
        generation += 1
        print(generation)
    finish()


def avrfitnessdict(generation):
    poplengthlist = sorted(lengthlist)
    poplengthlist = poplengthlist[:100]
    popavr = sum(poplengthlist) / 100
    fitnesavrdict[generation] = popavr
    ws1.append([popavr])
    if generation > 80 and fitnesavrdict[generation - 30] == popavr:
        finish()


def namegenerator(num, generation):
    namelist = []
    for i in range(num):
        name = f"abeille {generation} {i}"
        namelist.append(name)
    return namelist


def createAbeille(namelist):
    for i in range(len(namelist)):
        name = Abeille()
        setattr(name, 'name', namelist[i])
        abeillelist.append(name)


def createRootAbeille():
    for i in range(100):
        x = [i for i in range(len(cordinatlist))]
        shuffle(x)
        setattr(abeillelist[i], 'gen', x)
        setattr(abeillelist[i], 'mutasyonNum', 0)


def selection():
    poplengthlist = sorted(lengthlist)
    print('len(abeillelist)', len(abeillelist))
    print('len(lengthlist)', len(lengthlist))
    i = 0
    for i in range(bebenum):
        indis = lengthlist.index(poplengthlist.pop())
        del abeillelist[indis]
        length = lengthlist[indis]
        lengthlist.remove(length)
    print('len(abeillelist)', len(abeillelist))
    print('len(lengthlist)', len(lengthlist))


def lenghtroot(root):
    entre = (500, 500)
    lenght = 0
    for j in range(len(cordinatlist)+1):
        if j == 0:
            position1 = entre
            position2 = root[j]
            position2 = cordinatlist[position2]
            lenght = lengthcalculater(position1, position2) + lenght
        elif j == len(cordinatlist):
            position1 = root[j - 1]
            position1 = cordinatlist[position1]
            position2 = entre
            lenght = lengthcalculater(position1, position2) + lenght
        else:
            position1 = root[j - 1]
            position1 = cordinatlist[position1]
            position2 = root[j]
            position2 = cordinatlist[position2]
            lenght = lengthcalculater(position1, position2) + lenght
    return (lenght)


def lengthcalculater(position1, position2):
    lenght = ((position2[0] - position1[0]) ** 2 +
              (position2[1] - position1[1]) ** 2) ** (1 / 2)
    return lenght


def lenRootAbeille():
    for i in range(100):
        root = abeillelist[i].gen
        lenght = round(lenghtroot(root), 3)
        setattr(abeillelist[i], 'lenght', lenght)
        lengthlist.append(lenght)
        writeexcel(i)


def crossover(generation):
    x = sorted(lengthlist)
    x = x[0:100]
    count = 0
    for i in range(bebenum):
        indis3 = 100 + i
        y = x[count]
        z = x[-(count + 1)]
        indis1 = lengthlist.index(y)
        indis2 = lengthlist.index(z)
        genbebe = chainfinder(indis1, indis2)
        setattr(abeillelist[indis3], 'gen', genbebe)
        num = mutasyonNumChoise(indis1, indis2)
        setattr(abeillelist[indis3], 'mutasyonNum', num)
        root = abeillelist[indis3].gen
        lenght = round(lenghtroot(root), 3)
        lengthlist.append(lenght)
        setattr(abeillelist[indis3], 'lenght', lenght)
        writeexcel(indis3)
        count += 1


def chainfinder(indis1, indis2):
    gen1 = abeillelist[indis1].gen
    gen2 = abeillelist[indis2].gen
    leng1 = abeillelist[indis1].lenght
    numlist = list(range(len(cordinatlist)))
    chainelist = []
    while len(numlist) > 0:
        num = choice(numlist)
        chaine = []
        if gen1[num] == gen2[num]:
            chaine.append(gen1[num])
            try:
                numlist.remove(num)
                num = choice(numlist)
            except:
                continue
        else:
            start = gen1[num]
            try:
                numlist.remove(num)
            except:
                continue
            chaine.append(start)
            while start != gen2[num]:
                a = gen2[num]
                chaine.append(a)
                num = gen1.index(a)
                try:
                    numlist.remove(num)
                except:
                    continue
        chainelist.append(chaine)
    if len(chainelist) < 2:
        gen3 = list(reversed(gen1))
        return gen3
    chaine = random.choice(chainelist)
    chane1 = copy.deepcopy(chaine)
    gen = gencrossover(chane1, indis1)
    leng = lenghtroot(gen)
    if leng < leng1:
        return (gen)
    chane2 = copy.deepcopy(chaine)
    gen = gencrossover1(chane2, indis2)
    leng = lenghtroot(gen)
    if leng < leng1:
        return (gen)
    gen = mutasyon(indis1)
    return gen


def mutasyonLenghtlist():
    x = sorted(lengthlist)
    for i in range(100):
        y = x[i]
        indis = lengthlist.index(y)
        mutsayonNumAugmentattion(indis)


def mutsayonNumAugmentattion(indis):
    ajt = random.choice(range(0, 5))
    num = abeillelist[indis].mutasyonNum + ajt
    mutsayonDecision(num, indis)


def mutsayonDecision(num, indis):
    if num >= 20:
        num = num - 10
        setattr(abeillelist[indis], 'mutasyonNum', num)
        mutasyon(indis)
    else:
        setattr(abeillelist[indis], 'mutasyonNum', num)


def mutasyonNumChoise(indis1, indis2):
    num1 = abeillelist[indis1].mutasyonNum
    num2 = abeillelist[indis2].mutasyonNum
    if num1 > num2:
        return num1
    else:
        return num2


def mutasyonSet(count):
    liste = [i for i in range(len(cordinatlist))]
    liste2 = list(itertools.permutations(liste, r=count + 2))
    return (liste2)


def mutasyon(indis):
    boelian = True
    gen = abeillelist[indis].gen
    if gen in gennnlist:
        return (gen)
    leng1 = abeillelist[indis].lenght
    count = 0
    liste2 = mutasyonSet(count)
    while boelian == True:
        if len(liste2) == 0:
            boelian = True
            count = count + 1
            if count == 2:
                boelian = False
                gen = abeillelist[indis].gen
                gennnlist.append(gen)
                return (gen)
        else:
            chaine = list(random.choice(liste2))
            liste2.remove(tuple(chaine))
            gen = gencrossover(chaine, indis)
            leng = lenghtroot(gen)
            if leng < leng1:
                boelian = False
                setattr(abeillelist[indis], 'gen', gen)
                root = abeillelist[indis].gen
                lenght = round(lenghtroot(root), 3)
                lengthlist.remove(lengthlist[indis])
                lengthlist.insert(indis, lenght)
                setattr(abeillelist[indis], 'lenght', lenght)
                return (gen)
            else:
                boelian = True


def gencrossover2(indis):
    boelian = True
    leng1 = abeillelist[indis].lenght
    gen = abeillelist[indis].gen
    count = 0
    while count < 2500 and boelian == True:
        num1 = 0
        num2 = 0
        num = choice(range(3, 9))
        boelen = True
        while boelen == True:
            liste = random.sample(range(50 - num), 2)
            liste2 = sorted(liste)
            num1 = liste2[0]
            num2 = liste2[1]
            if num2 - num1 > num:
                boelen = False
            else:
                boelen = True
        i = 0
        while i < num:
            genom1 = gen[num1 + i]
            genom2 = gen[num2 + i]
            gen.remove(genom1)
            gen.remove(genom2)
            gen.insert((num1 + i), genom2)
            gen.insert((num2 + i), genom1)
            i += 1
        leng = lenghtroot(gen)
        if leng < leng1:
            boelian = False
            print(gen)
            return (gen)
        count += 1
    return (gen)


def gencrossover(chaine, indis):
    gen1 = abeillelist[indis].gen
    genenfant = []
    for gen in gen1:
        if gen in chaine:
            indis = chaine.index(gen)
            if indis == len(chaine) - 1:
                genenfant.append(chaine[0])
            else:
                genenfant.append(chaine[indis + 1])
        else:
            genenfant.append(gen)
    return (genenfant)


def gencrossover1(chaine, indis):
    gen1 = abeillelist[indis].gen
    genenfant = []
    for gen in gen1:
        if gen in chaine:
            indis = chaine.index(gen)
            if indis == 0:
                genenfant.append(chaine[-1])
            else:
                genenfant.append(chaine[indis - 1])
        else:
            genenfant.append(gen)
    return (genenfant)


def plotrootabeille(indis):
    gen = abeillelist[indis].gen
    name = abeillelist[indis].name
    lenght = abeillelist[indis].lenght
    fig, ax = plt.subplots()
    fig.suptitle(f'name: {name} --- lenght: {lenght}')
    Path = mpath.Path
    path_data = []
    for i in range(len(gen)):
        element1 = gen[i]
        element = (1, cordinatlist[element1])
        path_data.append(element)
    path_data.append((1, (500, 500)))
    path_data.insert(0, (1, (500, 500)))
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    x, y = zip(*path.vertices)
    line, = ax.plot(x, y, 'go-')
    ax.grid()
    ax.axis('equal')
    plt.plot([500], [500], 'o', color='m')
    plt.show()


def plotpopulatinFitness():
    names = list(fitnesavrdict.keys())
    values = list(fitnesavrdict.values())
    fig, axs = plt.subplots()
    axs.plot(names, values)
    fig.suptitle('Generation Length Average')
    plt.show()


def writeexcel(indis):
    genlist = []
    name = abeillelist[indis].name
    lenght = abeillelist[indis].lenght
    gen = list(abeillelist[indis].gen)
    for j in gen:
        num = str(j)
        genlist.append(num)
    genom = ', '.join(genlist)
    ws.append([name, lenght, genom])


def finish():
    poplengthlist = sorted(lengthlist)
    poplengthlist = poplengthlist[:100]
    popavr = sum(poplengthlist) / 100
    fitness = round(86400 / popavr, 3)
    print(popavr, fitness)
    x = sorted(lengthlist)
    indis1 = lengthlist.index(x[0])
    print(abeillelist[indis1].gen)
    plotpopulatinFitness()
    plotrootabeille(0)
    plotrootabeille(indis1)
    wb.save("Abeilles et Fleurs.xlsx")
    exit()


CoordiateListPlants()
generationg()
