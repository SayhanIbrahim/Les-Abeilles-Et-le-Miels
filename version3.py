import pandas as pd
from random import shuffle, choice
import copy
import random
import sys
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from openpyxl import Workbook

# sys.setrecursionlimit(10 ** 9)
numbebe = 10
cordinatlist = []
abeillelist = []
lengthlist = []
gennnlist = []
mutasyoncontrollist = []
fitnesavrdict = {}
countmutasyon = [0]


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
    while generation < 25000:
        if generation == 0:
            namelist = namegenerator(100, generation)
            createAbeille(namelist, generation)
            createRootAbeille()
            lenRootAbeille()
            avrfitnessdict(generation)
        else:
            namelist = namegenerator(numbebe, generation)
            createAbeille(namelist, generation)
            crossover(generation)
            # if generation % 20 == 0:
            mutasyonLenghtlist(generation)
            selection()
            avrfitnessdict(generation)
        generation += 1
        print(generation)
    finish()


def avrfitnessdict(generation):
    poplengthlist = sorted(lengthlist)
    poplengthlist = poplengthlist[:100]
    popavr = sum(poplengthlist) / 100
    fitnesavrdict[generation] = popavr
    if generation > 1000 and fitnesavrdict[generation - 500] == popavr:
        finish()


def namegenerator(num, generation):
    if generation != 0:
        num = 2 * num
    namelist = []
    for i in range(num):
        name = f"abeille {generation} {i}"
        namelist.append(name)
    return namelist


def createAbeille(namelist, generation):
    x = len(namelist)
    for i in range(x):
        name = Abeille()
        setattr(name, 'name', namelist[i])
        abeillelist.append(name)


def createRootAbeille():
    for i in range(100):
        x = [i for i in range(len(cordinatlist))]
        shuffle(x)
        setattr(abeillelist[i], 'gen', x)


def selection():
    poplengthlist = sorted(lengthlist)
    for i in range(numbebe*2):
        indis = lengthlist.index(poplengthlist.pop())
        del abeillelist[indis]
        length = lengthlist[indis]
        lengthlist.remove(length)


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
        if i == 0:
            plotrootabeille(0)
        else:
            continue


def crossover(generation):
    x = sorted(lengthlist)
    x = x[0:100]
    count = 0
    for i in range(numbebe):
        indis3 = 100 + 2 * i
        indis4 = indis3 + 1
        y = x[count]
        z = x[count + 1]
        indis1 = lengthlist.index(y)
        indis2 = lengthlist.index(z)
        genlistbebe = chainfinder(indis1, indis2)
        genbebe1 = genlistbebe[0]
        genbebe2 = genlistbebe[1]
        setattr(abeillelist[indis3], 'gen', genbebe1)
        setattr(abeillelist[indis4], 'gen', genbebe2)
        root1 = abeillelist[indis3].gen
        root2 = abeillelist[indis4].gen
        lenght1 = round(lenghtroot(root1), 3)
        lenght2 = round(lenghtroot(root2), 3)
        lengthlist.append(lenght1)
        lengthlist.append(lenght2)
        setattr(abeillelist[indis3], 'lenght', lenght1)
        setattr(abeillelist[indis4], 'lenght', lenght2)
        count += 2


def chainfinder(indis1, indis2):
    gen1 = abeillelist[indis1].gen
    gen2 = abeillelist[indis2].gen
    numlist = list(range(len(cordinatlist)))
    chainelist = []
    while len(numlist) > 0:
        chaine = []
        num = choice(numlist)
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
    if len(chainelist) < 2 or gen1 == gen2:
        gen3 = list(reversed(gen1))
        return [gen3, gen1]
    chaine = random.choice(chainelist)
    chane1 = copy.deepcopy(chaine)
    genbebe1 = gencrossover(chane1, indis1)
    chane2 = copy.deepcopy(chaine)
    genbebe2 = gencrossover1(chane2, indis2)
    return [genbebe1, genbebe2]


def mutasyonLenghtlist(generation):
    x = sorted(lengthlist)
    for i in range(numbebe*2):
        indis = lengthlist.index(x[-i])
    for i in range(numbebe*2):
        indis = lengthlist.index(x[-i])
        mutasyon(indis, generation)


def mutasyon(indis, generation):
    # gen = []
    # if generation > 21 and fitnesavrdict[generation - 20] == fitnesavrdict[generation - 1]:
    #     liste2 = random.sample(range(len(cordinatlist)), 5)
    #     gen = gencrossover(liste2, indis)
    # else:
    liste2 = random.sample(range(len(cordinatlist)), 2)
    gen = gencrossover(liste2, indis)
    setattr(abeillelist[indis], 'gen', gen)
    root = abeillelist[indis].gen
    lenght = round(lenghtroot(root), 3)
    lengthlist.remove(lengthlist[indis])
    lengthlist.insert(indis, lenght)
    setattr(abeillelist[indis], 'lenght', lenght)


def gencrossover2(indis):
    num1 = 0
    num2 = 0
    gen = abeillelist[indis].gen
    num = choice(range(3, 6))
    boelen = True
    while boelen == True:
        liste = random.sample(range(len(cordinatlist) - num), 2)
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
    gen = list(abeillelist[indis].gen)
    name = abeillelist[indis].name
    lenght = abeillelist[indis].lenght
    # for i in range(2):
    #     if i == 0:
    #         gen = genpremier
    #         name = 'abeille 0 0'
    #         lenght = genpremierlength
    #     else:
    #         continue
    fig, ax = plt.subplots()
    fig.suptitle(f'name: {name} --- length: {lenght}')
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


def writeexel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Abeilles et Fleurs"
    ws.append(['name', 'lenght', 'gen'])
    for i in range(len(abeillelist)):
        genlist = []
        name = abeillelist[i].name
        lenght = abeillelist[i].lenght
        gen = list(abeillelist[i].gen)
        for j in gen:
            num = str(j)
            genlist.append(num)
        genom = ', '.join(genlist)
        ws.append([name, lenght,  genom])
    ws1 = wb.create_sheet("Generation")
    ws1.append(['Distance average of generations'])
    for i in range(len(fitnesavrdict)):
        average = fitnesavrdict[i]
        ws1.append([average])
    wb.save("Abeilles et Fleurs.xlsx")


def finish():
    poplengthlist = sorted(lengthlist)
    poplengthlist = poplengthlist[:100]
    popavr = sum(poplengthlist) / 100
    print('length: ', popavr)
    x = sorted(lengthlist)
    indis1 = lengthlist.index(x[0])
    print(abeillelist[indis1].name)
    plotpopulatinFitness()
    plotrootabeille(-1)
    writeexel()
    print(len(lengthlist))
    exit()


CoordiateListPlants()
generationg()
