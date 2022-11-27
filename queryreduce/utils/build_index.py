import numpy as np 
import faiss 
import logging 
import bz2
import argparse 
import pickle

parser = argparse.ArgumentParser()

parser.add_argument('-source', type=str)
parser.add_argument('-k', type=int)
parser.add_argument('-out', type=str) 

def main(args):
    with bz2.open(args.source, 'rb') as f:
        triples = pickle.load(f)
    prob_dim = triples.shape[-1]

    ngpus = faiss.get_num_gpus()
    if ngpus < 1:
        logging.error("Error! Faiss Indexing Requires GPU, Exiting...")
        return 1

    logging.info('Building Index')

    faiss.normalize_L2(triples)
    quantiser = faiss.IndexFlatL2(prob_dim) 
    cpu_index = faiss.IndexIVFFlat(quantiser, prob_dim, args.k, faiss.METRIC_INNER_PRODUCT)
    cpu_index.train(triples)
    cpu_index.add(triples)

    faiss.write_index(cpu_index, args.out + f'triples.{args.k}.index')

    return 0
    


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('Building Faiss IVF Index')
    main(parser.parse_args())