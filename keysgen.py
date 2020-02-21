from brendapy import BrendaParser
import argparse

def get_arguments():
    parser=argparse.ArgumentParser(usage="creates config-file for ECtoJSONloader. Example: python3 keysgen.py -c 20 -n 15")
    parser.add_argument("-n","--number", metavar="INT", default=10, type=int, help="number of json files to download")
    parser.add_argument("-c","--cutoff", metavar="INT", default=20, type=int, help="number of maximum Atoms in Structure (without H)")


    return parser.parse_args()

def main():
    BRENDA_PARSER = BrendaParser()
    numbers =[]
    
    a = get_arguments()
    cutoff = a.cutoff
    anz = a.number

    for ec in BRENDA_PARSER.keys():
        n = str(ec).split(".")
        if len(n)<4:
            continue
        new = f"{n[0]}.{n[1]}.{n[2]}"
        if new not in numbers:
            numbers.append(new)

    f = open("config.txt", "w")
    for i in numbers:
        f.write(f"{i}\t{cutoff}\t{anz}\n")
    f.close()


if __name__ == '__main__':
    main()
