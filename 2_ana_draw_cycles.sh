for f in */aaout/*_cycles.txt; do
  echo "filename => $f"
  filedir=$(dirname $f)
  echo "dirname => $filedir"
  prename=$(basename $f .txt)
  echo "prefix => $prename"
  ampliconname=$(basename $f _cycles.txt)
  echo "amplicon => $ampliconname"

  resout=${filedir}/cyclevizout
  mkdir $resout
  python /data/home/pengli_data/aa/CycleViz/convert_cycles_file.py -o $resout -c $f -g ${filedir}/${ampliconname}_graph.txt 
  cv_cycles=${resout}/${prename}.txt.cv_cycles.txt
  mv ${resout}/cycles.txt $cv_cycles
  wait
  cids=( $( cat $cv_cycles | grep "Cycle=" | cut -d ";" -f 1 | cut -d "=" -f 2) )
  for ii in "${cids[@]}"; do
    echo "    This is cycle $ii"
    python /data/home/pengli_data/aa/CycleViz/CycleViz.py --cycles_file $cv_cycles --cycle $ii --sname ${cv_cycles}.${ii}
    echo "    This is cycle ${ii}, linear representation"
    python /data/home/pengli_data/aa/CycleViz/LinearViz.py --cycles_file $cv_cycles --path $ii --sname ${cv_cycles}.${ii}
  done
  echo "=== NEXT >>>"
  #break
done

echo "***** Done *****"
