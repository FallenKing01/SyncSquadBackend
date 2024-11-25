from Domain.extensions import open_session
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Utils.enums.role import Role
from Domain.Entities.grupa import Grupe
from Domain.Entities.examen import Examene

def add_student_repo(student_data,session):

    student = Student(student_data['id'], student_data['nume'], student_data['telefon'], student_data['facultatea'],student_data['specializarea'], student_data['idgrupa'], False)
    session.add(student)

def update_student(grupaId,studentId):

    try:

        session = open_session()

        existaSef = session.query(Student).filter(Student.idgrupa == grupaId, Student.sef == 1).first()

        if existaSef is None:

            student = session.query(Student).filter(Student.id == studentId).first()
            studentAcc = session.query(Utilizator).filter(Utilizator.id == studentId).first()

            student.sef = 1
            studentAcc.rol = Role.SEF.name.lower()

            session.commit()

            return {"message": "Student updated successfully"}

        else:

            currentSefId = existaSef.id
            currentSefAcc = session.query(Utilizator).filter(Utilizator.id == currentSefId).first()
            existaSef.sef = 0
            currentSefAcc.rol = Role.STUDENT.name.lower()

            session.query(Examene).filter(Examene.sefid == currentSefId).update(
                {Examene.sefid: studentId},
                synchronize_session=False
            )

            session.query(Student).filter(Student.id == studentId).update(
                {Student.sef: 1},
                synchronize_session=False
            )

            session.query(Utilizator).filter(Utilizator.id == studentId).update(
                {Utilizator.rol: Role.SEF.name.lower()},
                synchronize_session=False
            )

            session.commit()

        return {"message": "Student status updated successfully"}

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while updating student: {str(e)}")

    finally:

        session.close()



