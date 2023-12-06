from flask_restful import Api,Resource,reqparse
from models import *
from sqlalchemy.exc import IntegrityError
from validation import *
from flask import make_response
import json

api=Api()

course_parser=reqparse.RequestParser()
course_parser.add_argument("course_name")
course_parser.add_argument("course_code")
course_parser.add_argument("course_description")

class CourseAPI(Resource):
    def get(self,id):
        
        try:
            c=Course.query.get(id)
            
            return {"course_id":c.course_id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description},200
                
    
                
        except Exception as e:
            return make_response("Course Not found!",404)
        




    def put(self,id):
        updates=course_parser.parse_args()
        
        try:
            c=Course.query.get_or_404(id)
        except Exception as e:
            return make_response("Course not found!",404)
        if updates["course_name"]=="":
            raise CourseValidationError(status_code=404,error_code="COURSE001",error_message="Course Name is required.")
        if updates["course_code"]=="":
            raise CourseValidationError(status_code=404,error_code="COURSE002",error_message="Course Code is required.")
        
        c.course_code=updates["course_code"]
        c.course_name=updates["course_name"]
        c.course_description=updates["course_description"]
        db.session.commit()
        
        return {"course_id":id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description}
    
    def delete(self,id):
        try:
            c=Course.query.get_or_404(id)
        
        except:
            
            raise NotFoundError(status_code=404,error_message="Course not found!")
            
        
        try:
            db.session.delete(c)
            db.session.commit()
        except:
            return make_response("",500)
        return make_response("",200)

            

    
    def post(self):
        updates=course_parser.parse_args()
        if updates["course_code"]=="":
            raise CourseValidationError(status_code=404,error_code="COURSE002",error_message="Course Code is required.")
        if updates["course_name"]=="":
            raise CourseValidationError(status_code=404,error_code="COURSE001",error_message="Course Name is required.")
        try:
            c=Course(course_name=updates["course_name"],course_code=updates["course_code"],course_description=updates["course_description"])
            db.session.add(c)
            db.session.commit()
        except IntegrityError :
            return make_response("course_code already exists",409)

        return make_response(json.dumps({"course_id":c.course_id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description}),201)
    
student_parser=reqparse.RequestParser()
student_parser.add_argument("first_name")
student_parser.add_argument("last_name")
student_parser.add_argument("roll_number")



class StudentAPI(Resource):
    def get(self,id):
        
        try:
            s=Student.query.get_or_404(id)
        except:
            raise NotFoundError(status_code=404,error_message="Student not found")
        
        try:
            return make_response(json.dumps({"student_id":s.student_id,"first_name":s.first_name,"last_name":s.last_name,"roll_number":s.roll_number}),200)
        except:
            return make_response("",500)
        
        
        
        
    def put(self,id):
        updates=student_parser.parse_args()
        
        try:
            s=Student.query.get_or_404(id)
        except:
            raise NotFoundError(status_code=404,error_message="Student not found")
        if updates["roll_number"]=="":
            raise StudentValidationError(status_code=400,error_code="STUDENT001",error_message="Roll number is required.")
        if updates["first_name"]=="":
            raise StudentValidationError(status_code=400,error_code="STUDENT002",error_message="first name is required.")
        try:
            s.roll_number=updates["roll_number"]
            s.first_name=updates["first_name"]
            s.last_name=updates["last_name"]
            db.session.commit()
        except:
            return make_response("",500)
        
        return make_response(json.dumps({"student_id":s.student_id,"first_name":s.first_name,"last_name":s.last_name,"roll_number":s.roll_number}),200)
    
    def delete(self,id):
        try:
            s=Student.query.get_or_404(id)
        except:
            raise NotFoundError(status_code=404,error_message="Student not found")
        
        try:
            db.session.delete(s)
            db.session.commit()
        except:
            return make_response("",500)
        return make_response("",200)
            
    
        
        
    def post(self):
        
        new_student=student_parser.parse_args()
        if new_student["first_name"]=="":
            raise StudentValidationError(status_code=400,error_code="STUDENT002",error_message="First name is required")
        if new_student["roll_number"]=="":
            raise StudentValidationError(status_code=400,error_code="STUDENT001",error_message="Roll number is required")
        try:
            s=Student(roll_number=new_student["roll_number"],first_name=new_student["first_name"],last_name=new_student["last_name"])
            db.session.add(s)
            db.session.commit()
        except IntegrityError:
            return make_response("Student already exists",409)
        try:
            return make_response(json.dumps({"student_id":s.student_id,"first_name":s.first_name,"last_name":s.last_name,"roll_number":s.roll_number}),201)
        except:
            return make_response("",500)
        
enrollment_parser=reqparse.RequestParser()
enrollment_parser.add_argument("course_id",type=int)

class EnrollmentAPI(Resource):
    def get(self,sid):
        try:
            s=Student.query.get_or_404(sid)
        except:
            raise EnrollmentValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")
        
        
        e=Enrollment.query.filter_by(estudent_id=sid).all()
        if len(e)==0:
            raise NotFoundError(status_code=404,error_message="Student is not enrolled in any course")
        else:
            message=[]
            for x in e:
                message.append({"enrollment_id":x.enrollment_id,"student_id":x.estudent_id,"course_id":x.ecourse_id})
            return make_response(json.dumps(message),200)   
    def post(self,sid):
        
        try:
            s=Student.query.get_or_404(sid)
        except:
            raise NotFoundError(status_code=404,error_message="Student not found")
        
        enrolling_data=enrollment_parser.parse_args()
        cid=enrolling_data["course_id"]
        try:
            c=Course.query.get_or_404(cid)
        except:
            raise EnrollmentValidationError(status_code=400,error_code="ENROLLMENT001",error_message="Course does not exist")
        try:
            
            e=Enrollment(estudent_id=s.student_id,ecourse_id=c.course_id)
            db.session.add(e)
            db.session.commit()
        except:
            return make_response("",500)
        return make_response(json.dumps([{"enrollment_id":e.enrollment_id,"course_id":e.ecourse_id,"student_id":e.estudent_id}]),200)
        
            
        

        
        
        
api.add_resource(CourseAPI,"/api/course/<int:id>","/api/course")
api.add_resource(StudentAPI,"/api/student","/api/student/<int:id>")
api.add_resource(EnrollmentAPI,"/api/student/<int:sid>/course","/api/student/<int:sid>/course/<int:cid>")