
import os, sys, re
import pybedtools

def getRefGeneBed(txtFile='/data/home/pengli_data/aa/CycleViz/refGene_hg19.txt'):
  geneNames = []
  with open(txtFile, 'r') as fh:
    for line in fh:
      line = line.strip()
      eles = line.split('\t')
      chrName = eles[2]
      pstart = eles[4]
      pend = eles[5]
      pstrand = eles[3]
      refGeneName = eles[12]
      if not (refGeneName.startswith('LOC') or refGeneName.startswith('LINC') or refGeneName.startswith('MIR')):
        geneNames.append('{}\t{}\t{}\t{}\t{}\t{}\n'.format(chrName, pstart, pend, refGeneName, '0', pstrand))
  geneNames = set(geneNames)
  with open('tmp_4_ana_refGene.bed', 'w') as fout:
    for gg in geneNames:
      fout.write(gg)


def getEccdnaBed(txtFile='eccdnas_3_ana_out.txt'):
  segments = []
  with open(txtFile, 'r') as fin:
    dummy = fin.readline()
    for line in fin:
      eles = line.strip().split(',')
      segs = [x[:-1] for x in eles[1].strip(';;').split(';;')]
      segments += segs
  segments = set(segments)
  with open('tmp_4_ana_eccdna.bed', 'w') as fout:
    for ss in segments:
      eles = re.split(r'[:-]', ss)
      fout.write('{}\t{}\t{}\n'.format(*eles))


def getEccdnaGene(genebedfile='tmp_4_ana_refGene.bed', eccdnabedfile='tmp_4_ana_eccdna.bed'):
  refseqGenes = getOncogeneSubset()
  genebed = pybedtools.BedTool(genebedfile)
  eccdnabed = pybedtools.BedTool(eccdnabedfile)
  eccGene = eccdnabed.intersect(genebed, F=1.0, wa=True, wb=True)
  fout = open('eccdna_gene_4_ana_out.txt', 'w')
  fout.write('eccseg_loc,refseq_loc,refseq_name,refseq_strand,oncogene\n')
  for ee in eccGene:
    eles = str(ee).strip().split('\t')
    fout.write('{}:{}-{},{}:{}-{},{},{strand},{onco}\n'.format(*eles, strand=eles[8], onco=str(eles[6] in refseqGenes)))
  fout.close()


def getOncogeneSubset(oncofile='/data/home/pengli_data/aa/CycleViz/Bushman_group_allOnco_May2018.tsv'):
  refseqName = set()
  with open(oncofile) as fin:
    dummy = fin.readline
    for line in fin:
      eles = line.strip().split('\t')
      refseqName.add(eles[-1].strip('"'))
  return refseqName


def main():
  getRefGeneBed()
  getEccdnaBed()
  getEccdnaGene()


if __name__ == '__main__':
  main()
  print('Done')
