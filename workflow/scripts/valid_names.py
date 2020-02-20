import argparse


def get_arguments():
    parser = argparse.ArgumentParser(usage="remove redundant edges from graph file")
    parser.add_argument("-i", "--input",        metavar="FILE", default=[],     type = str, help= "path to input file")
    
    return parser.parse_args()

def main():

    a = get_arguments()

    input_file = a.input
    results = ""
    endung = ""

    with open(input_file) as f:
        for line in f:
            results += line

    output_file = input_file.split(".")[0]
    endung = input_file.split(".")[-1]

    output_file = output_file + "." + endung  
    
    with open(output_file, "w") as o:
        o.write(results)

if __name__ == "__main__":
    
    try:
        main()

    except IOError:
        raise Exception("\n \n ups, something failed tremendously... good luck finding the problem \n")

