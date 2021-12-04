import re
from backend.database_mysql import get_category_attribute_options

def parse_chart_type(info, expression):
    if "pie chart" in expression:
        info["chart_type"] = "pie chart"
    elif "bar chart" in expression:
        info["chart_type"] = "bar chart"
    else:
        info["chart_type"] = "table"


def parse_group_attribute(info, expression):
    result = re.findall(r'[\w ]+ (?:group|grouped|grouping) by ([\w ]+)', expression)[0]
    info['group_attribute'] = result.split(' ')[0]


def parse_filter_string(info, attribute, condition):
    print(get_category_attribute_options('country'))


def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


def parse_filter_number(info, attribute, condition):
    numbers = []
    for word in condition.split(' '):
        if word.isdecimal():
            numbers.append(int(word))
        elif check_float(word):
            numbers.append(float(word))
    numbers.sort()
    if len(numbers) == 2:
        info['filter'][attribute] = tuple(numbers)
    elif len(numbers) == 1:
        number = numbers[0]
        add_amount = 1 if attribute == 'year' else 0.1
        if 'greater than or equal to' in condition:
            info['filter'][attribute] = (number, None)
        elif 'less than or equal to' in condition:
            info['filter'][attribute] = (None, number)
        elif 'greater' in condition:
            info['filter'][attribute] = (number + add_amount, None)
        elif 'less' in condition:
            info['filter'][attribute] = (None, number - add_amount)
        else:
            info['filter'][attribute] = (number, number)


def parse_filter(info, condition):
    if 'genre' in condition:
        parse_filter_string(info, 'genre', condition)
    elif 'country' in condition:
        parse_filter_string(info, 'country', condition)
    elif 'year' in condition:
        parse_filter_number(info, 'year', condition)
    elif 'average vote' in condition:
        parse_filter_number(info, 'avg_vote', condition)


def parser(expression):
    """
    :param expression:
    1. group/grouped/grouping by followed by attribute
    2. must include 'pie chart'/'bar chart'/'table'
    3. with ... and ... to express filter condition
    4. for numbers, use 'equal to'/'greater than or equal to'/'less than or equal to'/'between'/'greater than'/'less than'
    :return:
    a dict, example is {'chart_type': 'pie chart', "group_attribute": "genre",
                        'filter': {'avg_vote': (6.5, 6.5), 'country': None, 'genre': None,
                        'year': (2008, 2009)}}
    note: range is inclusive
    """
    info = {"chart_type": None, "group_attribute": None, "target_variable": None,
            "filter": {"country": None, "year": None, "avg_vote": None, "genre": None}}
    parse_chart_type(info, expression)
    parse_group_attribute(info, expression)
    filter_expression = expression[expression.find('with') + len('with'):].lstrip()
    filter_conditions = filter_expression.split(' and ')
    for filter_condition in filter_conditions:
        parse_filter(info, filter_condition)
    return info


if __name__ == '__main__':
    expression = "Display a pie chart showing the average vote grouped by country " \
                 "with action as the genre and China as the country"
    print(parser(expression))
    expression = "Display a pie chart showing the average vote grouped by genre " \
                 "with year between 2002 to 2010"
    print(parser(expression))
    expression = "Display a pie chart showing the average vote grouped by country " \
                 "with year greater than or equal to 2010"
    print(parser(expression))
    expression = "Display a pie chart showing the average vote grouped by country " \
                 "with average vote between 6.5 to 10.0"
    print(parser(expression))
