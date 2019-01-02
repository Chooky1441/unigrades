import course, schedule_loader, utils

class Schedule:
    # a schedule is comprised of all the information about a students current class
    # schedule and academic standing (previous gpa etc..)
    def __init__(self, name: str, current_gpa: float, current_units: int, courses: [course.Course]):
        self.name = name
        self.current_gpa = current_gpa                         # the gpa the student had before the courses they are enrolled in
        self.current_units = current_units                     # the total units the student completed, excluding current courses
        self.courses = courses                                 # list of courses that the student is enrolled in
        self.projected_gpa =  self._calc_projected_gpa()       # the estimated gpa based on the grades they are currently recieving
        self.projected_units = self._calc_courses_units()      # the units the student will have completed at the end of this quarter/semester

    # private functions

    def _calc_courses_units(self) -> int:
        """returns the amount of units currently enrolled in"""
        return sum([c.units for c in self.courses])

    def _calc_projected_gpa(self) -> float:
        """returns the projected gpa based on course grades and the past gpa"""
        temp_gpa = self.current_gpa
        for c in self.courses:
            temp_gpa = self._add_one_course_to_gpa(c, temp_gpa)
        return temp_gpa

    def _add_one_course_to_gpa(self, c: course.Course, gpa: float) -> float:
        """returns the gpa with one course added"""
        return gpa if c.letter_grade() == 'N/A' else gpa * (self.current_units / (self.current_units + c.units)) + utils.to_gpa(c.letter_grade()) * (c.units / (self.current_units + c.units))

    # public functions

    def add_course(self, c: course.Course):
        """adds a course to the schedule, updating any relevant information"""
        self.courses.append(c)
        self.projected_units += c.units

    def remove_course(self, c: course.Course):
        """removes the course from the schedule, removing any relecant information"""
        self.courses.remove(c)
        self.projected_gpa = self._calc_projected_gpa()
        self.projected_units -= c.units

    def complete_course(self, c: course.Course):
        """removes the course form the schedule aswell as adding re-calculating the schedule stats"""
        if c.p_np is False: # only add to the gpa if the course is not a pass no pass grade
            self.current_gpa  = self._add_one_course_to_gpa(c, self.current_gpa)
        self.current_units += c.units
        self.projected_units -= c.units
        self.remove_course(c)

    def to_dict(self) -> dict:
        """returns a dictionary contaning all the information in a schedule"""
        return {'name': self.name, 'current_gpa':self. current_gpa, 'current_units': self.current_units,
                'courses': [c.to_dict() for c in self.courses]}

    def save(self) -> dict:
        """saves the schedule to the schedules folder"""
        schedule_loader.save_schedule(self)
