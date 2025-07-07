# init_db.py
from app.database import Base, engine
from app.models import user, role, permission, department  # ensure all models are imported

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully.")
