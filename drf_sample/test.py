#!/usr/bin/env python3
import os
import glob
import sys
import json
sys.path.append('/fan/')

from fan.sync import get_context  # noqa
from fan.exceptions import RPCHttpError


with get_context('test.py') as ctx:
    author = ctx.rpc.app.author

    cr = author.create(name='lol')
    print('create: {}'.format(cr))

    lst = ctx.rpc.app.author.list()
    print('list: {}'.format(lst))

    u = lst[0]
    u['name'] = 'new name'

    up = author.update(**u)
    print('update: {}'.format(up))

    lst = ctx.rpc.app.author.list()
    print('list2: {}'.format(lst))

    for l in lst:
        print('delete : {}'.format(l))
        dl = author.delete(**l)
    try:
        author.delete(id=1)
    except RPCHttpError as e:
        assert e.response.status_code == 404
    else:
        raise Exception


def get_spans():
    for name in glob.glob('/tmp/trace_*'):
        with open(name) as f:
            yield json.load(f)
        os.unlink(name)


def print_sorted(spans, curr=None, level=0, skip=[]):
    for span in spans:
        if span in skip:
            continue
        parent_id = span['parent_id']
        if parent_id == curr:
            indent = '-'*level
            print('{}-{}'.format(indent, span['span_id']))
            skip.append(span)
            print_sorted(spans, span['span_id'], level+1, skip)

spans = list(get_spans())
print_sorted(spans)
