DEFAULT_TRANSITION_LENGTH = 0.15

TO_GPA = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}

def to_gpa(grade: str) -> float:
    """returns the gpa the student has based on the letter grade (4.0 scale)"""
    return TO_GPA[grade]

# custom exceptions
class InvalidCutPointException(Exception):
    def __init__(self, key: str):
        print(f'Invalid CutPointSet key: {key}')

class InvalidCategoryException(Exception):
    def __init__(self, c: str):
        print(f'Invalid category {c}.')

class ScheduleLoadError(Exception):
    def __init__(self, message: str):
        self.message = message

class ScheduleSaveError(Exception):
    def __init__(self, message: str):
        self.message = message
