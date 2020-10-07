import argparse
from datetime import datetime as dt
import sys

from decouple import config as conf
from google.cloud.firestore import Client, CollectionReference

from transaction import Transaction

db = Client.from_service_account_json(conf('GOOGLE_APPLICATION_CREDENTIALS'))
exp_ref = db.collection('expenses')  # type: CollectionReference


def read_all():
    return [s for s in exp_ref.stream()]


def read_at(date_str):
    return [s for s in exp_ref.where('date', '==', date_str).stream()]


def update_at(date_str):
    pass


def create(doc_id, trans: Transaction):
    exp_ref.document(doc_id).set(trans.to_dict())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', dest='amount', type=int)
    parser.add_argument('-c', dest='category', default='')
    parser.add_argument('-n', dest='notes', default='')
    parser.add_argument('-d', dest='date', default=dt.now().strftime('%Y-%m-%d'))

    parser.add_argument('-l', dest='list', action='store_true')

    args = parser.parse_args()

    if args.list:
        total = 0
        print('{:<25}{:<12}{:<18}{}'.format('Date', 'Amount', 'Category', 'Notes'), end='\n')
        for doc in read_all():
            trans = Transaction.from_dict(doc.to_dict())
            print('{:<25}{:<12}{:<18}{}'.format(trans.date, trans.amount, trans.category, trans.notes))
            total += trans.amount

        print(end='\n')
        print('Total Expenses = {}'.format(total))

    if not args.amount:
        sys.exit()
    doc_id = dt.now().strftime('%Y%m%d%H%M%S')
    trans = Transaction(doc_id, args.amount, args.category, args.notes, args.date)

    create(doc_id, trans)
