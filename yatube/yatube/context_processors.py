import datetime as dt


def year(request):
    year_now = dt.datetime.today().year
    return {"year": year_now}
