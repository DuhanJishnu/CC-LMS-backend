from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import ARRAY
# Create db instance without app
db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'
    course_code = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String , nullable=False)
    
    # Relationships
    exams = db.relationship('Exam', backref='course', cascade="all, delete-orphan")
    enrollments = db.relationship('Enrollment', backref='course', cascade="all, delete-orphan")
    
    def json(self):
        return {
            'course_code': self.course_code,
            'course_name': self.course_name,
            'created_by': self.user_id
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    _id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_code = db.Column(db.String(20), db.ForeignKey('courses.course_code'))
    user_id = db.Column(db.String , nullable=False)
    
    def json(self):
        return {
            'course_code': self.course_code,
            'student_id': self.user_id
        }

class Exam(db.Model):
    __tablename__ = 'exams'
    exam_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_code = db.Column(db.String(20), db.ForeignKey('courses.course_code'))
    exam_type = db.Column(db.String(50), nullable=False)
    exam_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String , nullable=False)
    pyq_pdf = db.Column(db.String(500), nullable=True)
    
    # Relationships
    syllabus_items = db.relationship('SyllabusItem', backref='exam', cascade="all, delete-orphan")
    
    def json(self):
        return {
            'exam_id': self.exam_id,
            'course_code': self.course_code,
            'exam_type': self.exam_type,
            'exam_date': self.exam_date.isoformat(),
            'created_by': self.user_id
        }

class SyllabusItem(db.Model):
    __tablename__ = 'syllabus_items'
    item_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id = db.Column(db.String, db.ForeignKey('exams.exam_id'))
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String , nullable=False)
    completers = db.Column(ARRAY(db.String), nullable = True, default=[])
    
    def json(self):
        return {
            'item_id': self.item_id,
            'exam_id': self.exam_id,
            'description': self.description,
            'created_by': self.user_id,
            'completers': self.completers,
            'completers_len': len(self.completers)
        }


class Update(db.Model):
    __tablename__ = 'updates'
    update_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(512), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def json(self):
        return {
            'update_id': self.update_id,
            'title': self.title,
            'link': self.link,
            'sequence': self.sequence,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }