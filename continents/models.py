from cities.models import City

CODES = (
    ('NA', 'North America'),
    ('SA', 'South America'),
    ('EU', 'Europe'),
    ('AS', 'Asia'),
    ('OC', 'Oceania'),
    ('AF', 'Africa'),
)

class Continent(object):
    
    def __init__(self, code, name):
        self.name = name
        self.code = code

    def __unicode__(self):
        return self.name

    def cities(self):
        return City.objects.filter(country__continent=self.code).order_by('-population')[:13]


CONTINENTS = [Continent(code[0], code[1]) for code in CODES]
