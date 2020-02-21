import os
from os import listdir
import glob
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


path = f"{os.getcwd()}/alignments"

#dirs = glob.glob(str(path)+"/EC_5_3*")
dirs = glob.glob(str(path)+"/EC_*")

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))


files = []
for d in dirs:
    d = d + "/results"
    for f in os.listdir(d):
        if str(f).strip().endswith('.graph'):
            files.append(f"{d}/{str(f).strip()}")

results = {}
count = 0
for f in files:
    results[count] = []
    file = open(f, "r")
    nodes = []
    modus = False

    for line in file:
        if modus == True:
            nodes.append(line)
        if not line.strip():
            modus = not modus
            try:
                nodes.pop()
            except:
                continue
    file.close() 

    value = 0
    for n in nodes:
        code = n.split(";")[1].replace(" ","").strip()
        l = len(code)
        d = sum(c.isdigit() for c in code)
        v = 100 * d / l
        if v >= 100:
            value += 1
        results[count].append(v)
    ec = f.split("EC")[1].split("/")[0].replace("_",".")
    print("EC",ec[1:],"\t",len(code),"\t","|"*value)
    
    bins=[0,0,0,0,0,0,0,0,0,0]
    
    for i in results[count]:
        if i >= 100:
            bins[9]+=1
            continue
        if i >= 90:
            bins[8]+=1
            continue
        if i >= 80:
            bins[7]+=1
            continue
        if i >= 70:
            bins[6]+=1
            continue
        if i >= 60:
            bins[5]+=1
            continue
        if i >= 50:
            bins[4]+=1
            continue
        if i >= 40:
            bins[3]+=1
            continue
        if i >= 30:
            bins[2]+=1
            continue
        if i >= 20:
            bins[1]+=1
            continue
        if i >= 10:
            bins[0]+=1
            continue
    
    label=f"EC {ec[1:]}  -  {len(nodes)} nodes"
    
    fig= plt.figure(figsize=(6,2))
    y_pos = np.arange(len(bins))
    plt.bar(y_pos,bins)
    plt.xticks(y_pos, [10,20,30,40,50,60,70,80,90,100])
    plt.xlabel("Match in allen Graphen [%]")
    plt.ylabel('Anzahl der Graphen')
    plt.text(6, 16, label, style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.1, 'pad': 10})
    plt.axis([-0.5,10,0,20])
    try:
        os.mkdir("histos")
    except:
        print("mkdir failed")
    plt.savefig(f"histos/EC_{ec[1:]}.pdf")
    plt.close(fig)


"""
    f = open("toR.txt", "a")
    for i in results[count]:
        f.write(f"{str(i)}, ")
    f.write("\n")
    f.close()
    count+=1

pretty(results)
#print(results[0])

fig, axs = plt.subplots(len(results))

for r in results:
    x = results[r]
    num_bins = 10
    n, bins, patches = axs[r].hist(x, num_bins, facecolor='blue', alpha=0.5)
    axs[r].set_xlabel("xlabel")
    

    #('Match in allen Graphen [%]', axes=axs.all())
#plt.ylabel('Anzahl der Knoten')
#plt.axis([0,100,0,20])
#plt.grid(True)
plt.show()
"""
