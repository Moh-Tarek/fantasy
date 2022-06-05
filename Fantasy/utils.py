from itertools import groupby
import operator


def group_fixtures_by_stage(fixtures):
    result = {}
    for f in fixtures:
        s = f.get_stage_display()
        if s not in result.keys():
            result[s] = []
        result[s].append(f)
    return result

def played_fixtures_grouped(fixtures):
    fixtures_grouped = group_fixtures_by_stage(fixtures)
    
    played_fixtures_grouped ={}
    for key, value in fixtures_grouped.items():
        for x in value:
            if x.url:
                played_fixtures_grouped.update({key:value})
                continue

    return played_fixtures_grouped

def get_group_stats(group, group_fixtures):
    data = {}
    # prepare stats with zero values
    for t in group.teams.all():
        data[t.name] = {
            "MP": 0, 
            "W": 0, "D": 0, "L": 0, 
            "GS": 0, "GC": 0, "GD": 0, 
            "P": 0, 
            'W_vs': []
        }
    # add stats
    for f in group_fixtures:
        if not f.is_finished:
            continue
        t1 = f.team1.name
        t2 = f.team2.name
        t1_goals = f.team1_goals
        t2_goals = f.team2_goals

        # matches played
        data[t1]["MP"] += 1; data[t2]["MP"] += 1
        # goals scored
        data[t1]["GS"] += t1_goals; data[t2]["GS"] += t2_goals
        # goals conceded
        data[t1]["GC"] += t2_goals; data[t2]["GC"] += t1_goals
        # goals difference
        data[t1]["GD"] += t1_goals - t2_goals; data[t2]["GD"] += t2_goals - t1_goals
        # points + win + draw + lose
        if t1_goals > t2_goals:
            data[t1]["P"] += 3; data[t1]["W_vs"].append(t2)
            data[t1]["W"] += 1; data[t2]["L"] += 1
        elif t2_goals > t1_goals:
            data[t2]["P"] += 3; data[t2]["W_vs"].append(t1)
            data[t2]["W"] += 1; data[t1]["L"] += 1
        else:
            data[t1]["P"] += 1; data[t2]["P"] += 1
            data[t2]["D"] += 1; data[t1]["D"] += 1
    return data

def _sort_by_value(base_list, to_be_sorted_list, param, descending):
    # sort the list depending on the parameter and direction, then group by this parameter
    to_be_sorted_list.sort(key=operator.itemgetter(param), reverse=descending)
    for _k, v in groupby(to_be_sorted_list,key=lambda x:x[param]):
        base_list.append(list(v))
    return base_list

def _sort_by_win_versus_2(base_list, to_be_sorted_list, param='W_vs', vs_param='team'):
    # check if one of them won vs the other and make him first
    for t, vs in [[0, 1], [1, 0]]:
        if to_be_sorted_list[vs][vs_param] in to_be_sorted_list[t][param]:
            base_list.append([to_be_sorted_list[t]])
            base_list.append([to_be_sorted_list[vs]])
            return base_list
    # if code reached here, this means that no one of them won vs the other, so return it as it is
    base_list.append(to_be_sorted_list)
    return base_list

def _sort_by_win_versus_3(base_list, to_be_sorted_list, param='W_vs', vs_param='team'):
    # check if one of them won vs the others and make him first, 
    # then sort the other two by the above func
    for t, vs_1, vs_2 in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
        if to_be_sorted_list[vs_1][vs_param] in to_be_sorted_list[t][param] and \
        to_be_sorted_list[vs_2][vs_param] in to_be_sorted_list[t][param]:
            base_list.append([to_be_sorted_list[t]])
            # base_list.append([to_be_sorted_list[vs_1], to_be_sorted_list[vs_2]])
            to_be_sorted_list_2 = [to_be_sorted_list[vs_1], to_be_sorted_list[vs_2]]
            base_list = _sort_by_win_versus_2(base_list, to_be_sorted_list_2, param, vs_param)
            return base_list
    # check if two teams won vs the third and make them first, 
    # then sort those two by the above func, 
    # then add the third after them
    for t_1, t_2, vs in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
        if to_be_sorted_list[vs][vs_param] in to_be_sorted_list[t_1][param] and \
        to_be_sorted_list[vs][vs_param] in to_be_sorted_list[t_2][param]:
            # base_list.append([to_be_sorted_list[t_1], to_be_sorted_list[t_2]])
            to_be_sorted_list_2 = [to_be_sorted_list[t_1], to_be_sorted_list[t_2]]
            base_list = _sort_by_win_versus_2(base_list, to_be_sorted_list_2, param, vs_param)
            base_list.append([to_be_sorted_list[vs]])
            return base_list
    # if code reached here, this means that this criteria can't sort it out, so return it as it is
    base_list.append(to_be_sorted_list)
    return base_list

def _is_single_list(my_list):
    yes = True
    for i in my_list:
        if len(i) > 1:
            yes = False
    return yes

# [
    # {'value': ('P', True)},
    # {'win_versus': ('W_vs', 'team')},
    # {'value': ('GD', True)}, 
    # {'value': ('GS', True)}
# ]
def sort_by(data, actions):
    data = [data]
    for sort_action in actions:
        tmp = []
        for d in data:
            # check if single item, add it as it is and continue the loop
            if len(d) == 1:
                tmp.append(d)
                continue
            # act depending on sorting action's criteria
            for criteria, inputs in sort_action.items():
                if criteria == 'value':
                    param, descending = inputs
                    tmp = _sort_by_value(tmp, d, param, descending)
                elif criteria == 'win_versus':
                    param, vs_param = inputs
                    if len(d) == 2:
                        tmp = _sort_by_win_versus_2(tmp, d, param, vs_param)
                    elif len(d) == 3:
                        tmp = _sort_by_win_versus_3(tmp, d, param, vs_param)
                    else:
                        tmp.append(d)
        data = tmp
        # print(sort_action)
        # for d in data:
        #     print(len(d), d)
        # print("#"*100)
        if _is_single_list(data):
            break
    
    flatten_data = []
    rank = 1
    for d in data:
        for dd in d:
            dd['rank'] = rank
            flatten_data.append(dd)
        rank += len(d)
    return flatten_data