def group_fixtures_by_stage(fixtures):
    result = {}
    for f in fixtures:
        s = f.get_stage_display()
        if s not in result.keys():
            result[s] = []
        result[s].append(f)
    return result