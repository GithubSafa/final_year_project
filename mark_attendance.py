name='safa'
date_time_string = '12/06/22'
with open('attendance.csv', 'a') as f:
    f.writelines(f'\n{name},{date_time_string},Clock In')