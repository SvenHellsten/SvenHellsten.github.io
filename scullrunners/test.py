def date_to_nth_day():
	new_year_day = datetime.datetime(year=date.year, month=1, day=1)
	return (date.today() - new_year_day).days + 1