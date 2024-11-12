from Domain.extensions import session
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Utils.enums.role import Role
def update_student(studentId):

    try:

        student = session.query(Student).filter_by(id=studentId).first()

        if not student:
            return {"error": "Student not found"}, 404

        studentAcc = session.query(Utilizator).filter_by(id=studentId).first()

        if(studentAcc is None):
            return {"error": "Student account not found"}, 404

        studentAcc.rol = Role.SEF.name.lower()
        student.sef = True

        session.commit()

        return {"message": "Student status updated successfully"}

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while updating student: {str(e)}")


def get_profesori():

    try:

        profesori = session.query(Profesor).all()

        profesori_list = []

        for prof in profesori:

            profesori_list.append({
                "id": prof.id,
                "nume": prof.nume,
                "telefon": prof.telefon,
                "departament": prof.departament
            })

        return profesori_list

    except Exception as e:
        raise Exception(f"Error while getting profesori: {str(e)}")

