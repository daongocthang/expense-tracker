class Transaction:
    def __init__(self, doc_id, amount, category, notes, date):
        self.doc_id = doc_id
        self.amount = amount
        self.category = category
        self.notes = notes
        self.date = date

    @staticmethod
    def from_dict(src):
        return Transaction(src['doc_id'], src['amount'], src['category'], src['notes'], src['date'])

    def to_dict(self):
        return {
            'doc_id': self.doc_id,
            'amount': self.amount,
            'category': self.category,
            'notes': self.notes,
            'date': self.date
        }

    def __repr__(self):
        return 'Transaction(doc_id={},amount={},category={},notes={},date={})'.format(
            self.doc_id, self.amount, self.category, self.notes, self.date
        )
