from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=account_id).first()

    @staticmethod
    def credit_exists(db: Session, account_id: int) -> bool:
        return db.query(Credit).filter_by(account_id=account_id).first() is not None
