from sqlalchemy.exc import SQLAlchemyError

from Domain.extensions import open_session
from Utils.constants import SALI_URL,PROFESORI_URL,GRUPE_URL
import requests
import uuid
from Domain.Entities.sala import Sali
from Domain.Entities.examen import Examene
from Domain.Entities.profesor import Profesor
from Domain.Entities.grupa import Grupe
from Domain.Entities.student import Student
from Domain.Entities.materie import Materii
from Domain.Entities.saliCereri import SaliCereri
from Domain.Entities.utilizator import Utilizator
from fpdf import FPDF
import os
from Utils.passwordhash import hash_password
import random

class PDF(FPDF):
    def header(self):
        # Set font
        self.set_font('Arial', 'B', 12)
        # Title
        self.cell(0, 10, 'University Exam Schedule', border=False, ln=True, align='C')
        self.ln(10)  # Line break

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def insert_database_sali_from_api_repo():

    response = requests.get(SALI_URL)
    data_list = response.json()

    try:

        session = open_session()

        for record in data_list:

            if record.get('name') is None or record.get('shortName') == '':

                continue

            record["departament"] = None
            sali_entry = Sali(
                str(uuid.uuid4()),
                record['name'],
                record['departament'],
                record['shortName'],
                record['buildingName']
            )

            session.add(sali_entry)

        session.commit()

    except Exception as e:

        session.rollback()

    finally:

        session.close()

def insert_grupe_repo():
    """
    Fetch group data from an API and insert unique groups into the database.
    Only groups with specializationShortName == "C" are considered.
    """
    try:
        response = requests.get(GRUPE_URL)
        response.raise_for_status()  # Raise exception for HTTP errors
        data_list = response.json()  # Parse JSON response


        session = open_session()
        group_list = []

        for record in data_list:
            if record.get("specializationShortName") == "C":  # Filter only 'C' groups
                group_name = record.get("groupName")
                group_id = str(record.get("id"))  # Ensure ID is a string

                # Check if the group is already in the list
                if not any(gr["groupName"] == group_name for gr in group_list):
                    # Add the group to the local list to track uniqueness
                    group_list.append({"groupName": group_name, "id": group_id})

                    # Insert the group into the database
                    grupa = Grupe(id=group_id, grupa=group_name)
                    session.add(grupa)

        session.commit()

    except Exception as e:

        session.rollback()

    finally:
        session.close()

def insert_profesori_from_api_repo():

    response = requests.get(PROFESORI_URL)
    data_list = response.json()
    departamente = ["Calculatoare","Automatica","Electronica"]

    try:
        session = open_session()
        count = 0

        for record in data_list:

            if (
                record.get('facultyName') == "Facultatea de Inginerie Electrică şi Ştiinţa Calculatoarelor"
                and count < 50
            ):
                # Extract and clean data
                last_name = record.get('lastName', '').strip()
                first_name = record.get('firstName', '').strip()
                email = record.get('emailAddress', '').strip()  # Use correct email key

                # Skip records with missing names or emails
                if not last_name or not first_name or not email:
                    continue

                # Generate unique ID for both tables
                ##profesor_id = str(uuid.uuid4())
                profesor_id = str(record.get('id'))
                full_name = f"{last_name} {first_name}"

                # Insert into Profesor table
                profesor_entry = Profesor(
                    id=profesor_id,
                    nume=full_name,
                    telefon=None,  # Default to None
                    departament=random.choice(departamente)
                )
                session.add(profesor_entry)

                # Insert into Utilizator table
                password = hash_password("parola").decode('utf-8')
                utilizator_entry = Utilizator(
                    id=profesor_id,
                    email=email,
                    parola=password,
                    rol="profesor"
                )
                session.add(utilizator_entry)

                count += 1

        session.commit()

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()  # Rollback in case of error

    finally:
        session.close()
        print("Session closed.")



def generate_pdf_secretariat_repo():

    try:
        session = open_session()

        examene = session.query(Examene).filter(Examene.starea == "approved").order_by(Examene.data,Examene.orastart).all()
        examene_list = []

        for examen in examene:
            # Fetch related data from the database
            profesor_db = session.query(Profesor).filter(Profesor.id == examen.profesorid).first()
            nume_titular = profesor_db.nume
            asistent_db = session.query(Profesor).filter(Profesor.id == examen.asistentid).first()
            nume_asistent = asistent_db.nume
            sef_db = session.query(Student).filter(Student.id == examen.sefid).first()
            grupa_db = session.query(Grupe).filter(Grupe.id == sef_db.idgrupa).first()
            nume_grupa = grupa_db.grupa
            disciplina_db = session.query(Materii).filter(Materii.id == examen.materieid).first()
            nume_disciplina = disciplina_db.nume
            sali_cerere_db = session.query(SaliCereri).filter(SaliCereri.idcerere == examen.id).all()
            sala_db = session.query(Sali).filter(Sali.id == sali_cerere_db[0].idsala).first()
            nume_sala = sala_db.nume
            ora_start = examen.orastart
            ora_final = examen.orafinal
            data = examen.data
            examene_list.append({
                "nume_grupa": nume_grupa,
                "nume_disciplina": nume_disciplina,
                "nume_titular": nume_titular,
                "nume_asistent": nume_asistent,
                "data": data,
                "ora_start": ora_start,
                "ora_final": ora_final,
                "nume_sala": nume_sala,
            })

        # Generate PDF
        pdf = FPDF(orientation='L', format='A4')
        pdf.add_page()

        # Add title to the PDF
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "EXAMENE USV CALCULATOARE", 0, 1, 'C')  # Centered title
        pdf.ln(5)  # Add a small space after the title

        # Add table header
        pdf.set_font("Arial", size=8)
        pdf.set_fill_color(200, 220, 255)
        headers = ["Group", "Discipline", "Titular", "Assistant", "Date", "Start Time", "End Time", "Room"]
        column_widths = [25, 50, 30, 30, 25, 20, 20, 25]  # Adjusted column widths for better fit

        # Center header row
        for i, header in enumerate(headers):
            pdf.cell(column_widths[i], 8, header, border=1, fill=True, align='C')
        pdf.ln()

        pdf.set_font("Arial", size=8)
        for row in examene_list:
            pdf.cell(column_widths[0], 8, row["nume_grupa"], border=1, align='C')
            pdf.cell(column_widths[1], 8, row["nume_disciplina"], border=1, align='C')
            pdf.cell(column_widths[2], 8, row["nume_titular"], border=1, align='C')
            pdf.cell(column_widths[3], 8, row["nume_asistent"], border=1, align='C')
            pdf.cell(column_widths[4], 8, str(row["data"]), border=1, align='C')
            pdf.cell(column_widths[5], 8, str(row["ora_start"]), border=1, align='C')
            pdf.cell(column_widths[6], 8, str(row["ora_final"]), border=1, align='C')
            pdf.cell(column_widths[7], 8, row["nume_sala"], border=1, align='C')
            pdf.ln()

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        pdf_path = os.path.join(downloads_path, "examene_list.pdf")

        pdf.output(pdf_path)
        print(f"PDF saved successfully at {pdf_path}")

    except Exception as e:

        session.rollback()

    finally:

        session.close()


