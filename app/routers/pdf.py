from fastapi import APIRouter,Depends,HTTPException,status
from fpdf import FPDF
from app.database import get_db
from app.oauth2 import get_current_user
from sqlalchemy.orm import Session
from app import models
from reportlab.pdfgen import canvas

router = APIRouter()

@router.get('/profile_to_pdf')
def profile_to_pdf(db:Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    profile_data = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    user_data = db.query(models.User).filter(models.User.id == current_user.id).first()
    email_data = db.query(models.Email).filter(models.Email.id == current_user.email_id).first()
    if profile_data is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "data not found")
    data = {
        'First Name': user_data.first_name,
        'Last Name': user_data.last_name,
        'Phone Number': user_data.phone_number,
        'Date of Birth': profile_data.date_of_birth.strftime("%d %b,%y"),
        'address': profile_data.address,
        'Highest Qualification': profile_data.highest_qualification,
        'Email': email_data.user_email
    }

    # pdf = FPDF()

    # # Add a page
    # pdf.add_page()

    # # Set font and font size
    # pdf.set_font("Arial", size=12)

    # # Write profile data to the PDF
    # for key, value in data.items():
    #     pdf.cell(0, 10, txt=f"{key}: {value}",ln=True)

    # # Save the PDF to a file
    # pdf_name = "profile.pdf"
    # pdf_path = f'C:/Users/CS0142303/Desktop/Python/UserAccountWithUUID/{pdf_name}'
    # pdf.output(pdf_path)

    # return {
    #     "file_name":pdf_name,
    #     "file_path":pdf_path
    # }


    # Create a new PDF file
    pdf_name = "profile.pdf"
    pdf_path = f'C:/Users/CS0142303/Desktop/Python/UserAccountWithUUID/{pdf_name}'
    c = canvas.Canvas(pdf_path)

    # Set font and font size
    c.setFont("Helvetica", 12)

    # Write profile data to the PDF
    y = 700
    for key, value in data.items():
        c.drawString(50, y, f"{key}: {value}")
        # for new line
        y -= 30

    # Save and close the PDF file
    c.save()

    return {
        "file_name":pdf_name,
        "file_path":pdf_path
    }


