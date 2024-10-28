#' E. coli Protein Classes
#'
#' A dataset containing protein classifications for E. coli, where each protein is categorized into one of two classes.
#'
#' @format A data frame with X rows and 1 variable:
#' \describe{
#'   \item{class}{Integer value representing the protein classification: -1 for one class and 1 for the other}
#' }
"ecoli_protein_classes"

#' E. coli Protein Sequences
#'
#' A dataset containing amino acid sequences for 352 proteins from _Escherichia coli_.
#'
#' @format An AAStringSet object of length 352:
#' \describe{
#'   \item{width}{The length of each protein sequence in amino acids}
#'   \item{seq}{The amino acid sequence of each protein}
#'   \item{names}{Unique identifiers for each protein sequence, in the format 511145.bXXXX}
#' }
#'
#' @details The dataset includes the full amino acid sequences of proteins, each identified by a unique code.
#' Sequence information can be used for further bioinformatics analysis, such as alignment or functional prediction.
"ecoli_proteins"


#' Hemoglobin Protein Sequences
#'
#' A data set containing amino acid sequences for hemoglobin proteins from different species.
#'
#' @format An AAStringSet object of length 3:
#' \describe{
#'   \item{width}{The length of each hemoglobin protein sequence in amino acids}
#'   \item{seq}{The amino acid sequence of each hemoglobin protein}
#'   \item{names}{Species identifiers for each protein sequence: "HBA_HUMAN" for human, "HBA_MOUSE" for mouse, and "HBAZ_CAPHI" for Capra hircus (goat)}
#' }
#'
#' @details The dataset includes the full amino acid sequences for hemoglobin proteins from human, mouse, and goat. These sequences can be used for comparative analysis or structural studies.
"hglobin"

#' Gene Expression Dataset
#'
#' A dataset containing gene expression levels for various samples.
#'
#' @format A data frame with 35,238 rows and 904 variables:
#' \describe{
#'   \item{genes}{Character vector of gene symbols (e.g., "A1BG", "A1CF", "A2M")}
#'   \item{GSMxxxxxxx}{Integer values representing expression levels of each gene in specific samples, with each column corresponding to a unique sample (e.g., "GSM742944", "GSM2326089")}
#' }
#'
#' @details This dataset provides gene expression counts for over 35,000 genes across 903 samples. The data can be used for various analyses, including differential expression and clustering.
"human_liver"

#' modENCODE DESeq2 Dataset
#'
#' A `DESeqDataSet` object containing RNA-seq count data for 14,869 genes across 9 samples, used for differential expression analysis.
#'
#' @format A `DESeqDataSet` object with:
#' \describe{
#'   \item{dim}{14869 genes (rows) and 9 samples (columns)}
#'   \item{assays}{List of 4 assays: `counts`, `mu`, `H`, and `cooks`}
#'   \item{rownames}{Identifiers for each gene (e.g., "FBgn0000003", "FBgn0000008")}
#'   \item{colnames}{Sample identifiers for each column (e.g., "SRX008026", "SRX008174")}
#'   \item{rowData}{Data on each gene, including 22 attributes like `baseMean`, `baseVar`, `deviance`, and `maxCooks`}
#'   \item{colData}{Metadata for each sample, including `sample.id`, `num.tech.reps`, `stage`, and `sizeFactor`}
#' }
#'
#' @details This dataset is used in differential expression analysis with DESeq2, with sample information stored in `colData` and gene information in `rowData`.
"modencode_dds"


#' Plastid Genomes Dataset
#'
#' A `DNAStringSet` object containing complete chloroplast genome sequences from different plant species.
#'
#' @format A `DNAStringSet` object with the following structure:
#' \describe{
#'   \item{pool}{Contains raw sequence data stored as a `SharedRaw_Pool` object}
#'   \item{ranges}{Contains information on each sequence, including:
#'     \describe{
#'       \item{NAMES}{Names of each sequence, including accession numbers and species (e.g., "NC_018523.1 Saccharina japonica chloroplast, complete genome")}
#'     }
#'   }
#'   \item{elementType}{Indicates the element type, "DNAString" for each sequence}
#' }
#'
#' @details The dataset includes chloroplast genome sequences for five species, each represented by a complete genome sequence in DNA format. Useful for comparative genomics and evolutionary studies.
"plastid_genomes"



