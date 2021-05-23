'''
Created by hl17490, does genetic algorithms using one point, flib bit and tournament, through these three it runs a steady
state, individuals are called children in this program.
'''
import random as r
import timeit
import copy
import sys
sys.setrecursionlimit(9**9)# This is set to max, and frankly, if I could raise it more, I would.
start = timeit.default_timer()
gen = [361700864190383365,5,100,200] # This is the starting generation, feel free to fiddle, but you must start with at least two, as it must sexually reproduce
randgen = True # If you enable this, it'll create a random generation between randmin and randmax, overwriting "gen"
randmin = 1
randmax = 15
forceregen = False # This will overwrite the generation if your runtime hits a certain limit, as defined by forceregentime
forceregentime = 5# This is how long it will wait before overwriting the generation, I have it set to 3, but on slower processors you might want to increase this, I tested it with a R7 3700x for refrence.
# as it cannot asexually reproduce. They are converted into binary before it runs, and if running Max1 they are pushed to 100 bit

counttarget = 10000000000000 # If doing count, this is the goalpost
maxonetarget = 100 # One's out of 100, the higher this number the longer your runtime will be.
knapsacktarget = 535 # This is the size of the knapsack
bins = [10,75,100,177] # Any value between 1 and 255 will work, it's an 8 bit system


children = 1000 # What size do you want the generation to be?
difficulty = 10# How many children survive the tournament


mutationchance = 5 # 1 in x chance
childgrowth = True # Can a bitflip add a bit?//This is automatically disabled if running Max1
shrinkage = True # Can a bitflip remove a bit?//This is automatically disabled if running Max1
childgrowthmutation = 2 # 1 in x chance
breeding = True # Do they breed? If not they do asexual reproduction, much like aphids


goal = "Knapsack" # "Max1" to do maximise ones, "Knapsack" to do the knapsack problem, and "Count" to count to the target variable, "NBin" for N Bin problem

'''
Optimal settings for each test, testing data and deeper explanation can be found within Optimisationrecords.xlsx:

max1: [Randgen:True,Randmin:1,Randmax:15,Forceregen=False,Forceregentime = 10,Counttarget:10000000000000,maxonetarget: 100,
knapsacktarget:535, bins:[10,75,100,177],children:1000,difficulty:10,mutationchance:125,childgrowth:False,Shrinkage:False,
Childgrowthmutation:3,Breeding:True] average runtime: 2.596

knapsack: [Randgen:True,Randmin:1,Randmax:15,Forceregen=False,Forceregentime = 10,Counttarget:10000000000000,maxonetarget: 100,
knapsacktarget:535, bins:[10,75,100,177],children:1000,difficulty:10,mutationchance:5,childgrowth:True,Shrinkage:False,
Childgrowthmutation:2,Breeding:True] average runtime: 0.06

NBin: [Randgen:True,Randmin:1,Randmax:15,Forceregen=True,Forceregentime = 10,Counttarget:10000000000000,maxonetarget: 100,
knapsacktarget:535, bins:[10,75,100,177],children:1000,difficulty:5,mutationchance:25,childgrowth:True,Shrinkage:True,
Childgrowthmutation:5,Breeding:False] average runtime: 0.984

'''

def fitness(value,goal):
    if goal=="Count":
        intval = int(value,2)
        fitval = (intval/counttarget)
        # print("floater",fitval)
        # fitval = "{:.9f}".format(fitval)
        # onefloat = float(1)
        if fitval>=1:
            print("This child: ",value," has achieved the goal of counting to: ",counttarget," or greater")
            print("With the integer: ",int(value,2))
            stop = timeit.default_timer()
            print("Time was:", stop - start)
            sys.exit(0)
        return fitval


    if goal=="Max1":

        splitval = split(value)
        fitval=0
        for x in splitval:
            if x=="1":
                fitval+=1
        if fitval>=maxonetarget:
            print("This child: ",value," has achieved the goal of getting :",maxonetarget," ones")
            stop = timeit.default_timer()
            print("Time was:", stop - start)
            sys.exit(0)

        return fitval

    if goal=="Knapsack":
        intvalue=0
        try:
            intvalue = int(value,2)
        except:
            pass

        if intvalue==0:
            return 0


        if knapsacktarget>intvalue:
            smolfit = intvalue/knapsacktarget
            return smolfit

        if knapsacktarget<intvalue:
            bigfit = knapsacktarget/intvalue
            return bigfit

        if knapsacktarget==intvalue:
            print("This child: ",value," has achieved the goal of filling the knapsack of size: ",knapsacktarget," with the integer:",intvalue)
            stop = timeit.default_timer()
            print("Time was:", stop - start)
            sys.exit(0)

    if goal=="NBin":
        totalbins = len(bins)
        totfit = 0
        fitness = 0

        fitvalues = []
        intvalues = []

        for x in range(0,totalbins):
            if x==0:
                a = 0
                b = 8
            if x>=1:
                a = x*8
                b = (x+1)*8

            childchunk = value[a:b]
            try:
                intchildchunk = int(childchunk, 2)
            except:
                intchildchunk = 0


            intvalues.append(intchildchunk)
            thisbin = bins[x]

            if thisbin >= intchildchunk:
                fitness = intchildchunk / thisbin


            if thisbin < intchildchunk:
                fitness = thisbin / intchildchunk

            fitvalues.append(copy.copy(fitness))


        for x in fitvalues:
            totfit+=x

        # Len counts from 1, not 0, hence the -1 so it matches the number of b
        totfit = totfit/totalbins


        if totfit==1:
            print("This child: ",value," has achieved the goal of filling the bins: ",bins)
            print("With these values:",intvalues)
            stop = timeit.default_timer()
            print("Time was:", stop - start)
            sys.exit(0)

        return totfit

    if goal !="NBin" or "Count" or "Knapsack" or "Max1":
        print(goal," is an Invalid goal")
        sys.exit(0)

def split(value):
    return [bit for bit in value]

def tournament(gen):
    global goal
    max = 0
    newgen = []
    count = 0
    clonegen = copy.copy(gen)

    for x in gen:
        strongchild = ""
        Achild = clonegen[count]
        Bchildindex = r.randint(1,(len(gen)-1))
        Bchild = clonegen[Bchildindex]

        Afitness = fitness(Achild,goal)
        Bfitness = fitness(Bchild,goal)

        if Afitness>Bfitness:
            strongchild = Achild
            if (len(newgen) < 10):
                newgen.append(Achild)

        if Bfitness>=Afitness:
            strongchild = Bchild
            if (len(newgen)<10):
                newgen.append(Bchild)


        if (len(newgen)==difficulty):
            c = 0
            sfit = fitness(strongchild,goal)
            for y in newgen:
                yfit = fitness(y,goal)
                if sfit>yfit:
                    newgen[c] = copy.copy(strongchild)
                    break
                c+=1
        count += 1
    return newgen


def flipbit(gen):
    newgen = []
    counter = 0
    global mutationchance

    for x in gen:
        child = gen[counter]
        bit_child = copy.copy(child)
        bit_child = split(bit_child)
        newchild = ""
        for y in bit_child:
            mutation = r.randint(1,mutationchance)
            if mutation==1:
                if y=="1":
                    newchild+="0"
                if y=="0":
                    newchild+="1"
                if childgrowth and (goal!="Max1"):
                    growthmutation = r.randint(1,childgrowthmutation)
                    if growthmutation==1:
                        flip = r.randint(0,1)
                        newchild += str(flip)
                    if (shrinkage==True) and growthmutation==2:
                        newchild = newchild[:-1]
            else:
                newchild+=y


        newgen.append(newchild)

        counter+=1
    return newgen

def asexual(gen):
    ngen = copy.copy(gen)
    while len(ngen)<children:
        for x in gen:
            ngen.append(x)

    while (len(ngen) > children):
        ngen.remove(-1)
    if (len(ngen) == children):
        return ngen



def onepoint(gen):
    newgen = copy.copy(gen)

    full = False
    while (full==False):
        xx = r.randint(0, (len(gen)-1))
        xy = r.randint(0,(len(gen)-1))

        mother = gen[xx]
        father = gen[xy]

        bitmum = copy.copy(mother)
        bitdad = copy.copy(father)

        son = ""
        daughter = ""
        dadlen = len(bitdad)
        mumlen = len(bitmum)
        try:
            if dadlen<=mumlen:
                crossoverpoint = r.randint(1,(dadlen-1))
                son +=(bitdad[:crossoverpoint])
                son +=(bitmum[crossoverpoint:])
                daughter += (bitdad[crossoverpoint:])
                daughter += (bitdad[:crossoverpoint])

                # son = int(son,2)
                # daughter = int(daughter,2)

                newgen.append(son)
                newgen.append(daughter)

            elif(dadlen>mumlen):
                crossoverpoint = r.randint(1,(mumlen-1))
                son +=(bitmum[:crossoverpoint])
                son +=(bitdad[crossoverpoint:])
                daughter +=(bitmum[crossoverpoint:])
                daughter +=(bitdad[:crossoverpoint])

                # son = int(son, 2)
                # daughter = int(daughter, 2)

                newgen.append(son)
                newgen.append(daughter)
        except:
            newgen.append(father)
            newgen.append(mother)

        while(len(newgen)>children):
            newgen.remove(-1)
        if (len(newgen)==children):
            return newgen

evolutioncounter = 0
def evolve(gen):
    x = True
    while x:
        global evolutioncounter
        global forceregentime

        gen = tournament(gen)

        if breeding:
            gen = onepoint(gen)
        else:
            gen = asexual(gen)

        gen = flipbit(gen)
        evolutioncounter += 1
        checktime = timeit.default_timer()

        if (forceregentime%checktime==forceregentime) and forceregen==True:
            forceregentime = forceregentime+forceregentime
            print("Excessive evolution, randomising")
            gen = genrandgen()




bgen = []

def genrandgen():
        rgen = []
        for x in range(0, children):
            rgen.append(r.randint(randmin, randmax))
        rgen = binaryizer(rgen)
        if goal=="NBin":
            return NBinformat(rgen)
        if goal=="Max1":
            return Max1format(rgen)
        return rgen

# This turns your generation into strings representing binary values
def binaryizer(gen):
    cgen = []
    for x in gen:
        cgen.append(format(x,'b'))
    return cgen

# These just format your generation to work with certain tasks.
def NBinformat(bgen):
    c = 0
    targetlen = (len(bins)*8)
    for x in bgen:
        while len(x)<targetlen:
            x+="0"
        bgen[c]=x
        c+=1
    return bgen

def Max1format(bgen):
    c = 0
    for x in bgen:
        while len(x) < 100:
            x += "0"
        bgen[c] = x
        c += 1
    return bgen
print("Processing")
if randgen:
    gen = genrandgen()
else:
    gen = binaryizer(gen)

if goal=="Max1":
    gen = Max1format(gen)

if goal=="NBin":
    print("This can take some time")
    gen = NBinformat(gen)

if goal=="":
    pass

evolve(gen)

