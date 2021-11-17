import re


def parse_single_condition_string(filter_condition, info):
    field, value = filter_condition.split('=')
    info["filter"][field] = value
    return info


def parse_single_condition_int(filter_conditions, info):
    value = [None, None]
    for filter_condition in filter_conditions.split('&'):
        if '<=' in filter_condition:
            value[1] = int(filter_condition.split('<=')[1])
        elif '>=' in filter_condition:
            value[0] = int(filter_condition.split('>=')[1])
        elif '=' in filter_condition:
            value[0] = value[1] = int(filter_condition.split('=')[1])
        elif '<' in filter_condition:
            value[1] = int(filter_condition.split('<')[1]) - 1
        elif '>' in filter_condition:
            value[0] = int(filter_condition.split('>')[1]) + 1
    info["filter"]["year"] = tuple(value)
    return info


def parse_single_condition_one_decimal(filter_conditions, info):
    value = [None, None]
    for filter_condition in filter_conditions.split('&'):
        if '<=' in filter_condition:
            value[1] = float(filter_condition.split('<=')[1])
        elif '>=' in filter_condition:
            value[0] = float(filter_condition.split('>=')[1])
        elif '=' in filter_condition:
            value[0] = value[1] = float(filter_condition.split('=')[1])
        elif '<' in filter_condition:
            value[1] = float(filter_condition.split('<')[1]) - 0.1
        elif '>' in filter_condition:
            value[0] = float(filter_condition.split('>')[1]) + 0.1
    info["filter"]["avg_vote"] = tuple(value)
    return info


def transform_chart_type(s):
    if s == "barchart":
        return "bar chart"
    elif s == "piechart":
        return "pie chart"
    else:
        return s


def parser(expression):
    expression = re.sub(r"\s+", "", expression.lower())
    clauses = expression.split('$')
    info = {"chart_type": None, "group_attribute": None,
            "filter": {"country": None, "year": None, "avg_vote": None, "genre": None}}
    for clause in clauses:
        if ':' in clause:
            chart_type, info["group_attribute"] = clause.split(':')
            info["chart_type"] = transform_chart_type(chart_type)
        elif clause == 'table':
            info["chart_type"] = "table"
        else:
            filter_conditions = clause.split(',')
            for filter_condition in filter_conditions:
                if filter_condition[:7] == 'country' or filter_condition[:5] == 'genre':
                    info = parse_single_condition_string(filter_condition, info)
                elif filter_condition[:4] == 'year':
                    info = parse_single_condition_int(filter_condition, info)
                elif filter_condition[:8] == 'avg_vote':
                    info = parse_single_condition_one_decimal(filter_condition, info)
    return info


def test():
    expression = "bar chart:genre$year>=2008&year<=2010,country=USA, avg_vote<=9&avg_vote>=6"
    assert parser(expression) == {'chart_type': 'bar chart', "group_attribute": "genre",
                                  'filter': {'avg_vote': (6, 9), 'country': 'usa', 'genre': None,
                                             'year': (2008, 2010)}}
    expression = "pie chart:genre$year=2008, avg_vote=6.5"
    assert parser(expression) == {'chart_type': 'pie chart', "group_attribute": "genre",
                                  'filter': {'avg_vote': (6.5, 6.5), 'country': None, 'genre': None,
                                             'year': (2008, 2008)}}
    expression = "table$year>=2008, avg_vote <=8"
    assert parser(expression) == {'chart_type': 'table', "group_attribute": None,
                                  'filter': {'avg_vote': (None, 8), 'country': None, 'genre': None,
                                             'year': (2008, None)}}
    expression = "table$year>2008 & year < 2011, avg_vote >6 & avg_vote<8"
    assert parser(expression) == {'chart_type': 'table', "group_attribute": None,
                                  'filter': {'avg_vote': (6.1, 7.9), 'country': None, 'genre': None,
                                             'year': (2009, 2010)}}
