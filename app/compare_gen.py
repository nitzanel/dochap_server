from dochap_tool.gtf_utils import parser as gtf_parser
from dochap_tool.draw_utils import draw_tool
from dochap_tool.compare_utils import compare_exons
import pathlib
import os
import flask


def create_html_pack_better(user_transcripts, specie, genes, run_local: bool=False, save_dir: str=None, file_name: str='compare.html'):
    print('genes are', genes)
    print('user_transcripts are of length', len(user_transcripts))
    genes_ids_dict = get_genes_ids_dict(user_transcripts, genes)
    user_transcripts = gtf_parser.get_dictionary_of_exons_and_genes(user_transcripts)
    # domains_svgs_variations_by_gene_symbol, variants_by_symbol = get_genes_svgs_and_variations(genes_ids_dict, specie)
    transcript_svgs_by_symbol = get_svgs(user_transcripts, genes_ids_dict, specie)
    with open('./static/css/svg_style.css','r') as f:
        fix_css = f.read()
    with open('./static/js_scripts/tooltip_size_fix.js','r') as f:
        fix_js = f.read()
    html = flask.render_template(
            'compare_transcripts.html',
            svgs_by_symbol = transcript_svgs_by_symbol,
            fix_css = fix_css,
            fix_js = fix_js
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
        if genes[0] == '':
            # insanity check
            genes = None
        user_gene_transcript_ids_dict = gtf_parser.get_dictionary_of_ids_and_genes(transcripts, genes)
    print(user_gene_transcript_ids_dict)
    return user_gene_transcript_ids_dict


def get_svgs(user_transcripts: dict, genes_ids_dict: dict, specie:str):
    svgs_by_symbol = {}
    symbols = genes_ids_dict.keys()
    print('symbols are: ', symbols)
    for symbol in symbols:
        gene_symbol = gtf_parser.get_gene_symbol_from_transcript_ids('data', specie, user_transcripts[symbol].keys())
        print('GENE SYMBOL IS', gene_symbol)
        user_transcripts_dict = user_transcripts[symbol]
        svg = None
        if gene_symbol is None:
            print('could not find ncbi symbol for ', symbol)
            continue
        db_transcripts_dict = compare_exons.get_exons_from_gene_symbol('data',specie,gene_symbol)
        svg = draw_tool.draw_combination(symbol, user_transcripts_dict, 'blue', db_transcripts_dict, 'purple')
        svgs_by_symbol[symbol] = svg
    return svgs_by_symbol
