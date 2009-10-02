
class difference :
    
    def __init__(self,v):
        self.verbose = v
       
    def list_diff(self,aList1, aList2, string1, string2):
        "Searches for differences between two modules of the same kind"
        differences=[]
        for i in range(2,len(aList1)):
            for j in range(2,len(aList2)):
                if (i==j) and (aList1[i]!=aList2[j]):
                    if aList1[i][:(aList1[i].index('=')+1)] == aList2[j][:(aList2[j].index('=')+1)]:
                        if self.verbose==str(2) or self.verbose==str(1):
                            str1 = aList1[i][2:aList1[i].index('=')+1] + aList1[i][aList1[i].index('=')+1:]+'  ['+ string1+']'
                            str2 = len(aList1[i][2:aList1[i].index('=')+1])*' '+aList2[j][aList2[j].index('=')+1:]+'  ['+string2+']'
                            print str1,'\n',str2,'\n'
                            differences.append(str1)
                            differences.append(str2)
                   
        return differences 
                                                    
    def module_diff(self,module1,module2, string1, string2):
        "Searches for modules which are in both the files but whose parameters are setted at different values"
        ### verificare se queste liste sono utilizzate
        modulesfile1=[]  
        modulesfile2=[]
        print '\nList of modules present in both the files with different parameter values\n'
        for i in module1.keys():
            for j in module2.keys():
                if (i==j) and (i=='Processing'):
                    list= module1[i]
                    print list
                    for k in range(len(list)):
                        if module1[i][k]!= module2[i][k]:
                            print "Different processes "
                            print module1[i][k]+'  ['+string1+']'
                            print module2[i][k]+'  ['+string2+']'
                if (i==j) and (i!='Processing'):
                    #print i
                    #print module1[i]
                    for name1,value1 in module1[i]:
                        for name2,value2 in module2[j]:
                            #print item1.label
                            #print item1.value
                            if (name1==name2) and (value1!=value2): 
                                    print 'Process: '+'"'+i+'"'+'\n'+'Module: '+'"'+name1+'"'+'\n'
                                    d=difference(self.verbose) ###questo non ha senso
                                    d.process=i
                                    d.moduleLabel=name1 ###non mi interessano in questo francente il processo e la label
                                    d.firstvalue=value1
                                    d.secondvalue=value2
                                    self.list_diff(d.firstvalue,d.secondvalue, string1, string2)
                                #else: pass

        self.onefilemodules(module1,module2,'first')
        self.onefilemodules(module2,module1,'second')
    


### capire perche' e' stato utilizzato  il bool onlyonefile
    def onefilemodules(self,module1,module2,string):
        "Searches for modules present only in one of the two files"
        #onlyonefile=False
        print '\nModules run only on the '+string+ ' edmfile:'+'\n'
        for i in module1.keys():
            #print 'KEY: ',i
            labelList=[]
            if i not in module2.keys():
                print '\n Process '+i+' not run on edmfile '+string +'\n'
            elif i!='Processing':
                labelList2=[module[0] for module in module2[i]]
                labelList1=[module[0] for module in module1[i]]
                #print labelList1
                for name, value in module1[i] :
                    #print 'NAME',name
                    if name not in labelList2:
                        print 'Process: '+'"'+i+'"'+'\n'+'Module: '+'"'+name+'"'
                        if  self.verbose==str(2):
                            for k in value:
                                print k
                                


