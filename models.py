from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer, primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", back_populates="dev")


    def __repr__(self):
        return f"<Dev{self.name}>"
    

    def _repr_(self):
        return f"<Dev(name={self.name})>"
    
    @property
    def companies(self):
        """Return a list of companies that have given freebies to this dev"""
        return list(set(freebie.company for freebie in self.freebies))

    def received_one(self, item_name):
        """Check if dev has received a freebie with given item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie, session):
        """Transfer a freebie to another dev if it belongs to this dev"""
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", back_populates="company")
 

    def __repr__(self):
        return f"<Company{self.name})>"
    
    @property
    def devs(self):
        return list(set(freebie.dev for freebie in self.freebies))
    

    def give_freebie(self, session, dev, item_name, value):
        """Create and return a new freebie for this company and dev"""
        freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        session.add(freebie)
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        """Return the company with the earliest founding year"""
        return session.query(cls).order_by(cls.founding_year).first()

class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer, primary_key=True)
    item_name = Column(String())
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey("devs.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def __repr__(self):
        return f"<Freebie {self.item_name}, Value:{self.value}>"

    def print_details(self):
        """Return a formatted string with freebie details"""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
