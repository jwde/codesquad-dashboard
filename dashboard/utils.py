def order(field, vals):
    cases = ' '.join('WHEN {}={} THEN {}'.format(field, v, i)\
                     for i,v in enumerate(vals))
    return 'CASE {} END'.format(cases)
