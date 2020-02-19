
process get_valid_names {

  input:
    file x

  output:
    file "*"

  script:
    """
    python3 $baseDir/scripts/valid_names.py -i $x
    """
}

process json2graph {
  //publishDir "$baseDir/results",  mode: "copy"

  input:
    file x

  output:
    file "${x.baseName}.graph_output.graph"

  script:
    """
    python3 $baseDir/scripts/graphDating/GraphDating.py -i $x -if json -go ${x.baseName}.graph
    """
}


process json2graph_without_hydrogen {
  //publishDir "$baseDir/results",  mode: "copy"

  input:
    file x

  output:
    file "${x.baseName}.graph_output.graph"

  script:
    """
    python3 $baseDir/scripts/graphDating/GraphDating.py -i "${x}" -nh -if json -go ${x.baseName}.graph
    """
}


process remove_redundant_edges {
  //publishDir "$baseDir/results",  mode: "copy"

  input:
    file x
  
  output:
    file "${x.baseName}.graph"
  
  script:
    """
    python3 $baseDir/scripts/remove_redundant_edges.py -i $x -o ${x.baseName}.graph
    """
}


process graphDating_align {
  publishDir "$baseDir/results",  mode: "copy"

  input:
    file x
    each y
  
  output:
    file "*_result_*.graph"

  script:
    """
    python3 $baseDir/scripts/graphDating/GraphDating.py -i $x -ga $y -sgo result.graph -sub
    """
}


process multiVitamin_align {
  input:
    file x
  
  output:
    file "output.graph"
  
  script:
    """
    multiVitamin -i $x -a subVF2
    """
}

process graphDating_visualise {
  
  input:
    file x
    val y1
    val y2
    val y3

  output:
  
  script:
    """
    python3 $baseDir/scripts/graphDating/GraphDating.py -i $x -n "$y1" "$y2" "$y3"
    """
}