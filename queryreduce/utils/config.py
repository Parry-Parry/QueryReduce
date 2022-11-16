from typing import NamedTuple, Any, Union
import torch
from numpy import array


### Config Structures ###

class EmbedConfig(NamedTuple):
    tokenizer : Any 
    model : Any
    dataset : Any

### General Structures ###

class Embedding(NamedTuple):
    embed_obj : Any 
    id : Any

class Triplet(NamedTuple):
    id : Any
    q : Any
    d_pos : Any 
    d_neg : Any
