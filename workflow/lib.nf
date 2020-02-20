
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
    python3 $baseDir/scripts/graphDating/GraphDating.py -i ${x} -nh -if json -go ${x.baseName}.graph
    """
}


process graphDating_align {
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
    path "results"
  
  script:
    """
    multiVitamin -ri $x -a subVF2
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


process load_substrates {

  input:
  
  output:
    path "EC_*/*.json"
  
  script:
    """
    python3 $baseDir/scripts/ECtoJSONloader.py
    """
}


process get_nice_names {

  input:
    file x

  output:
    file "*"

  script:
    """
    python3 $baseDir/scripts/valid_names.py -i $x
    """
}