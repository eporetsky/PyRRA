#!/usr/bin/env Rscript
# Run R rankMatrix with specified parameters and save output
library(RobustRankAggreg)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: run_r_parameterized.R <dataset> <full> [N]")
}

dataset <- args[1]
full <- as.logical(args[2])
N <- NULL
if (length(args) >= 3 && args[3] != "None") {
  N <- as.integer(args[3])
}

# Load data based on dataset
if (dataset == "letters") {
  glist <- list(
    L1 = c("b", "c", "d", "a"),
    L2 = c("h", "g", "f", "e", "d", "c", "b", "a", "j", "i"),
    L3 = c("m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b")
  )
} else if (dataset == "cellCycleKO") {
  # Load from longform CSV
  df <- read.csv("export_cellCycleKO_longform.csv", stringsAsFactors = FALSE)
  glist <- split(df$Gene, df$List)
  # Ensure proper ordering within each list
  glist <- lapply(glist, function(x) {
    idx <- match(x, df[df$List == names(glist)[1], "Gene"])
    x[order(df[df$List == names(glist)[1], "Rank"][idx])]
  })
  # Actually, simpler approach:
  glist <- lapply(split(df, df$List), function(subdf) {
    subdf <- subdf[order(subdf$Rank), ]
    subdf$Gene
  })
} else {
  stop(paste("Unknown dataset:", dataset))
}

# Run rankMatrix with parameters
if (is.null(N)) {
  result <- rankMatrix(glist = glist, full = full)
} else {
  result <- rankMatrix(glist = glist, N = N, full = full)
}

# Save output
write.csv(result, "temp_r_output.csv", row.names = TRUE)

