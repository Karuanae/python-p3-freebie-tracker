# debug.py - Alternative testing script

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

def display_data(session):
    """Helper function to display current data"""
    print("\n=== CURRENT DATABASE STATE ===")
    companies = session.query(Company).all()
    devs = session.query(Dev).all()
    freebies = session.query(Freebie).all()
    
    print("Companies:")
    for company in companies:
        print(f"- {company.name} (founded {company.founding_year})")
    
    print("\nDevelopers:")
    for dev in devs:
        print(f"- {dev.name}")
    
    print("\nFreebies:")
    for freebie in freebies:
        print(f"- {freebie.print_details()}")

def test_relationships(session):
    """Test all relationship properties"""
    print("\n=== TESTING RELATIONSHIPS ===")
    
    # Test company.devs
    for company in session.query(Company):
        dev_names = [dev.name for dev in company.devs]
        print(f"{company.name} has developers: {', '.join(dev_names) if dev_names else 'None'}")
    
    # Test dev.companies
    for dev in session.query(Dev):
        company_names = [company.name for company in dev.companies]
        print(f"{dev.name} has freebies from: {', '.join(company_names) if company_names else 'None'}")

def test_methods(session):
    """Test all class methods"""
    print("\n=== TESTING METHODS ===")
    
    # Test oldest_company
    oldest = Company.oldest_company(session)
    print(f"Oldest company is {oldest.name} (founded {oldest.founding_year})")
    
    # Test received_one
    dev = session.query(Dev).filter_by(name="Musk").first()
    print(f"Does Musk have a T-shirt? {dev.received_one('T-shirt')}")
    print(f"Does Musk have a Mug? {dev.received_one('Mug')}")
    
    # Test give_away
    freebie = session.query(Freebie).filter_by(item_name="T-shirt").first()
    print(f"\nBefore give_away: {freebie.print_details()}")
    dev.give_away(dev=session.query(Dev).filter_by(name="Louis").first(), 
                 freebie=freebie, 
                 session=session)
    print(f"After give_away: {freebie.print_details()}")

def add_new_data(session):
    """Add new test data"""
    print("\n=== ADDING NEW TEST DATA ===")
    
    # Add new company
    new_company = Company(name="Nvidia", founding_year=1993)
    session.add(new_company)
    
    # Add new dev
    new_dev = Dev(name="Linus")
    session.add(new_dev)
    
    session.commit()
    
    # Give new freebies
    company = session.query(Company).filter_by(name="Nvidia").first()
    dev = session.query(Dev).filter_by(name="Linus").first()
    company.give_freebie(session, dev, "GPU", 1500)
    
    print("Added Nvidia company, Linus developer, and a GPU freebie")

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Display initial data
    display_data(session)
    
    # Test relationships
    test_relationships(session)
    
    # Test methods
    test_methods(session)
    
    # Add and test new data
    add_new_data(session)
    
    # Display final state
    display_data(session)
    
    session.close()
    print("\nDebugging complete!")
