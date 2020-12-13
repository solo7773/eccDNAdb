
import os, sys, glob, pandas as pd, re

clinicfile = 'allPatches_Table_S1_20.10.16_py.csv'
eccdnafile = 'eccdnas_3_ana_out.txt'
outdir = 'webdata'
outfilename = 'eccdnas_3_ana_out.txt_3.1_ana_out.txt'

existids = set()
input('There are {} existing ids, are you sure?'.format(len(existids)))


def getEccId(xx=None, existids=None):
    """
    Assign id to each eccDNA
    :param xx: string
    :param existids: set
    :return: string
    """
    segments = xx.strip(';;').split(';;')
    # print(segments)
    segChrs = []
    for ii in segments:
        chrname = ii.split(':')[0]
        segChrs += [chrname]
    segChrs = list(set(segChrs))
    eccidsufix = 1
    if len(segChrs) > 1:
        eccid = 'hsa_{}Chr_{}S_{}'.format(len(segChrs), len(segments), eccidsufix)
        while eccid in existids:
            eccidsufix += 1
            eccid = 'hsa_{}Chr_{}S_{}'.format(len(segChrs), len(segments), eccidsufix)
        # print(eccid)
    else:
        eccid = 'hsa_{}_{}S_{}'.format(segChrs[0].capitalize(), len(segments), eccidsufix)
        while eccid in existids:
            eccidsufix += 1
            eccid = 'hsa_{}_{}S_{}'.format(segChrs[0].capitalize(), len(segments), eccidsufix)
        # print(eccid)
    # update existed id
    existids.add(eccid)
    return eccid


eccdnas = pd.read_csv(eccdnafile)
# get SRR
eccdnas = eccdnas.assign(Run = eccdnas['Img'].apply( lambda x: x.split('_')[0]))
# custom eccdna id
resEccdnaIds = eccdnas['Segments'].apply(getEccId, args=(existids,))
eccdnas.insert(0, 'dbID', resEccdnaIds)

clinicData = pd.read_csv(clinicfile)

resdf = eccdnas.merge(clinicData, how='left', on='Run', validate='many_to_one')
resdf.to_csv(os.path.join(outdir, outfilename), na_rep=' ', index=False)

print('Done')