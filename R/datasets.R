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
#'   \item{GSMxxxxx}{Numeric values representing expression levels for each sample. The dataset contains expression data from multiple samples labeled as 'GSM' followed by a unique identifier (e.g., GSM1067795, GSM1416804, etc.).}
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

#' Time Series SNP Data
#'
#' A dataset containing time series data for SNP frequencies over 400 days.
#'
#' @format A data frame with 400 rows and 3 variables:
#' \describe{
#'   \item{day}{Integer indicating the day of the observation}
#'   \item{snp}{Character string representing the SNP identifier}
#'   \item{frequency}{Numeric value representing the frequency of the SNP on the given day}
#' }
#'
#' @details This dataset is used to analyze the changes in SNP frequencies over time.
"ts_data"

#' Five Disease Data
#'
#' A dataset containing gene expression or related data across five diseases.
#'
#' @format A tibble with 2,406 rows and 5 variables:
#' \describe{
#'   \item{disease}{Character string representing the disease (e.g., "Alzheimers")}
#'   \item{a}{Numeric value representing a measurement related to the disease}
#'   \item{b}{Numeric value representing another measurement related to the disease}
#'   \item{c}{Numeric value representing a third measurement related to the disease}
#'   \item{gene}{Character string representing the gene associated with the observation}
#' }
#'
#' @details This dataset can be used for analyzing variations in gene measurements across different diseases.
"five_disease"

#' Example Metadata for Genomic Data
#'
#' A dataset containing example metadata for genomic data analysis, including details about cell lines and related attributes.
#'
#' @format A data frame with 1,829 rows and 22 variables:
#' \describe{
#'   \item{DepMap_ID}{Character string representing the unique identifier for each cell line.}
#'   \item{cell_line_name}{Character string representing the name of the cell line.}
#'   \item{stripped_cell_line_name}{Character string representing a simplified version of the cell line name.}
#'   \item{CCLE_Name}{Character string representing the CCLE name.}
#'   \item{alias}{Character string for alternative names for the cell line.}
#'   \item{COSMICID}{Integer representing the COSMIC ID.}
#'   \item{sex}{Character string indicating the sex of the cell line ("Male" or "Female").}
#'   \item{source}{Character string representing the source of the cell line (e.g., "ATCC").}
#'   \item{RRID}{Character string for the Research Resource Identifier.}
#'   \item{WTSI_Master_Cell_ID}{Integer representing the WTSI master cell ID.}
#'   \item{sample_collection_site}{Character string indicating the sample collection site.}
#'   \item{primary_or_metastasis}{Character string indicating if the sample is primary or metastatic.}
#'   \item{primary_disease}{Character string for the primary disease associated with the cell line.}
#'   \item{Subtype}{Character string for the subtype of the disease.}
#'   \item{age}{Numeric value indicating the age of the donor, if available.}
#'   \item{Sanger_Model_ID}{Character string for the Sanger model ID.}
#'   \item{depmap_public_comments}{Character string for any public comments about the cell line.}
#'   \item{lineage}{Character string indicating the lineage (e.g., "blood").}
#'   \item{lineage_subtype}{Character string for the lineage subtype.}
#'   \item{lineage_sub_subtype}{Character string for the sub-subtype of the lineage.}
#'   \item{lineage_molecular_subtype}{Character string for the molecular subtype within the lineage.}
#'   \item{culture_type}{Character string indicating the culture type (e.g., "Adherent", "Suspension").}
#' }
#' @details This dataset is used to illustrate how metadata can be used in genomic analysis, including characteristics of cell lines and their related information.
"metadata"
