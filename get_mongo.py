#!/usr/bin/env python
import click
import numpy as np
import pprint
import pymongo
import zlib

from tabulate import tabulate

def decompress_array(a):
    """Decompress and map from log10 space back to standard coordinates."""
    return np.power(10, np.fromstring(zlib.decompress(a['value'].decode('base64'))).reshape(a['shape']))

def get_job_results(exp_name, params):
    """Retrieves all job results for experiment `exp_name` and parameters `params`."""
    # Construct projection query
    proj = {p : '$params.{0}.values'.format(p) for p in params}
    proj['val_loss'] = '$values.main'
    proj['_id'] = False

    # Make MongoDB connection
    db = pymongo.MongoClient()['spearmint']

    # Select/project experiment job results
    jobs = db[exp_name + '.jobs']\
        .aggregate([
            { '$project': proj },
            { '$sort': { 'val_loss': 1 } }
        ])

    for job in jobs:
        result = parse_job(job)

        # exclude results which have no metric for comparison
        if 'val_loss' not in result:
            continue
        else:
            yield result

def parse_job(job):
    result = {}
    for k,v in job.items():
        if k == 'val_loss': result[k] = v
        else: result[k] = decompress_array(v)[0]
    return result

@click.command()
@click.argument('exp-name', nargs=1, type=str)
@click.option('-p','--params', multiple=True, type=str)
def print_mongo_results(exp_name, params):
    """Retrieves all `params` for experiment `exp-name`, converts log-scale to standard scale, and formats
    into Markdown."""
    if not params:
        params = ['rnn_size', 'seq_length', 'wordvec_size', 'num_layers']
    print 'Best result:'
    pprint.pprint(min(get_job_results(exp_name, params), key=lambda x: x['val_loss']))
    print 'Markdown-formatted table of all results:'
    print tabulate(
        get_job_results(exp_name, params),
        headers='keys',
        tablefmt='pipe')

if __name__ == "__main__":
    print_mongo_results()
