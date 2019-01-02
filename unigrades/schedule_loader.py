from schedule import Schedule
import course, utils
import json, pathlib

def get_all_schedule_names() -> [str]:
    """returns a list of all the name of the saved schedules"""
    return sorted([dir.stem for dir in pathlib.Path('schedules').iterdir() if dir.is_file()], key = lambda x: x.lower())


def get_schedule_dict(name: str) -> dict:
    """returns a dict with all the data for a schedule"""
    file = None
    try:                                                 # if the file cannot be opened then the appropriate error will be raised
        file = open(pathlib.Path(f'schedules/{name}.json'), 'r')
    except:
        raise utils.ScheduleLoadError('Failed to load schedule.')
    else:
        with file as f:
            sch_dict = json.load(f)
        return sch_dict

def load_schedule(name: str) -> Schedule:
    """converts the dict gotten from the json file into a schedule object"""
    s = get_schedule_dict(name)
    courses = []
    for c in s['courses']:
        rcps = c['cutpointset']
        cps = course.CutPointSet(rcps['a'], rcps['aminus'],
                                 rcps['bplus'], rcps['b'], rcps['bminus'],
                                 rcps['cplus'], rcps['c'], rcps['cminus'],
                                 rcps['dplus'], rcps['d'], rcps['dminus'])
        cats = []
        for cat in c['categories']:
            assignments = []

            for a in cat['assignments']:
                a.append(course.Assignment(a['name'], a['pts_rec'], a['pts_total']))

            cats.append(course.Category(cat['name'], cat['weight'], assignments))
        courses.append(course.Course(c['name'], c['units'], cps, cats, c['p_np']))

    return Schedule(s['name'], s['current_gpa'], s['current_units'], courses)


def save_schedule(schedule: Schedule) -> None:
    """saves the schedule"""
    file = open(pathlib.Path(f'schedules/{schedule.name}.json'), 'w')  # if the file cannot be opened then the appropriate error will be raised
    with file as f:
        try:
            json.dump(schedule.to_dict(), f)
        except:
            raise utils.ScheduleSaveError('Failed to save schedule.')
        finally:
            file.close()

def delete_schedule(name: str) -> None:
    """trys to delete the given schedule, if it can not be found an error is raised"""
    try:
        pathlib.Path(f'schedules/{name}.json').unlink()
    except:
        raise utils.ScheduleDeleteError('Failed to delete schedule.')
