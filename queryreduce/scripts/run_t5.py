import pyterrier as pt
pt.init()
from pyterrier_t5 import MonoT5ReRanker
from pyterrier.measures import RR, MAP, NDCG
import argparse 
import logging
import os
import pandas as pd 

parser = argparse.ArgumentParser()

parser.add_argument('-source', type=str)
parser.add_argument('-sink', type=str)
parser.add_argument('-i_dir', type=str)
parser.add_argument('-i_name', type=str)
parser.add_argument('-variant', type=str)

parser.add_argument('--filter', type=str, nargs='*')
parser.add_argument('--verbose', action='store_true')

def main(args):
    source = os.path.join(args.source, 'train.py')
    dirs = [f for f in os.listdir(source) if not os.path.isfile(os.path.join(source, f))]
    if args.filter:
        dirs = [d for filter in args.filter for d in dirs if filter in d]

    bm25 = pt.BatchRetrieve.from_dataset('msmarco_passage', 'terrier_stemmed_text', wmodel='BM25', metadata=['docno', 'text'])
    dataset = pt.get_dataset("trec-deep-learning-passages")

    for directory in dirs:    
        checkpoint = os.path.join(source, directory, 'checkpoints', 't5.dnn')
        monoT5 = MonoT5ReRanker(model=checkpoint, batch_size=32)
        
        sparse_T5 = bm25 >> pt.text.get_text(dataset, "text") >> monoT5

        res = pt.Experiment(
        [bm25, sparse_T5],
        dataset.get_topics(variant=args.variant),
        dataset.get_qrels(variant=args.variant),
        eval_metrics=[RR(rel=2), MAP(rel=2), NDCG(cutoff=10)],
        names=["BM25", "BM25 >> MonoT5"]
        )

        res.to_csv(os.path.join(args.sink, f"{directory}.csv"))
        
        
if __name__ == '__main__':
    args = parser.parse_args()
    if args.verbose: log_level = logging.DEBUG
    else: log_level = logging.INFO
    logging.basicConfig(format='%(asctime)s - %(message)s', level=log_level)
    logging.info('--Running Experiment for MonoT5--')
    main(args)
