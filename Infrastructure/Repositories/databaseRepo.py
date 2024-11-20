from Domain.extensions import session
from Utils.constants import SALI_URL,PROFESORI_URL
import requests
import uuid
from Domain.Entities.sala import Sali
from Domain.Entities.profesor import Profesor

def insert_database_sali_from_api_repo():
    response = requests.get(SALI_URL)
    data_list = response.json()

    try:
        for record in data_list:
            # Skip the record if 'name' is None or 'shortName' is empty
            if record.get('name') is None or record.get('shortName') == '':
                continue  # Skip this record

            record["departament"] = None
            sali_entry = Sali(
                str(uuid.uuid4()),
                record['name'],
                record['departament'],
                record['shortName'],
                record['buildingName']
            )
            print("am intrat aici")
            session.add(sali_entry)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

import requests
import uuid
from sqlalchemy.orm import sessionmaker

def insert_profesori_from_api_repo():
    response = requests.get(PROFESORI_URL)
    data_list = response.json()

    try:
        # Initialize a counter to keep track of inserted records
        count = 0

        for record in data_list:
            # Check the facultyName condition and ensure we're within the first 50
            if (
                record.get('facultyName') == "Facultatea de Inginerie Electrică şi Ştiinţa Calculatoarelor"
                and count < 50
            ):
                # Trim lastName and firstName, and check validity
                last_name = record.get('lastName', '').strip()
                first_name = record.get('firstName', '').strip()

                if not last_name or not first_name:  # Skip if either is empty after trimming
                    continue

                # Construct the fullName
                full_name = f"{last_name} {first_name}"

                # Create a new Profesor entry
                profesor_entry = Profesor(
                    str(uuid.uuid4()),  # Generate a unique ID
                    full_name,          # Use the constructed fullName
                    None,               # Optional fields, adjust as needed
                    None
                )

                # Add the entry to the session
                session.add(profesor_entry)

                # Increment the counter
                count += 1

        # Commit the transaction after processing
        session.commit()

    except Exception as e:
        # Rollback the transaction in case of an error
        session.rollback()
        print(f"An error occurred: {e}")
