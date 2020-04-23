f = open("admins.txt")
ADMINS = set([x for x in f.read().split('\n')])
f.close()
f = open("god.txt")
GOD = set([x for x in f.read().split('\n')])
f.close()

