# init_db.py
from app.database import Base, engine
from app import models# ensure all models are imported
from app.models.rank import Rank
# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully.")
