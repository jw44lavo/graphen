nextflow.preview.dsl=2

include "./lib.nf"



workflow {

    log.info "############################"
    
    main:

        json = Channel.fromPath(params.json)

//      HYDROGEN DECISION

        if (params.without_hydrogen == "false"){
            graph = get_nice_names(json2graph(json))
        }
        else if (params.without_hydrogen == "true"){
            graph = get_nice_names(json2graph_without_hydrogen(json))
        }
        else {
            log.info "no information about hydrogen given - see 'nextflow.config'"
        }



//      ALIGNMENT TYPE DECISION

        if (params.alignment_type == "matching_based"){
            alignment_type = "mb"
        }
        else if (params.alignment_type == "bron_kerbosch"){
            alignment_type = "bk"
        }
        else {
            log.info "no alignment type given - see 'nextflow.config'"

        }

//      ALIGNMENT

        if (params.program_type == "graphDating"){
            alignment = graphDating_align(graph.collect(), alignment_type)
        }
        else if (params.program_type == "multiVitamin"){
            alignment = multiVitamin_align(graph.collect())
        }
        else if (params.program_type == "nothing"){
            log.info "no alignment wanted"
        }
        else {
            log.info "no program type given - see 'nextflow.config' "
        }

//      VISUALISATION

        if (params.visualisation == "true" && params.alignment_type == "all"){
            log.info "can not visualise all alignments at once"
        }
        else if (params.visualisation == "true" && params.alignment_type != "all"){
            graphDating_visualise(alignment, params.neo4j_http, params.neo4j_user, params.neo4j_password)
        }
        else if (params.visualisation == "false"){
            log.info "no visualisaiton wanted"
        }
        else {
            log.info "no information about visualisation given - see 'nextflow.config' "
        }
     

    log.info "############################"
    

    publish:
        graph to: "${params.publish_graphs}", mode: "copy"

        alignment to: "${params.publish_alignments}", mode: "copy"     

}