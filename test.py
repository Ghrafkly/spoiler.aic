import csv

a = '!spoiler 173, 999, 9999, aaa9, aa'

b = [x.strip(',') for x in a.split()][1:]
rd, nrd, nv = '', '', ''

print(b)

def spoiler(scp):
    with open('SCPspoiler.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        # for row in r:
        #     if row == [scp]:
        #         return True
        # return False

        return next((row for row in r if row == [scp]), False)
        # return [True if row == [scp] else False for row in r]

for i in range(len(b)):
    if b[i].isnumeric():
        if spoiler(b[i]):
            rd += (f'{b[i]}, ')
        else:
            nrd += (f'{b[i]}, ')
    else:
        nv += (f'{b[i]}, ')

print(rd[:len(rd)-2])
print(nrd[:len(nrd)-2])
print(nv[:len(nv)-2])