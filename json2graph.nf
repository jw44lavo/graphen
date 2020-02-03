nextflow.preview.dsl=2


process parse {
  publishDir "/home/johann/OneDrive/Projects/projects/praktikum/commonplace/data/graph/", mode: "copy"

  input:
    file x

  output:
    file "${x.baseName}.graph_output.graph"

  script:
    """
    python3 ~/OneDrive/Projects/git/BestesRepository/GraphDating.py -i $x -if json -go ${x.baseName}.graph
    """
}


workflow {
    main:

        data = Channel.fromPath("/home/johann/OneDrive/Projects/projects/praktikum/commonplace/data/json/*")

        parse(data)

}