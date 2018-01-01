from dochap_tool.gtf_utils import parser as gtf_parser

def parse_gtf_file(filepath):
        user_transcripts = gtf_parser.parse_gtf_file('/tmp/uploaded_gtf')
        return user_transcripts
