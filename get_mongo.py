#!/usr/bin/env python
import numpy as np
import pymongo
from tabulate import tabulate
import zlib

def decompress_array(a):
    """Decompress and map from log10 space back to standard coordinates."""
    return np.power(10, np.fromstring(zlib.decompress(a['value'].decode('base64'))).reshape(a['shape']))

def main(exp_name, params):
    # Construct projection query
    proj = {p : '$params.{0}.values'.format(p) for p in PARAMS}
    proj['main'] = '$values.main'
    proj['_id'] = False

    # Make MongoDB connection
    db = pymongo.MongoClient()['spearmint']

    # Select/project experiment job results
    jobs = db[EXP_NAME + '.jobs']\
        .aggregate([
            { '$project': proj },
        ])

    for job in jobs:
        result = {}
        for k,v in job.items():
            if k == 'main': result['val_loss'] = v
            else: result[k] = decompress_array(v)[0]
        yield result

if __name__ == "__main__":
    EXP_NAME = 'duration'
    PARAMS = ['rnn_size', 'seq_length', 'wordvec_size', 'num_layers']

    print tabulate(
        main(EXP_NAME, PARAMS),
        headers='keys',
        tablefmt='simple_tables')

