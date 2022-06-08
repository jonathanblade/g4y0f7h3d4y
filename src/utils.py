from datetime import datetime


def calc_duration(duration: int, assignment_time: datetime | None) -> int:
    if assignment_time:
        return duration + int((datetime.utcnow() - assignment_time).total_seconds())
    else:
        return duration
