from numpy import save
import pandas as pd
import chardet
import unicodedata
import re


class ClearData:
    def __init__(self, base_path: str, file: str) -> None:
        self.path = base_path + file
        self.base_path = base_path
        self.file = file
        self.data = None
        self.path_save = None

    def encoding_file(self) -> None:
        with open(self.path, 'rb') as f:
            result = chardet.detect(f.read(1000))
        return result['encoding']

    def read_dataset(self) -> None:

        self.data = pd.read_csv(self.path, delimiter=';',
                                encoding=self.encoding_file())

        pattern = re.compile(r'unnamed:\s\d+', re.IGNORECASE)

        drop_cols = [pattern.findall(i)[0]
                     for i in self.data.columns.values if len(pattern.findall(i)) > 0]

        self.data.drop(drop_cols, axis=1, inplace=True)

    def excluir_acento_rename(self) -> None:
        new_cols = []
        for p in self.data.columns:
            p_aux = []
            for i in unicodedata.normalize('NFKD', p):
                if len(p_aux) < len(p):
                    if not unicodedata.combining(i):
                        p_aux.append(i)

            ncol = ''.join(p_aux)

            if ncol[0] == '_':
                ncol = ncol[1:]
            if ncol[-1] == '_':
                ncol = ncol[:-1]

            new_cols.append(ncol)

        rnamecols = {k: v.lower() for k, v in zip(self.data.columns, new_cols)}
        self.data.rename(columns=rnamecols, inplace=True)
        index_peso = list(self.data.columns.values).index('peso_kg')
        index_altura = list(self.data.columns.values).index('altura_cm')
        self.virg_p_pt('float64', index_peso, index_altura+1)

    def classificar_imc(df):
        pass

    def virg_p_pt(self, new_type: str, col_i: int, col_f: int) -> None:
        for i in self.data.iloc[:, col_i:col_f]:
            self.data[i] = self.data[i].astype(
                str).str.replace(',', '.').astype(new_type)

    def clear_data(self) -> None:
        self.read_dataset()
        self.excluir_acento_rename()

    def save_data(self) -> None:
        self.path_save = self.base_path[:-1] + '_tratado/' + 'new_' + self.file
        self.data.to_csv(self.path_save, sep=';', index=False)
