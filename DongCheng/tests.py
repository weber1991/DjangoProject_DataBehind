from django.test import TestCase



# Create your tests here.

def get_year(year):
    import datetime  
    year_date = datetime.datetime(year=int(year), month=1, day=1, hour=0, second=0)
    return year_date

if __name__ == '__main__':
    print(get_year(2019))
    print(type(get_year(2019)))
