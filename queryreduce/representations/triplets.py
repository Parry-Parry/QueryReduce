from typing import Any, List, Union, NamedTuple
from queryreduce.config import EmbedConfig, Triplet
import numpy as np
import pandas as pd
from pandas.io.parsers import TextFileReader
from sentence_transformers import SentenceTransformer
import pickle

'''
Retrieve text associated with triplets of IDs, generate embeddings and return tuples
'''

class VectorFactory:
    def __init__(self, model : str, **kwargs) -> None:
        self.model = SentenceTransformer(model)

    ### BATCHED OP ###
    def _batch_encode(self, txt : List[str]) -> np.array:
        return self.model.encode(txt, convert_to_numpy=True)
    def _batch_create(self, triples : pd.DataFrame):
        e_q = self._batch_encode(triples['qid'].to_list())
        e_pos = self._batch_encode(triples['pid+'].to_list())
        e_neg = self._batch_encode(triples['pid-'].to_list())

        batch = np.stack([e_q, e_pos, e_neg], axis=1)

        return batch.reshape((batch.shape[0], -1))

    def run(self, triples : TextFileReader, out : str):
        batches = [self._batch_create(chunk) for chunk in triples]
        with open(out, 'wb') as f:
            pickle.dump(np.stack(batches, axis=0), f)
    
