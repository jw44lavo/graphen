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
    minis = ["+ TTP","TTP +","+ UTP","UTP +","+ ITP","ITP +","+ GTP","GTP +","+ CTP","CTP +","+ ADP","ADP +","CoA +","+ CoA","acetate +","+ acetate","+ H2O","H2O +", "+ ATP", "ATP +", "ATP","+ 2 H2O", "CO2", "+ NAD+", "NAD+ +"]
    for i in minis:
        string = string.replace(i, "")
    return string

################################################################
################################################################
https://github.com/Tschichen/MIGRAINE
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
    try:
        os.mkdir(f"{dir_path}/{dir_search}")
        dir_search=f"{dir_path}/{dir_search}"
    except:
        print("mkdir failed")
    return dir_search

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


def check_size_of_substrate(name, cutoff):
    counter=0
    try:
        p = pcp.get_cids(name, 'name', 'substance', list_return='flat')
    except:
        print("substrate not found..")
        return False
    if len(p) == 0:
        print("substrate not found..")
        return False
    c = pcp.Compound.from_cid(p[0])
    c = c.to_dict(properties=['atoms', 'bonds', 'inchi'])
    for atom in c['atoms']:
        if atom['element'] is not 'H':
            counter += 1
            if counter > cutoff:
                print("Strukture of Substrate too big")
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
                if "more" in str(first):
                    continue
                if len(str(first)) == 0:
                    continue
                substrates.append(first)
        except:
            continue
    try:
        counted = Counter(substrates)
        most_common = max(set(substrates), key=substrates.count)
    except:
        print("mcs doesnt WORK")
        return None, None
    return most_common, counted

def get_structure(code,cutoff,dir_search,BRENDA_PARSER):
    print("GET STRUCTURE FILES...")
    proteins = BRENDA_PARSER.get_proteins(code)
    substrate, counted = choose_substrate(proteins)
    #substrate = str(substrate).rstrip()
    if substrate == None:
        print("No suitable substrate found, skip..")
        return False
    for s in counted:
        print(str(counted[s]), " : \t", s )
    print("\nmost common: ", substrate)
    if substrate == "several substrates":
        print("\nProtein uses several substrates, skip it..")
        return False
    if substrate == "more":
        print("\nProtein uses several substrates, skip it..")
        return False
    if check_size_of_substrate(substrate,cutoff) == False:
        return False
    #file = (f'{dir_search}/{code}_{str(substrate).strip()}.json')
    file = (f'{dir_search}/{str(substrate).strip()}.json')

    try:
        pcp.download('JSON', file, substrate, 'name')
    except:
        print("substrate not found..")
        return False
    return True


def get_structure_files(list,anz,cutoff,dir_search,BRENDA_PARSER):
    enzymes = list
    result_list = []
    while len(result_list) < anz:
        if len(enzymes) == 0:
            return False
        sampling = random.choice(enzymes)
        enzymes.remove(sampling)
        print("\n\n",sampling)
        if get_structure(sampling,cutoff,dir_search,BRENDA_PARSER) == True:
            result_list.append(sampling)
    return True

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

    if get_structure_files(enzym_selection,anz,cutoff,dir_search,BRENDA_PARSER):
        print("SUCCESS: Structures found and downloaded")
    else:
        print("ERROR: Not enough processible structures available")

######################################################################

if __name__ == '__main__':
    main()
