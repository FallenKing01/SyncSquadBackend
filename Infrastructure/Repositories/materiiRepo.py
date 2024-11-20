import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.extensions import session
from Domain.Entities.examen import Examene

def add_subject_repo(subject_data):

    subject = Materii(subject_data['id'], subject_data['nume'], subject_data['abreviere'],
                      subject_data['tipevaluare'], subject_data['numarcredite'], subject_data['profesorid'])

    session.add(subject)

def create_subject_repo(subject_data):

    subject_id = str(uuid.uuid4())

    try:

        profesor = session.query(Profesor).filter(Profesor.id == subject_data['profesorid']).first()

        if profesor is None:

            return {"error": "The professor does not exist"}, 204

        subject_data['id'] = subject_id
        add_subject_repo(subject_data)

        session.commit()

        return {"message": "Subject created successfully"}, 201

    except Exception as e:

        session.rollback()

        print(f"Error while inserting subject: {e}")
        raise Exception(f"Error while inserting subject: {str(e)}")


def get_subjects_of_profesor_repo(profesorId):

    try:

        subjects = session.query(Materii).filter(Materii.profesorid == profesorId).all()
        subjects_list = []

        if not subjects:

            return subjects_list, 204

        for subject in subjects:

            subject_dict = {
                "subjectId": subject.id,
                "nume": subject.nume,
                "abreviere" : subject.abreviere,
                "tipEvaluare" : subject.tipevaluare,
                "numarCredite" : subject.numarcredite,
            }

            subjects_list.append(subject_dict)

        return subjects_list

    except Exception as e:

        raise Exception(f"Error while getting subjects of professor: {str(e)}")

def delete_subject_repo(idMaterie):

    try:

         subject = session.query(Materii).filter(Materii.id == idMaterie).first()

         if subject is None:

                return {"error": "The subject does not exist"}, 204

         session.delete(subject)
         session.commit()

         return {"message": "Subject deleted successfully"}, 200

    except Exception as e:

            session.rollback()

            raise Exception(f"Error while deleting subject: {str(e)}")

def update_subject_repo(idMaterie, subject_data):

    try:

        # Găsește materia după ID
        subject = session.query(Materii).filter(Materii.id == idMaterie).first()

        if subject is None:
            return {"error": "The subject does not exist"}, 204

        # Verifică dacă profesorul există în baza de date
        if 'profesorid' in subject_data:
            profesor = session.query(Profesor).filter(Profesor.id == subject_data['profesorid']).first()
            if profesor is None:
                raise Exception(f"Profesor with ID {subject_data['profesorid']} does not exist")

        # Actualizează câmpurile materiei
        subject.nume = subject_data.get('nume', subject.nume)
        subject.abreviere = subject_data.get('abreviere', subject.abreviere)
        subject.tipevaluare = subject_data.get('tipevaluare', subject.tipevaluare)
        subject.numarcredite = subject_data.get('numarcredite', subject.numarcredite)
        subject.profesorid = subject_data.get('profesorid', subject.profesorid)

        # Salvează modificările
        session.commit()

        return {"message": "Subject updated successfully"}, 200

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while updating subject: {str(e)}")

def get_materii_examene_neprogramate_repo(profesorId, studentId):

    try:

        subjects = session.query(Materii).filter(Materii.profesorid == profesorId).all()
        subjects_list = []

        examene = session.query(Examene).filter(Examene.sefid == studentId).all()

        materii_cu_examene_ids = []

        for examen in examene:

            materii_cu_examene_ids.append(examen.materieid)

        for subject in subjects:

                if subject.id not in materii_cu_examene_ids:

                    subject_dict = {
                        "subjectId": subject.id,
                        "nume": subject.nume,
                        "abreviere" : subject.abreviere,
                        "tipEvaluare" : subject.tipevaluare,
                        "numarCredite" : subject.numarcredite,
                    }

                    subjects_list.append(subject_dict)

        return subjects_list

    except Exception as e:

        raise Exception(f"Error while getting subjects of professor: {str(e)}")