nextflow.preview.dsl=2

include "./lib.nf"
include remove_redundant_edges as remove_redundant_edges_1 from "./lib.nf"
include remove_redundant_edges as remove_redundant_edges_2 from "./lib.nf"


workflow {

    log.info "############################"
    
    main:

        //json = Channel.fromPath(params.json)

//      HYDROGEN DECISION
/*
        if (params.without_hydrogen == "false"){
            graph = json2graph(json)
        }
        else if (params.without_hydrogen == "true"){
            graph = json2graph_without_hydrogen(json)
        }
        else {
            log.info "no information about hydrogen given - see 'nextflow.config'"
        }
*/
//      ALIGNMENT TYPE DECISION
/*
        if (params.alignment_type == "matching_based"){
            alignment_type = "mb"
        }
        else if (params.alignment_type == "bron_kerbosch"){
            alignment_type = "bk"
        }
        else {
            log.info "no alignment type given - see 'nextflow.config'"

        }
*/
//      ALIGNMENT
/*
        if (params.program_type == "graphDating"){
            alignment = graphDating_align(graph.collect(), alignment_type)
        }
        else if (params.program_type == "multiVitamin"){
            remove_redundant_edges(graph)
            alignment = multiVitamin_align()
        }
        else if (params.program_type == "migrane"){
            remove_redundant_edges(graph)
            alignment = migrane_align()
        }
        else if (params.program_type == "all"){
            graphDating_align()
            remove_redundant_edges(graph)
            multiVitamin_align()
            migrane_align()
        }
        else {
            log.info "no program type given - see 'nextflow.config' "
        }
*/
//      VISUALISATION
/*
        if (params.visualisation == "true" && params.alignment_type == "all"){
            log.info "can not visualise all alignments at once"
        }
        else if (params.visualisation == "true" && params.alignment_type != "all"){
            graphDating_visualise(alignment, params.neo4j_http, params.neo4j_user, params.neo4j_password)
        }
        else {
            log.info "no information about visualisation given - see 'nextflow.config' "
        }
*/      
        get_json_from_brenda(params.ec_subtree, params.ec_cutoff, params.ec_number)
    //    json2graph(json)
    //    get_valid_names(json2graph.out)
    //   remove_redundant_edges(get_valid_names.out)

    log.info "############################"
    

    publish:

        //remove_redundant_edges.out to: "${params.publish}", mode: "copy"
        get_json_from_brenda.out to: "${params.publish}", mode: "copy"



}