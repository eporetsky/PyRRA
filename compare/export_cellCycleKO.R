#' Export cellCycleKO data for cross-language testing
library(RobustRankAggreg)
data(cellCycleKO)

# Save ranked lists as CSV (long-form: listname, gene, rank)
rank_lists <- cellCycleKO$gl
all_names <- unique(unlist(rank_lists))
rank_mat <- rankMatrix(rank_lists, N=cellCycleKO$N)

# Save rank matrix
write.csv(rank_mat, file="cellCycleKO_rank_matrix.csv")

# Save list of ranked elements as tidy long-form, with which list and rank (optional, can help cross-check)
long_form <- do.call(rbind, lapply(seq_along(rank_lists), function(i) {
  data.frame(List=paste0("L",i), Gene=rank_lists[[i]], Rank=seq_along(rank_lists[[i]]))
}))
write.csv(long_form, file="compare/export_cellCycleKO_longform.csv", row.names=FALSE)

# Save metadata (optional): N and reference gene set
meta <- list(N=cellCycleKO$N, ref=cellCycleKO$ref)
dput(meta, file="compare/export_cellCycleKO_meta.R")
