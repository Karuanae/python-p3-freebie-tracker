#!/usr/bin/env python3

# Script goes here!
from models import Base, Dev, Company, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///freebies.db')

Session = sessionmaker(bind=engine)
session = Session()

# Create devs
dev1 = Dev(name="Musk")
dev2 = Dev(name="Louis")
dev3 = Dev(name="Ada")
dev4 = Dev(name="Grace")

# Create companies
company1 = Company(name="Grok", founding_year=2023)
company2 = Company(name="OpenAI", founding_year=2015)
company3 = Company(name="Microsoft", founding_year=1975)
company4 = Company(name="Apple", founding_year=1976)

# Create freebies with relationships
freebie1 = Freebie(item_name="T-shirt", value=20, dev=dev1, company=company2)
freebie2 = Freebie(item_name="Laptop", value=2000, dev=dev2, company=company1)
freebie3 = Freebie(item_name="Stickers", value=5, dev=dev3, company=company4)
freebie4 = Freebie(item_name="Water Bottle", value=15, dev=dev4, company=company3)
freebie5 = Freebie(item_name="Hoodie", value=45, dev=dev1, company=company1)  # Changed dev5 to dev1 since we only have 4 devs

session.add_all([company1, company2, company3, company4, dev1, dev2, dev3, dev4, freebie1, freebie2, freebie3, freebie4, freebie5])
session.commit()

print("Database created successfully!")
