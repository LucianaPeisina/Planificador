# calendarapp/utils.py
from calendar import HTMLCalendar
from .models import Comida


class Calendario(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendario, self).__init__()


    # filter comidas por doa
    def formatday(self, day, comidas):
        comidas_per_day = comidas.filter(start_time__day=day)
        d = ""
        for comida in comidas_per_day:
            d += f"<li> {comida.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, comidas):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, comidas)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter comidas by year and month
    def formatmonth(self, withyear=True):
        comidas = Comida.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )
        cal = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )  # noqa
        cal += (
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, comidas)}\n"
        return cal
