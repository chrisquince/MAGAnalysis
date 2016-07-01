library(KEGGREST)
library(pathview)
library(KEGGgraph)


plot_cluster_pathways <- function(clusters, pathway, cluster_ko_table, suffix = "dummy"){
  path <- keggGet(pathway)
  mappg <- parseKGML(paste(pathway, ".xml", sep=""))
  elements <- unname(sapply(nodes(mappg), getDisplayName))
  ko_elements <- elements[grep("K", elements)]
  ko_elements <- ko_elements[-grep("\\.\\.\\.", ko_elements)]
  relevant_kos <- cluster_ko_table[clusters,, drop=F]
  names(relevant_kos) <- sub("ko.", "", names(relevant_kos))
  relevant_kos <- relevant_kos[, which(names(relevant_kos) %in% ko_elements)]
  relevant_kos <- relevant_kos[,colSums(relevant_kos) > 0  ]
  relevant_kos[row.names(relevant_kos) %in% c("C326", "C318", "C47") & relevant_kos > 0] <- -1
  pv.out <- pathview(gene.data = t(relevant_kos), cpd.data = NULL, pathway.id = pathway,species="ko", out.suffix = suffix)
  
}

cctable <- read.table("AD/ClusterKOR.csv", sep = ",", header=T, row.names = 1)
plot_cluster_pathways(c("C326", "C318", "C47","C202","C79","C265","C101"),"ko00330", cctable )
