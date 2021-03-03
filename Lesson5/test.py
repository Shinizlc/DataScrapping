d={'name':input('your name\n'),'last_name':input('your last name\n')}
l=[]
for i in range(0,2):
    dic={k:v for k,v in d.items()}
    l.append(dic)
print(l)