from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base_class import Base

class SIPTransaction(Base):
    __tablename__ = "mf_sys_txn_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    scheme_code = Column(String)
    amount = Column(Float)       # SIP amount
    units = Column(Float)
    txn_type = Column(String)
    txn_status = Column(String)


class SIPInstallments(Base):
    __tablename__ = "mf_sip_installments"

    id = Column(Integer, primary_key=True, index=True)
    sip_id = Column(Integer, index=True)
    amount = Column(Float)
    nav = Column(Float)
    units = Column(Float)
    status = Column(String)


class SIPSchedule(Base):
    __tablename__ = "mf_sip_schedule_details"

    id = Column(Integer, primary_key=True, index=True)
    sip_id = Column(Integer, index=True)
    total_invested_amount = Column(Float)
    total_units_allocated = Column(Float)
    completed_installments = Column(Integer)
    next_due_date = Column(Date)


class MutualFundSchemes(Base):
    __tablename__ = "mutual_fund_schemes"

    id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String, index=True)
    scheme_name = Column(String)
