from dochap_tool.gtf_utils import parser as gtf_parser
from dochap_tool.draw_utils import draw_tool
from dochap_tool.compare_utils import compare_exons
import utils
import flask


def create_html_pack(transcripts,specie):
    # get needed data
    genes_ids_dict = get_genes_ids_dict(transcripts)
    svgs_by_symbol, variants_by_symbol = get_genes_svgs_and_variations(genes_ids_dict,specie)
    db_transcripts_svgs_by_id,db_transcript_ids_by_symbol = get_transcripts_svgs(genes_ids_dict,specie)
    user_svgs_by_id_by_symbol = get_user_svgs_by_id(transcripts,genes_ids_dict)
    # render it
    html = flask.render_template(
        'compare.html',
        genes_ids_dict = genes_ids_dict,
        db_gene_svg_list_dict = svgs_by_symbol,
        gene_variations_dict = variants_by_symbol,
        db_transcript_id_svg_dict = db_transcripts_svgs_by_id,
        db_transcript_ids_by_symbol = db_transcript_ids_by_symbol,
        user_transcript_id_svg_dict = user_svgs_by_id_by_symbol,
    )
    # fix bootstrap css link
    html = html.replace('//cdnjs','http://cdnjs')
    with open('/tmp/compare.html','w') as f:
        f.write(html)
    response = flask.send_file('/tmp/compare.html',as_attachment=True)
    return response


def get_genes_ids_dict(transcripts):
    user_gene_transcript_ids_dict = gtf_parser.get_dictionary_of_ids_and_genes(transcripts)
    return user_gene_transcript_ids_dict


def get_genes_svgs_and_variations(genes_ids_dict,specie):
    symbols = genes_ids_dict.keys()
    domains_by_symbol = {}
    for symbol in symbols:
        domains_by_symbol[symbol] = compare_exons.get_domains_of_gene_symbol('data',specie,symbol.lower())
    variants_by_symbol = {}
    svgs_by_symbol = {}
    for symbol in domains_by_symbol:
        svgs_by_symbol[symbol] = []
        variants_by_symbol[symbol] = []
        domains_variants = domains_by_symbol[symbol]
        for index,domain_variant in enumerate(domains_variants):
            variant_text = f'domains variant: {index+1}'
            svg=draw_tool.draw_domains(domain_variant,variant_text)
            svgs_by_symbol.append(svg)
            variants_by_symbol[symbol].append(variant_text)

    return svgs_by_symbol, variants_by_symbol

def get_transcripts_svgs(genes_ids_dict,specie):
    symbols = genes_ids_dict.keys()
    transcripts_dict_by_symbol= {}
    for symbol in symbols:
        transcripts_dict = compare_exons.get_exons_from_gene_symbol('data',specie,symbol)
        transcripts_dict_by_symbol[symbol] = transcripts_dict
    transcripts_svgs_by_id= {}
    db_transcript_ids_by_symbol = {}
    for symbol in transcripts_dict_by_symbol:
        db_transcript_ids_by_symbol[symbol] = []
        for t_id,exon_list in transcripts_dict_by_symbol[symbol].items():
            t_id_text = f'transcript_id: {t_id}'
            svg = draw_tool.draw_exons(exon_list,t_id_text)
            transcripts_svgs_by_id[t_id] = svg
            db_transcript_ids_by_symbol[symbol].append(t_id)

    return transcripts_svgs_by_id,db_transcript_ids_by_symbol

def get_user_svgs_by_id(transcripts,genes_ids_dict):
    symbols = genes_ids_dict.keys()
    svg_by_symbol_by_id = {}
    for symbol in symbols:
        transcripts_of_gene = gtf_parser.get_transcripts_by_gene_symbol(transcripts,symbol)
        svg_by_symbol_by_id[symbol] = {}
        for t_id, exon_list in transcripts_of_gene.items():
            t_id_text = f'transcript_id: {t_id}'
            svg = draw_tool.draw_exons(exon_list,t_id_text)
            svg_by_symbol_by_id[symbol][t_id] = svg
    return svg_by_symbol_by_id


