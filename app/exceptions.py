"""
# Put here all exceptions that will be thrown by your application
# It is recommended that an Exception should be raise on every request that does NOT satisfy the requirement of endpoint
# eg:
# on /api/guestbook/create if the email address already exist. the endpoint will raise EmailAlreadyExistException()
# which will be converted automatically to json response
"""


class CustomException(Exception):
    status_code = 400
    payload = None

    def __init__(self, desc, code):
        Exception.__init__(self)
        if code is not None:
            self.status_code = code

        self.message = desc
        self.payload = None

    def __str__(self):
        return self.message

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class SampleException(CustomException):
    def __init__(self, employee_id):
        self.status_code = 200
        self.message = "Missing data for employee with id %s" % employee_id


class EmailAlreadyExistException(CustomException):
    def __init__(self):
        self.status_code = 500
        self.message = "Email already exist"


class ForbiddenException(CustomException):
    def __init__(self, message="Forbidden"):
        self.status_code = 403
        self.message = message