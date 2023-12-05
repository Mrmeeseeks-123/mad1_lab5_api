from flask_restful import Api,Resource,reqparse
from models import *
from sqlalchemy.exc import IntegrityError

api=Api()

parser=reqparse.RequestParser()
parser.add_argument("course_name")
parser.add_argument("course_code")
parser.add_argument("course_description")

class CourseAPI(Resource):
    def get(self,id):
        try:
            c=Course.query.get(id)
            
            return {"course_id":c.course_id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description},200
                
            #else:
                #return 404,"Course Not Found!"
                
        except Exception as e:
            print("error occured!")
            return {}




    def put(self,id):
        updates=parser.parse_args()
        
        try:
            c=Course.query.get_or_404(id)
        except Exception as e:
            return "Course not found!",404
        
        c.course_code=updates["course_code"]
        c.course_name=updates["course_name"]
        c.course_description=updates["course_description"]
        db.session.commit()
        
        return {"course_id":id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description},200
    
    def post(self):
        updates=parser.parse_args()
        try:
            c=Course(course_name=updates["course_name"],course_code=updates["course_code"],course_description=updates["course_description"])
            db.session.add(c)
            db.session.commit()
        except IntegrityError :
            return "course_code already exists",

        return {"course_id":c.course_id,"course_name":c.course_name,"course_code":c.course_code,"course_description":c.course_description},201
        
        
api.add_resource(CourseAPI,"/api/course/<int:id>","/api/course")