from typing import Tuple
import faiss
from faiss.loader import 
from functools import partial
import numpy as np 


'''
Distance functions for Markov Process sample choice
'''

def init_penalty_distance(resource, alpha, beta, gamma):
    norm = partial(faiss.pairwise_distance_gpu, resource)
    def distance(x, xs):
        return alpha * norm(x[:, 0], xs[:, 0]) + beta * norm(x[:, 1], xs[:, 1]) + () * norm(x[:, 2], xs[:, 2]) - gamma * norm(xs[:, 1], xs[:, 2])

    return distance

def init_interpolated_distance(resource, alpha, beta, equal=False):
    gamma = 1 - alpha - beta
    if gamma < 0: gamma = 0
    if equal:
        alpha, beta, gamma = 1, 1, 1

    norm = partial(faiss.pairwise_distance_gpu, resource)
    def distance(x, xs):
        return alpha * norm(x[:, 0], xs[:, 0]) + beta * norm(x[:, 1], xs[:, 1]) + gamma * norm(x[:, 2], xs[:, 2])

    return distance

def init_interpolated_similarity(resource, alpha, beta, equal=False, METRIC=None):
    if not METRIC:
        METRIC = faiss.METRIC_INNER_PRODUCT

    gamma = 1 - alpha - beta
    if gamma < 0: gamma = 0
    if equal:
        alpha, beta, gamma = 1, 1, 1

    norm = lambda x : faiss.normalize_L2(x)
    dist = lambda x, y : faiss.pairwise_distance_gpu(resource, norm(x), norm(y), metric=METRIC) 

    def distance(x, xs):
        x = x.reshape()
        q = alpha * dist(x[:, 0], xs[:, 0])
        pos = beta * dist(x[:, 1], xs[:, 1])
        neg = gamma * dist(x[:, 2], xs[:, 2])
        return q + pos + neg

    return distance






    