import argparse
import pubchempy as pcp

def get_arguments():
    parser=argparse.ArgumentParser(usage="compares to graphs")
    parser.add_argument("-a","--graphA", metavar="gA", default="NONE", type=str, help="input graph a")
    parser.add_argument("-b","--graphB", metavar="gB", default="NONE", type=str, help="input graph b")

    return parser.parse_args()



def comparison(graph1, graph2):
    g1=graph1.get_name()
    g2=graph2.get_name()
    a='h_bond_donor_count'
    b='h_bond_acceptor_count'
    c='rotatable_bond_count'
    d='xlogp'

    args = [a,b,c,d]

    c_1 = pcp.Compound.from_cid(g1)
    #c_1 = pcp.get_compounds(g1, 'name')
    p_1 = c_1.to_dict(properties=args)

    c_2 = pcp.Compound.from_cid(g2)
    #c_2 = pcp.get_compounds(g2, 'name')
    p_2 = c_2.to_dict(properties=args)

    euclidean_dist = ( (p_1[d] - p_2[d])**2 + (p_1[a] - p_2[a])**2 + (p_1[b] - p_2[b])**2 + (p_1[c] - p_2[c])**2)**(1/2)
    return float(euclidean_dist)

if __name__ == "__main__":
    a = get_arguments()
    ed = comparison(a.graphA,a.graphB)
    print(ed)

print("comparison")
