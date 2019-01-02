# I chose to have the following three classes in the course.py file since it
# wouldn't make sence to want a course without these objects, therefore I'm
# eliminating the option to do so by bundling them together

class CutPointSet:
    # a cutpoint set describes the cut off points for grades in a class
    # so if a class doesnt use the typical 50 - 60 - 70 - 80 - 90 scale for
    # grading (i.e. it is curved) then this allows one to adjust for that
    def __init__(self, a = 93.5, aminus = 90, bplus = 86.5, b = 83.5, bminus = 80, cplus = 76.5,
                       c = 73.5, cminus = 70, dplus = 66.5, d = 63.5, dminus = 60):              # all values should be floats
        self.a = a
        self.aminus = aminus
        self.bplus = bplus
        self.b = b
        self.bminus = bminus
        self.cplus = cplus
        self.c = c
        self.cminus = cminus
        self.dplus = dplus
        self.d = d
        self.dminus = dminus

    def __str__(self) -> str:
        # used for printing to the console
        s = '\n\t'.join(['{:>7}: {}'.format(k, v) for k, v in self.to_dict().items()])
        return f'CutPointSet:\n\t{s}'

    def str_list(self):
        return [str(self.a), str(self.aminus),
                str(self.bplus), str(self.b), str(self.bminus),
                str(self.cplus), str(self.c), str(self.cminus),
                str(self.dplus), str(self.d), str(self.dminus)]

    def __getitem__(self, perc: float) -> str:
        # will return a letter grade given a percentage
        if perc is None:
            return 'N/A'
        elif perc >= self.a:
            return 'A'
        elif perc >= self.aminus:
            return 'A-'
        elif perc >= self.bplus:
            return 'B+'
        elif perc >= self.b:
            return 'B'
        elif perc >= self.bminus:
            return 'B-'
        elif perc >= self.cplus:
            return 'C+'
        elif perc >= self.c:
            return 'C'
        elif perc >= self.cminus:
            return 'C-'
        elif perc >= self.dplus:
            return 'D+'
        elif perc >= self.d:
            return 'D'
        elif perc >= self.dminus:
            return 'D-'
        else:
            return 'F'

    def to_dict(self) -> dict:
        """returns a dictionary with all of the data representing a cuttpointset"""
        # used when saving as a json file
        return  {'a': self.a, 'aminus': self.aminus, 'bplus': self.bplus, 'b': self.b, 'bminus': self.bminus,
                 'cplus': self.cplus, 'c': self.c, 'cminus': self.cminus, 'dplus': self.dplus, 'd': self.d, 'dminus': self.dminus}


class Assignment:

    def __init__(self, name: str, pts_rec: float = None, pts_total: float = None):
        self.name = name            # name of the assignment
        self.pts_rec = pts_rec      # points recieved on the assignment
        self.pts_total = pts_total  # total points possible on the assignment

    def __str__(self) -> str:
        # used for printing to the console
        return f'Assignment: {self.name}\n\t\tPoints Recieved: {self.pts_rec}\n\t\tPoints Total: {self.pts_total}'

    def percent(self) -> float:
        """returns the percent grade recieved"""
        return (self.pts_rec / self.pts_total) * 100

    def is_graded(self) -> bool:
        """returns true if the assignment has a grade"""
        return False if self.pts_rec is None else True

    def to_dict(self) -> dict:
        """returns a dictionary with all of the data representing an assignment"""
        # used when saving as a json file
        return {'name': self.name, 'pts_rec': self.pts_rec, 'pts_total': self.pts_total}


class Category:
    # a category is describes how assignemnts should be weighted in a course
    # if "Tests" are 50% of ones grade, then any assignemnts in the "Tests"
    # category will be multiplied by 0.50
    def __init__(self, name: str, weight: float, assignments: [Assignment] = []):
        self.name = name        # name of the cateogry
        self.weight = weight    # weighting (% of total grade)
        self.assignments = assignments

    def __str__(self) -> str:
        # used for printing to the console
        assigns = '\n\t\t'.join([f'Name: {a.name}, Percent: {a.percent()}' for a in self.assignments])
        return f'Category {self.name} with a weight of {self.weight}\n\tAssignments:\n\t\t{assigns}'

    def grade(self) -> float:
        """returns the percentage (out of 100) recieved in this catagory"""
        return None if len(self.assignments) == 0 else sum([a.percent() for a in self.assignments]) / len(self.assignments)

    def to_dict(self) -> dict:
        """returns a dictionary with all of the data representing a Cateogry"""
        # used when saving as a json file
        return {'name':self.name, 'weight':self.weight, 'assignments': [a.to_dict() for a in self.assignments]}



class Course:

    def __init__(self, name: str, units: int, cutpointset : CutPointSet, categories: [Category], p_np: bool = False):
        self.name = name
        self.units = units
        self.cutpointset = cutpointset
        self.categories = categories
        if self.categories == []:
            self.categories.append(categories('General', 100))
        self.grade_ = self.grade()
        self.p_np = p_np        # 'pass no pass' is used if the student doesnt want a letter grade for the class

    # public functions

    def __str__(self) -> str:
        # used for printing to the console
        cats = '\n\t'.join([str(c) for c in self.categories])
        return f'Course {self.name}\n\tUnits: {self.units}\n\n\t{str(self.cutpointset)}\n\n\t{cats}'

    def add_assignment(category: str, a: Assignment):
        """adds the assignment to the category, if the category does not exist than an error is raised"""
        for c in self.categories:
            if c.name == category:
                c.assignments.append(a)     # if the category can be found, add the assignment to the
                self.grade_ = self.grade()  # category and re-calculate the expected grade
                break
        else:
            raise utils.InvalidCategoryException(category)

    def letter_grade(self) -> str:
        """returns the letter grade the student currently has in the course"""
        return self.cutpointset[self.grade_]

    def grade(self) -> float:
        """calculates the grade a student has in the course"""
        total_cat_perc, cat_perc = 0, 0
        for c in self.categories:
            grade = c.grade()
            if grade is not None:
                cat_perc += grade
                total_cat_perc += c.weight
        return None if total_cat_perc == 0 else cat_perc / total_cat_perc

    def add_category(self, c: Category) -> None:
        """adds the category to the course and sorts the list"""
        self.categories = sorted(self.categories + [c], key = lambda x: x.name)

    def to_dict(self) -> dict:
        """returns a dictionary with all of the data representing a Course"""
        return {'name': self.name, 'units': self.units, 'cutpointset': self.cutpointset.to_dict(), 'categories': [c.to_dict() for c in self.categories], 'p_np': self.p_np}
