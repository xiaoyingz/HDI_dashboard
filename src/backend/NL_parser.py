import re
from backend.database_mysql import get_category_attribute_options


def parse_chart_type(info, expression):
    if "pie chart" in expression:
        info["chart_type"] = "PIE"
    elif "bar chart" in expression:
        info["chart_type"] = "BAR"
    elif 'box plot' in expression:
        info["chart_type"] = "BOX"
    elif 'scatter plot' in expression:
        info["chart_type"] = "scatter"
    elif 'heatmap' in expression:
        info['chart_type'] = 'heatmap'
    else:
        info['chart_type'] = 'table'


def parse_group_attribute(info, expression):
    result = re.findall(r'[\w ]+ (?:group|grouped|grouping) by ([\w ]+)', expression)[0]
    words = result.split(' ')
    if len(words) > 1 and words[1] == 'and':
        info['group_attribute'] = (words[0], words[2])
    elif 'box plot' in expression or 'scatter plot' in expression:
        for attribute in ['avg_vote', 'budget', 'metascore', 'worldwide_gross_income', 'usa_gross_income']:
            if attribute in expression:
                info['group_attribute'] = (words[0], attribute)
                break
    else:
        info['group_attribute'] = words[0]


def parse_filter_string(info, attribute, condition):
    options = [word.lower() for word in get_category_attribute_options(attribute)]
    for word in condition.split(' '):
        if word.lower() in options:
            info['filter'][attribute] = word
            break


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
    2. must include 'pie chart'/'bar chart'/'table'/'heatmap'/'boxplot'/'scatter plot'
    3. with ... and ... to express filter condition
    4. for numbers, use 'equal to'/'greater than or equal to'/'less than or equal to'/'between'/'greater than'/'less than'
    :return:
    a dict, example is {'chart_type': 'pie chart', "group_attribute": "genre",
                        'filter': {'avg_vote': (6.5, 6.5), 'country': None, 'genre': None,
                        'year': (2008, 2009)}}
    note: range is inclusive
    """
    info = {"chart_type": None, "group_attribute": None,
            "filter": {"country": None, "year": None, "avg_vote": None, "genre": None}}
    parse_chart_type(info, expression)
    if info["chart_type"] != 'table':
        parse_group_attribute(info, expression)
    if 'with' in expression:
        filter_expression = expression[expression.find('with') + len('with'):].lstrip()
        filter_conditions = filter_expression.split(' and ')
        for filter_condition in filter_conditions:
            parse_filter(info, filter_condition)
    return info


def get_name(parsed):
    if parsed["chart_type"] in ['PIE', 'BAR']:
        name = "movies by {}".format(parsed["group_attribute"])
    elif parsed["chart_type"] == "table":
        name = "movies"
    elif parsed["chart_type"] in ["BOX", 'scatter']:
        name = "{} vs {}".format(parsed["group_attribute"][1], parsed["group_attribute"][0])
    elif parsed["chart_type"] == 'heatmap':
        name = "movies by {} and {}".format(parsed["group_attribute"][0], parsed["group_attribute"][1])
    else:
        name = ""
    filter_name = " ["
    for attribute in parsed["filter"]:
        if parsed["filter"][attribute] is not None:
            filter_name += "{}:{},".format(attribute, parsed["filter"][attribute])
    filter_name = filter_name[:-1] + "]"
    if filter_name == " ]":
        filter_name = ''
    return name + filter_name


if __name__ == '__main__':
    expression = "Display a pie chart showing the distribution grouped by country " \
                 "with action as the genre and China as the country"
    print(parser(expression))
    expression = "Display a bar chart showing the distribution group by genre " \
                 "with year between 2002 to 2010"
    print(parser(expression))
    expression = "Display a heatmap showing the count grouped by country and genre " \
                 "with year greater than or equal to 2010"
    print(parser(expression))
    expression = "Display a box plot showing the distribution of average vote grouped by country " \
                 "with average vote between 6.5 to 10.0 and year less than 2021"
    print(parser(expression))
    expression = "Display a table"
    print(parser(expression))
