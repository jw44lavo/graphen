import argparse


def get_arguments():
    parser = argparse.ArgumentParser(usage="remove redundant edges from graph file")
    parser.add_argument("-i", "--input",        metavar="FILE", default=[],     type = str, help= "path to input file")
    parser.add_argument("-o", "--output",       metavar="", default=[],     type = str, help= "path to output file for contigs >= length ")
    
    return parser.parse_args()

def main():

    a = get_arguments()

    input_file = a.input
    output_file = a.output

    list_edges = []
    
    print()
    print(input_file)
    for file in input_file:
        
        print()
        print(file)
        file_name = file.split(".")[1]
        with open(file, "r") as f:
            result = ""
    
            for line in f:
    
                if len(line.split(";")) < 3:
                    result += line
                
                if len(line.split(";")) == 3:
                    string = line.split(";")
                    list_edges.append([string[0], string[1], string[2].rstrip("\n")])
    
        for i in list_edges:
            j = [i[1], i[0], i[2]]
    
            if j in list_edges:
                index = (list_edges.index(j))
                list_edges.pop(index)
            
            else:
                continue
    
        for i in list_edges:
            result += str(i[0])+";"+str(i[1])+";"+str(i[2])+"\n"
        
        with open(output_file + file_name + ".graph", "w") as o:
            o.write(result)
        

if __name__ == "__main__":
    
    try:
        main()

    except IOError:
        raise Exception("\n \n ups, something failed tremendously... good luck finding the problem \n")

