library(ape)
library(msa)
library(seqinr)

seqs <- readAAStringSet("/users/theodosiou/Desktop/datasets/ch3/hglobin.fa")
seqs

#multiple sequence alignment
alignment <-  msa(seqs, method="ClustalOmega")
alignment

alignment_seqinr <- msaConvert(alignment, type = "seqinr::alignment")
alignment_seqinr

distances <- seqinr::dist.alignment(alignment_seqinr, "identity")
distances

tree <- ape::nj(distances)
tree

plot(tree)


BiocManager::install("DECIPHER")
library(DECIPHER)  # Library for synteny and genome alignment analysis

names(seqs)
BiocManager::install("RSQLite")
#######
Seqs2DB(seqs, "XStringSet", "long_db", names(seqs))

synteny <- FindSynteny("long_db")
