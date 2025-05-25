from models import Base

from sqlalchemy import create_engine

engine = create_engine('sqlite:///freebies.db')


Base.metadata.create_all(engine)

print("✅ freebies.db created and tables initialized!")