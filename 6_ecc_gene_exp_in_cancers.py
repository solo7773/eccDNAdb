import pandas as pd, os, glob, plotly.graph_objects as go
from plotly.subplots import make_subplots
from multiprocessing import Pool

eccdnafile = 'eccdnas_3_ana_out.txt'
eccdnaGenefile = 'eccdna_gene_4_ana_out.txt'
geneExpFiles = glob.glob(
    'webdata/gene_exp/*')
outdir = 'eccdnageneexp'

eccdna = pd.read_csv(eccdnafile)
eccdnaGene = pd.read_csv(eccdnaGenefile)


def getGenes(xxx=None):
    xxx = xxx.strip(';;').split(';;')
    xxx = [x[:-1] for x in xxx]
    idx = eccdnaGene['eccseg_loc'].map(lambda x: x in xxx)
    if sum(idx) > 0:
        return eccdnaGene.loc[idx, 'refseq_name'].values.tolist()
    else:
        return None


def makeFig(row=None):
    eccdnauuid = row[0]
    print(eccdnauuid)
    markGenes = getGenes(row[1])
    if markGenes is not None:
        figAll = make_subplots(rows=1, cols=len(geneExpFiles), shared_yaxes=True,  # horizontal_spacing=0,
                               row_titles=None,
                               column_titles=['-'.join(os.path.basename(x).split('-')[0:2]) for x in geneExpFiles],
                               x_title='Cancer type', y_title='Gene expression (FPKM)')
        # plot for each cancer
        for i in range(len(geneExpFiles)):
            expFile = geneExpFiles[i]
            # print(os.path.basename(expFile))
            cancerType = '-'.join(os.path.basename(expFile).split('-')[:2])
            indata = pd.read_csv(expFile)
            indata.sort_values(by='Mean_exp', ascending=False, inplace=True)
            # indata = indata.iloc[0:200, :]
            idx = indata.Symbol.isin(markGenes)
            indata_marker = indata.loc[idx, :]
            fig = go.Figure(
                data=[go.Scatter(x=indata['Symbol'], y=indata['Mean_exp'], mode='lines',
                                 name='', connectgaps=True, showlegend=False),
                      go.Scatter(x=indata_marker['Symbol'], y=indata_marker['Mean_exp'],
                                 mode='markers', name='eccDNA', showlegend=False)],

                layout={'title_text': cancerType,
                        'xaxis_title_text': 'Genes ranked by expression level',
                        'xaxis_showticklabels': False,
                        'xaxis_ticks': '',
                        'yaxis_title_text': 'Expression (FPKM)'}
            )
            for iii in zip(range(indata_marker.shape[0]), indata_marker.values.tolist()):
                rrr = iii[1]
                # ensg Symbol Mean_exp
                fig.add_annotation(x=rrr[1], xref='x',
                                   y=rrr[2], yref='y', text=rrr[1],
                                   ax=rrr[1], axref='x', ay=-30 * (iii[0] % 9 + 1), ayref='pixel',
                                   arrowhead=0, arrowcolor='gray', font_color='magenta')
            fig.write_image(os.path.join(outdir, '{}_{}.png'.format(eccdnauuid, cancerType)))

            figAll.add_trace(go.Scatter(x=indata['Symbol'], y=indata['Mean_exp'], mode='lines',
                                        name='', connectgaps=True,
                                        marker={'color': 'gray'}, showlegend=False),
                             row=1, col=i + 1)
            figAll.add_trace(go.Scatter(x=indata_marker['Symbol'], y=indata_marker['Mean_exp'],
                                        mode='markers', name='eccDNA',
                                        marker={'color': 'red', 'opacity': 1}, showlegend=False),
                             row=1, col=i + 1)
        # polish fig
        # figAll.update_annotations(textangle=-90)
        for annotation in figAll.layout.annotations:
            if annotation.text != 'Cancer type':
                annotation.textangle = -90
        for i in range(len(geneExpFiles)):
            xaxis_name = 'xaxis' if i == 0 else f'xaxis{i + 1}'
            figAll.layout[xaxis_name].showticklabels = False
        figAll.write_image(os.path.join(outdir, eccdnauuid + '.png'))
    return None


# for arow in eccdna.values:
#     # uuid segments copycount cyclefile ampliconfile
#     makeFig(arow)
#     break

if __name__ == '__main__':
    with Pool(6) as p:
        p.map(makeFig, eccdna.values)

print('Done')
