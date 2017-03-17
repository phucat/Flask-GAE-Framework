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
        self.error_code = 'S002'
        self.message = "Missing data for employee with id %s" % employee_id


class EmailAlreadyExistException(CustomException):
    def __init__(self):
        self.status_code = 500
        self.error_code = 'S002'
        self.message = "Email already exist"
