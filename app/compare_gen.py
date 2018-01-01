from dochap_tool.gtf_utils import parser as gtf_parser
from dochap_tool.draw_utils import draw_tool
from dochap_tool.compare_utils import compare_exons
import json
import flask


def create_html_pack(transcripts):
    # get dict of genes and ids
    genes_ids_dict = get_genes_ids_dict(transcripts)
    html = flask.render_template('compare.html',genes_ids_dict=genes_ids_dict)
    html = html.replace('//cdnjs','http://cdnjs')
    with open('/tmp/compare.html','w') as f:
        f.write(html)
    response = flask.send_file('/tmp/compare.html',as_attachment=True)
    return response


def get_genes_ids_dict(transcripts):
    user_gene_transcript_ids_dict = gtf_parser.get_dictionary_of_ids_and_genes(transcripts)
    return user_gene_transcript_ids_dict


