import pandas as pd

def _read_tsv(path):
    return pd.read_csv(path, sep = '\t')

class Datasets:
    
    def __init__(self, data_dir):
        self._data_dir = data_dir
        self._path_gcp_datasets = self._data_dir + '/raw/gcp/datasets'
        self.ssi = self._read_gcp('StandingSettlementInstructions', 'SSIPLUS_V3_MONTHLY_FULL_20200828.txt')
        self.bdp = self._read_gcp('StandingSettlementInstructions', 'BANKDIRECTORYPLUS_V3_FULL_20200828.txt')
    
    def _read_gcp(self, dir_name, file_name):
        return _read_tsv(self._path_gcp_datasets + '/' + dir_name + '/' + file_name)
    
