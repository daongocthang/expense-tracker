import argparse
from datetime import datetime as dt
import sys

from decouple import config as conf
from google.cloud.firestore import Client, CollectionReference, Query

import utils
from transaction import Transaction

db = Client.from_service_account_json(conf('GOOGLE_APPLICATION_CREDENTIALS'))
exp_ref = db.collection('expenses')  # type: CollectionReference


def read_all():
    return [s for s in exp_ref.order_by('date', direction=Query.DESCENDING).stream()]


def update(doc_id, fields):
    doc_ref = exp_ref.document(doc_id)
    doc_ref.update(fields)


def create(doc_id, trans: Transaction):
    exp_ref.document(doc_id).set(trans.to_dict())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--new', action='store_true')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('-a', dest='attrs', action=utils.StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...",
                        required=False)

    args = parser.parse_args()

    if args.list:
        total = 0
        print('{:<18}{:<15}{:<12}{:<15}{}'.format('Id', 'Date', 'Amount', 'Category', 'Notes'), end='\n')

        for doc in read_all():
            trans = Transaction.from_dict(doc.to_dict())
            print('{:<18}{:<15}{:<12}{:<15}{}'.format(trans.doc_id, trans.date, trans.amount, trans.category,
                                                      trans.notes))
            total += trans.amount

        print(end='\n')
        print('Total Expenses = {}'.format(total))
        sys.exit()

    attrs = dict()
    for k, v in args.attrs.items():
        attrs[k] = v

    if args.new:
        now = dt.now()

        doc_id = now.strftime('%Y%m%d%H%M%S')
        amount = int(args.amount) if args.amount else 0
        category = args.category if args.category else 'personal'
        notes = args.notes if args.note else ''
        date = args.date if args.date else now.strftime('%Y-%m-%d')

        trans = Transaction(doc_id, args.amount, args.category, args.notes, args.date)

        create(doc_id, trans)

    if args.update:
        if not attrs.get('doc_id'):
            print('[-] Not found any documentId')
        doc_id = attrs.pop('doc_id')

        if attrs.get('amount'):
            val = int(attrs.get('amount'))
            attrs['amount'] = val

        update(doc_id, attrs)
