import course

class UniGrades():
    def __init__(self):
        c1 = course.Category('Exams', 100)
        a1 = course.Assignemnt('Final', 90, 100, c1)
        co = course.CutPointSet()
        c = course.Course('ICS 46', 4, co, [c1], [a1])
        print(c)


if __name__ == '__main__':
    UniGrades()
