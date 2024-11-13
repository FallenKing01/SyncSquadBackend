from Domain.extensions import session
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Utils.enums.role import Role

def add_student_repo(student_data):

    student = Student(student_data['id'], student_data['nume'], student_data['telefon'], student_data['facultatea'],student_data['specializarea'], student_data['idgrupa'], False)
    session.add(student)

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



