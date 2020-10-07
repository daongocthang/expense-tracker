class Transaction:
    def __init__(self, amount, category, notes, date):
        self.amount = amount
        self.category = category
        self.notes = notes
        self.date = date

    @staticmethod
    def from_dict(src):
        return Transaction(src['amount'], src['category'], src['notes'], src['date'])

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'notes': self.notes,
            'date': self.date
        }

    def __str__(self):
        return f'amount: {self.amount}, category: {self.category}, notes: {self.notes}, date: {self.date}'
