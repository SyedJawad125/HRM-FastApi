from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def paginate_data(data, request):
    try:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end], len(data)
    except:
        return data, len(data)
    
from fastapi.responses import JSONResponse
def create_response(data, message, status_code):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": message,
            "result": data
        }
    )
from app import models

def filter_departments(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Department.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query



def filter_employees(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Employee.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query

def filter_ranks(params, query):
    title = params.get("title")
    if title:
        query = query.filter(models.Rank.title.ilike(f"%{title}%"))
    # Add more filters as needed
    return query

def filter_attendances(params, query):
    is_present = params.get("is_present")
    date = params.get("date")
    employee_id = params.get("employee_id")

    # Handle is_present filter
    if is_present is not None:
        is_present = is_present.lower()
        if is_present in ["true", "1"]:
            query = query.filter(models.Attendance.is_present == True)
        elif is_present in ["false", "0"]:
            query = query.filter(models.Attendance.is_present == False)

    # Handle date filter
    if date:
        try:
            # Optional: Validate the date format
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")  # Will raise ValueError if invalid
            query = query.filter(models.Attendance.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Handle employee_id filter
    if employee_id:
        try:
            query = query.filter(models.Attendance.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    return query


def filter_timesheets(params, query):
    date = params.get("date")
    employee_id = params.get("employee_id")
    attendance_id = params.get("attendance_id")

    if date:
        try:
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")
            query = query.filter(models.Timesheet.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if employee_id:
        try:
            query = query.filter(models.Timesheet.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if attendance_id:
        try:
            query = query.filter(models.Timesheet.attendance_id == int(attendance_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="attendance_id must be an integer.")

    return query
    
from fastapi import HTTPException
from sqlalchemy.orm import Query
from datetime import datetime

from app import models, schemas 
 # ✅ Keep this if enums are in the same schemas file


def filter_leave(params: dict, query: Query):
    status = params.get("status")
    leave_type = params.get("leave_type")
    employee_id = params.get("employee_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if status:
        if status not in [s.value for s in schemas.LeaveStatus]:  # ✅ Use schemas.LeaveStatus
            raise HTTPException(status_code=400, detail="Invalid leave status.")
        query = query.filter(models.Leave.status == status)

    if leave_type:
        if leave_type not in [lt.value for lt in schemas.LeaveType]:  # ✅ Use schemas.LeaveType
            raise HTTPException(status_code=400, detail="Invalid leave type.")
        query = query.filter(models.Leave.leave_type == leave_type)

    if employee_id:
        try:
            query = query.filter(models.Leave.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Leave.start_date >= start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(models.Leave.end_date <= end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

    return query



from fastapi.responses import JSONResponse
from app import models

def filter_permissions(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Permission.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query

from fastapi.responses import JSONResponse

def filter_roles(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Role.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query




import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email_notification(to_email: str, subject: str, message: str):
    sender_email = os.getenv("EMAIL_USER", "default@gmail.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "")
    email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port = int(os.getenv("EMAIL_PORT", 465))

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(email_host, email_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Failed to send email:", e)



# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "syedjawadali92@gmail.com"
# EMAIL_HOST_PASSWORD = "ctpgxfclwyucweni"