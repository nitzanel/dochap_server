from dochap_tool.ncbi_utils import downloader as ncbi_downloader
from dochap_tool.ucsc_utils import downloader as ucsc_downloader
from dochap_tool.db_utils import create_db
import os

def main():
    species = ['Mus_musculus','Homo_sapiens']
    ncbi_downloader.download_species_from_ncbi(species,'data')
    ucsc_downloader.download_from_ucsc(species,'data')
    for specie in species:
        create_db.create_db('data',specie)

if __name__ == '__main__':
    main()

