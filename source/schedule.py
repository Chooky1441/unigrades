import course

class Schedule:
    # a schedule is comprised of all the information about a students current class
    # schedule and academic standing (previous gpa etc..)
    def __init__(name: str, current_gpa: float, current_units: int, courses: [course.Course]):
        self.name = name
        self.current_gpa = current_gpa                         # the gpa the student had before the courses they are enrolled in
        self.current_units = current_units                     # the total units the student completed, excluding current courses
        self.courses = courses                                 # list of courses that the student is enrolled in
        self.projected_gpa = 0                                 # the estimated gpa based on the grades they are currently recieving
        self.projected_units = self.current_units              # the units the student will have completed at the end of this quarter/semester
                               + self._calc_courses_units()

    # private functions

    def _calc_courses_units(self) -> int:
        """returns the amount of units currently enrolled in"""
        return sum([c.units for c in self.courses])

    def _calc_projected_gpa() -> int:
        """returns the projected gpa based on course grades and the past gpa"""

    # public functions

    def add_course(c: course.Course):
        """adds a course to the schedule, updating any relevant information"""
        self.courses.add(c)
        self.projected_units += c.units

    def remove_course(c: course.Course):
        """removes the course from the schedule, removing any relecant information"""
        self.courses.remove(c)
        


    def to_dict() -> dict:
        """returns a dictionary contaning all the information in a schedule"""
        return {'name': name, 'current_gpa': current_gpa, 'current_units': current_units,
                'projected_gpa': projected_gpa, 'projected_units': projected_units}
