from dochap_tool.gtf_utils import parser as gtf_parser
from dochap_tool.draw_utils import draw_tool
from dochap_tool.compare_utils import compare_exons
import pathlib
import os
import flask


def create_html_pack_better(user_transcripts, specie, genes, run_local: bool=False, save_dir: str=None, file_name: str='compare.html'):
    genes_ids_dict = get_genes_ids_dict(user_transcripts, genes)
    # domains_svgs_variations_by_gene_symbol, variants_by_symbol = get_genes_svgs_and_variations(genes_ids_dict, specie)
    transcript_svgs_by_symbol = get_svgs(user_transcripts, genes_ids_dict, specie)
    html = flask.render_template(
            'compare_transcripts.html',
            genes_ids_dict = genes_ids_dict,
            svgs_by_symbol = transcript_svgs_by_symbol
            )
    if run_local:
        if save_dir is None:
            save_dir = './output'
        pathlib.Path(save_dir.mkdir(parents=True, exist_ok=True))
    else:
        save_dir = '/tmp'
    with open(os.path.join(save_dir, file_name), 'w') as f:
        f.write(html)
    flask.flash('Parsing complete!', category='success')
    if run_local:
        flask.flash(f'The file can be found at: {os.path.join(save_dir,file_name)}', category='information')
        return flask.redirect('upload')
    flask.flash('Download starts...', category='information')
    response = flask.send_file('/tmp/compare.html', as_attachment=True)
    return response


def get_genes_ids_dict(transcripts: dict, genes: list) -> dict:
    if len(genes) == 0:
        user_gene_transcript_ids_dict = gtf_parser.get_dictionary_of_ids_and_genes(transcripts)
    else:
        user_gene_transcript_ids_dict = gtf_parser.get_dictionary_of_ids_and_genes(transcripts, genes)
    return user_gene_transcript_ids_dict


def get_svgs(user_transcripts: dict, genes_ids_dict: dict, specie:str):
    svgs_by_symbol = {}
    symbols = genes_ids_dict.keys()
    for symbol in symbols:
        db_transcripts_dict = compare_exons.get_exons_from_gene_symbol('data',specie,symbol)
        user_transcripts_dict = user_transcripts[symbol]
        svg = draw_tool.draw_combination(symbol, user_transcripts_dict, 'blue', db_transcripts_dict, 'purple')
        svgs_by_symbol[symbol] = svg
    return svgs_by_symbol
