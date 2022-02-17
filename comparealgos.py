import json

def comparealgos(filename1,filename2):
    f1=open(filename1,'r',encoding='utf-8')
    f2=open(filename2,'r',encoding='utf-8')
    d1=json.load(f1)
    d2=json.load(f2)
    f1.close()
    f2.close()
    for k in d1.keys():
        for e1 in d1[k]:
            for e2 in d2[k]:
                if e1['X1']==e2['X1']:
                    if e1['X2']!=e2['X2']:
                        if sorted(e1['X2'])==sorted(e2['X2']):
                            return (e1,e2)