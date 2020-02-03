import argparse
from itertools import islice



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
                for line in islice(f, 0, None, 2):
                    result += line

    with open(output_file, "w") as o:
        o.write(result)


if __name__ == "__main__":
    
    try:
        main()

    except IOError:
        raise Exception("\n \n ups, something failed tremendously... good luck finding the problem \n")

