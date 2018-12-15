# I chose to have the following three classes in the course.py file since it
# wouldn't make sence to want a course without these objects, therefore I'm
# eliminating the option to do so by bundling them together


class Category:
    # a category is describes how assignemnts should be weighted in a course
    # if "Tests" are 50% of ones grade, then any assignemnts in the "Tests"
    # category will be multiplied by 0.50
    def __init__(self, name: str, weight: float):
        self.name = name        # name of the cateogry
        self.weight = weight    # weighting (% of total grade)

    def __str__(self) -> str:
        # used for printing to the console
        return f'Category {self.name} with a weight of {self.weight}'


class CutPointSet:

    class InvalidCutPointException(Exception):
        def __init__(self, key: str):
            print(f'Invalid CutPointSet key: {key}')

    # a cutpoint set describes the cut off points for grades in a class
    # so if a class doesnt use the typical 50 - 60 - 70 - 80 - 90 scale for
    # grading (i.e. it is curved) then this allows one to adjust for that
    def __init__(self, a = 93.5, aminus = 90, bplus = 86.5, b = 83.5, bminus = 80, cplus = 76.5,
                       c = 73.5, cminus = 70, dplus = 66.5, d = 63.5, dminus = 60):              # all values should be floats
        self._cuttoffdict = {'a': a, 'aminus': aminus, 'bplus': bplus, 'b': b, 'bminus': bminus,
                             'cplus': cplus, 'c': c, 'cminus': cminus, 'dplus': dplus, 'd': d, 'dminus': dminus}

    def __str__(self) -> str:
        # used for printing to the console
        s = '\n\t'.join(['{:>7}: {}'.format(k, v) for k, v in self._cuttoffdict.items()])
        return f'CutPointSet:\n\t{s}'


    def __getitem__(self, key: str):
        try:
            return self._cuttoffdict[key]
        except:
            raise InvalidCutPointException(key)

    def __iter__(self):
        def _gen():
            for k, v in self._cuttoffdict.items():
                yield (k, v)


class Assignemnt:

    def __init__(self, name: str, pts_rec: float, pts_total: float, category: Category):
        self.name = name            # name of the assignemnt
        self.pts_rec = pts_rec      # points recieved on the assignment
        self.pts_total = pts_total  # total points possible on the assignment
        self.category = category    # the category in the course that this assignment belongs to

    def __str__(self) -> str:
        # used for printing to the console
        return f'Assignment: {self.name}\n\t\tPoints Recieved: {self.pts_rec}\n\t\tPoints Total: {self.pts_total}\n\t\tCategory: {self.category.name}'


class Course:

    def __init__(self, name: str, units: int, cutpointset : CutPointSet, categories: [Category], assignments: [Assignemnt]):
        self.name = name
        self.units = units
        self.cutpointset = cutpointset
        self.categories = categories
        self.assignments = assignments

    def __str__(self) -> str:
        # used for printing to the console
        cats = '\n\t'.join([str(c) for c in self.categories])
        assigns = '\n\t'.join([str(a) for a in self.assignments])
        return f'Course {self.name}\n\tUnits: {self.units}\n\n\t{str(self.cutpointset)}\n\n\t{cats}\n\n\t{assigns}'
