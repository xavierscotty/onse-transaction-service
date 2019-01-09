import uuid

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class PostgreSQLTransactions:
    def __init__(self, host, port, username, password, db):
        url = f'postgresql://{username}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def store(self, tx_hash):
        transaction = Transaction(id=str(uuid.uuid4()),
                                  account_number=tx_hash['accountNumber'],
                                  amount=tx_hash['amount'])
        self.session.add(transaction)
        self.session.commit()

    def fetch_by_account_number(self, account_number):
        transactions = self.session \
            .query(Transaction) \
            .filter(Transaction.account_number == account_number)

        return [{'accountNumber': tx.account_number,
                 'amount': tx.amount} for tx in transactions]


Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String(100), primary_key=True)
    account_number = Column(String(50))
    amount = Column(Integer)
