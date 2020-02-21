import argparse
import json
import random
import pubchempy as pcp
from brendapy import BrendaParser
from collections import Counter
import os
import shutil

################################################################
## Strings in list "minis" will be filtered in chemical equation
## Add '+' with whitespace at the beginning and the end

def remove_minis(string):
    minis = ["TTP","UTP","ITP","GTP","CTP","ADP","CoA","acetate","H2O", "ATP", "H2O", "CO2", "NAD+", "NADPH", "H2", "NAD(P)H", "H+", "O2", "NADH", "NADHX", "HCN"]
    string = string.split("+")
    new_string =[]

    for s in string:
        new_string.append(s.strip())

    for s in new_string:
        if s in minis:
            new_string.remove(s)
        if s.isdigit():
            new_string.remove(s)
        if s == "more":
            new_string.remove(s)
            
    if len(new_string) > 1:
        print("ERROR: several substrates, continue...")
        return None
    elif not new_string:
        return None
    else:
        return new_string[0]
"""
def remove_minis(string):
    minis = ["+ TTP","TTP +","+ UTP","UTP +","+ ITP","ITP +","+ GTP","GTP +","+ CTP","CTP +","+ ADP","ADP +","CoA +","+ CoA","acetate +","+ acetate","+ H2O","H2O +", "+ ATP", "ATP +", "ATP","+ 2 H2O", "CO2", "+ NAD+", "NAD+ +", "+ H2", "H2 +", "", ""]
    for i in minis:
        string = string.replace(i, "")
    return string
"""

################################################################
################################################################

def get_arguments():
    parser=argparse.ArgumentParser(usage="script to download json files from onlinedatabase of enzyme structures")
    parser.add_argument("-s","--subtree", metavar="EC", default="", type=str, help="coordinates of subtree as EC code")
    parser.add_argument("-n","--number", metavar="INT", default=10, type=int, help="number of json files to download")
    parser.add_argument("-c","--cutoff", metavar="INT", default=20, type=int, help="number of maximum Atoms in Structure (without H)")
    parser.add_argument("-o","--output", metavar="PATH", default="./", type=str, help="set output directory")

    return parser.parse_args()

def make_dir(ec, output):
    s = ec.split(".")
    dir_path= output  #os.path.dirname(os.path.realpath(__file__))
    dir_search="EC"
    for i in s:
        dir_search=f"{dir_search}_{i}"
    path = os.path.join(os.getcwd(),dir_path, dir_search)
    try:
        os.makedirs(path)
    except:
        print("mkdir failed")
    return path

def select(list, search):
    selection = []
    for ec in list:
        if str(ec).startswith(search):
            selection.append(ec)
    return selection

def new_enzyme_list(BRENDA_PARSER):
    el = []
    for ec in BRENDA_PARSER.keys():
        el.append(ec)
    return el

def check_for_char(string):
    for c in string:
        if c.isalpha():
            return False
    return True

def check_size_of_substrate(CID, cutoff):
    counter=0
    c = pcp.Compound.from_cid(CID)
    c = c.to_dict(properties=['atoms', 'bonds', 'inchi'])
    for atom in c['atoms']:
        if atom['element'] is not 'H':
            counter += 1
            if counter > cutoff:
                print("Structure of Substrate too big")
                return False
    return True

def choose_substrate(proteins):
    substrates=[]
    for i in proteins.values():
        #if i.organism == "Homo sapiens":
        try:
            for j in i.SP:
                line = j["data"].split("=")
                first = remove_minis(line[0])
                if first == None:
                    continue
                substrates.append(first)
        except:
            continue
    try:
        counted = Counter(substrates)
        most_common = max(set(substrates), key=substrates.count)
    except:
        print("no most common substrate found")
        return None, None
    return most_common, counted

def get_structure(code,cutoff,dir_search,BRENDA_PARSER):
    proteins = BRENDA_PARSER.get_proteins(code)
    substrate, counted = choose_substrate(proteins)

    if substrate == None:
        print("No suitable substrate found, skip..")
        return False
    #for s in counted:
        #print(str(counted[s]), " : \t", s )
    print("\nmost common: ", substrate)
    
    try:
        CID = pcp.get_cids(substrate, 'name', 'substance', list_return='flat')[0]
    except:
        print("CID not found..")
        return False
    
    if cutoff:
        if check_size_of_substrate(CID,cutoff) == False:
            return False

    file = (f'{dir_search}/{CID}.json')
    #file = (f'{dir_search}/{str(substrate).strip()}.json')
    try:
        pcp.download('JSON', file, CID, 'cid')
    except:
        return False
    return True


def get_structure_files(list,anz,cutoff,dir_search,BRENDA_PARSER):
    enzymes = list
    for e in enzymes:
        print("\n\n",e)
        if get_structure(e,cutoff,dir_search,BRENDA_PARSER) == True:
            print("Success, file loaded..")
        else:
            print("substrate not found..")
    return

######################################################################

def main():
    a = get_arguments()
    BRENDA_PARSER = BrendaParser()
    cutoff = a.cutoff
    anz = a.number
    search = a.subtree
    output = a.output

    dir_search = make_dir(search, output)
    enzyme_list = new_enzyme_list(BRENDA_PARSER)
    enzym_selection = select(enzyme_list, search)

    get_structure_files(enzym_selection,anz,cutoff,dir_search,BRENDA_PARSER)
    
    print("habe fertig!")


######################################################################

if __name__ == '__main__':
    main()
