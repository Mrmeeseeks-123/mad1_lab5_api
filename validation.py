from werkzeug.exceptions import HTTPException
from flask import make_response
import json






class CourseValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message={"error_code":error_code,"error_message":error_message}
        self.response=make_response(json.dumps(message),status_code)

class NotFoundError(HTTPException):
    def __init__(self,status_code,error_message):
        self.response=make_response(error_message,status_code)

class StudentValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message={"error_code":error_code,"error_message":error_message}
        self.response=make_response(json.dumps(message),status_code)
        
class EnrollmentValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message={"error_code":error_code,"error_message":error_message}
        self.response=make_response(json.dumps(message),status_code)