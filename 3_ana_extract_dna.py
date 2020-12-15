
import os, sys, glob, re, uuid

os.getcwd()
outFh = open('./eccdnas_3_ana_out.txt', 'w')
outFh.write('UUID,Segments,Copy_count,File,Img\n')

cycleFiles = sorted(glob.glob('./*/aaout/*_cycles.txt'))

for ff in cycleFiles:
  print('This is', ff)
  cyclesFilename = os.path.basename(ff)
  pngFilename = cyclesFilename.split('_cycle')[0] + '.png'
  #outFh.write('This is '+ ff + '\n') ###
  segDict = {}
  with open(ff, 'r') as fh:
    for line in fh:
      line = line.strip()
      # segments information dict
      if re.compile('Segment').match(line):
        eles = line.split()
        segDict[eles[1]] = '{}:{}-{}'.format(*eles[2:])
        continue
      # find cycle line
      if re.compile('Cycle').match(line):
        ## skip non-eccDNA
        if re.search(r'\D0\D', line):
          print(line, 'skipped')
          #outFh.write(line + ' skipped\n') ###
        ## parse eccDNA info
        else:
          #outFh.write(line + '\n') ###
          outFh.write(uuid.uuid4().hex + ',')
          mm = re.search(r'^Cycle=(.*);Copy_count=(.*);Segments=(.*)$', line)
          if mm:
            nCycle = mm.group(1)
            countCopy = mm.group(2)
            segments = mm.group(3).split(',')
            # eg 'd+,d-,d+'
            ### handle segments info
            for seg in segments:
              seg = seg.strip()
              segId = seg[:-1]
              segStrand = seg[-1]
              segInfo = segDict[segId] + segStrand
              #outFh.write('{}__{};;'.format(seg, segInfo))
              outFh.write('{};;'.format(segInfo))
            outFh.write(',{},{},{}\n'.format(countCopy, cyclesFilename, pngFilename))
  #break

outFh.close()
