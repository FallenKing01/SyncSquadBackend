import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.extensions import session

def add_subject_repo(subject_data):

    subject = Materii(subject_data['id'], subject_data['nume'], subject_data['abreviere'],
                      subject_data['tipevaluare'], subject_data['numarcredite'], subject_data['profesorid'])

    session.add(subject)

def create_subject_repo(subject_data):

    subject_id = str(uuid.uuid4())

    try:

        profesor = session.query(Profesor).filter(Profesor.id == subject_data['profesorid']).first()

        if profesor is None:

            return {"error": "The professor does not exist"}, 404

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
            return subjects_list, 404

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
