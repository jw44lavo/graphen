import argparse
import itertools



def get_arguments():
    parser = argparse.ArgumentParser(usage="script to filter assembled contigs by length")
    parser.add_argument("-i", "--input",        metavar="", default=[],     type = str, help= "path to input file")
    parser.add_argument("-o", "--output",       metavar="", default=[],     type = str, help= "path to output file for contigs >= length ")
    
    return parser.parse_args()

def main():

    a = get_arguments()

    input_file = a.input
    output_file = a.output

    with open(input_file, "r") as f:
        count_newline = 0
        count_line = 0
        result = ""

        for line in f:
            count_line += 1 

            if count_newline < 2:
                result += line

            if line == "\n":
                count_newline += 1

            if count_newline == 2:
                                
                if line.split(";")[0] == "\n":
                    continue

                else:
                    x, y, z = line.split(";")[0], line.split(";")[1], line.split(";")[2]

                    result += line

                    a = next(f).split(";")
                    if a[0] == y and a[1] == x and a[2] == z:
                        continue

        
    with open(output_file, "w") as o:
        o.write(result)

if __name__ == "__main__":
    
    try:
        main()

    except IOError:
        raise Exception("\n \n ups, something failed tremendously... good luck finding the problem \n")

