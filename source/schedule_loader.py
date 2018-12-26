from schedule import schedule
import json, pathlib

def get_schedule_dict(name: str) -> dict:
    """returns a dict with all the data for a schedule"""
    file = None
    try:                                                 # if the file cannot be opened then the appropriate error will be raised
        file.open(f'schedules/{name}.json', 'r')
    except:
        raise utils.ScheduleLoadError('Failed to load schedule')
    else:
        with file as f:
            sch_dict = json.load(f)
        return sch_dict


def save_schedule(schedule: Schedule) -> None:
    """saves the schedule"""
    file = open(f'schedules/{schedule.name}.json', 'w')  # if the file cannot be opened then the appropriate error will be raised
    with file as f:
        try:
            json.dump(schedule.to_dict(), f)
        except:
            raise utils.ScheduleSaveError('Failed to save schedule')
        finally:
            file.close()