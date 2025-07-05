from app.database import SessionLocal
from app.models import User
from app.utils import get_password_hash  # make sure this function exists
from sqlalchemy.exc import SQLAlchemyError

def populate():
    db = SessionLocal()

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "adminuser1").first()
        if existing_user:
            print("✅ Superuser already exists.")
            return

        # Create superuser
        superuser = User(
            username="adminuser1",
            email="syedjawadali92@gmail.com",
            hashed_password=get_password_hash("password123"),
            is_superuser=True,
            is_active=True
        )
        db.add(superuser)
        db.commit()
        print("✅ Superuser created successfully.")

    except SQLAlchemyError as e:
        db.rollback()
        print("❌ Error creating superuser:", str(e))
    finally:
        db.close()

if __name__ == "__main__":
    populate()
