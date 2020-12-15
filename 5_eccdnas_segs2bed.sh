
cut -d ',' -f 2 eccdnas_3_ana_out.txt | awk 'NR>1{print}' | tr ";;" '\n' | awk 'NF' | sed 's/[\+\-]$//' | awk '{gsub(/[:\-]/, "\t"); print}' > eccdna_segs_5.bed
