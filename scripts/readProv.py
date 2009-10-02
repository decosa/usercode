
import copy

class filereader:

    class Module:
        def __init__(self,label='',value=[]):
            self.label=label
            self.value=value

    def __init__(self):
        self.aList=['Module', 'ESSource']

    def startswith(self,line):
        "Checks if the first word of the line starts with any of the aList elements"
        for item in self.aList:
            if line.startswith(item):
                return True
        return False    

    def readfile(self,nomefile):
        "Reads the file line by line and searches for the begin and the end of each Module block"       
        aFile = open(nomefile)
        #module=self.module()
        module=[]
        value=[]
        file_modules = {}
        processing=False
        insideModuleBlock = False
        insideParameterBlock = False
        for line in aFile.readlines():
            if line.startswith("Processing History:"):
                print "Processing"
                value=[]
                processing=True
            elif (not line.startswith('---------Event')) and processing:
                value.append(line)
            elif line.startswith('---------Event') and processing:
                file_modules['Processing']=value
                print value
                processing=False
                print "end processing block"
                #print module
            ###if line.startswith("---------Event"):
                #print "Stop processing"
            elif self.startswith(line):
                if  insideParameterBlock:
                    module.append(tuple(value))
                    #print 'VALUE end ', value
                    #print 'MODULE end ', module.value
                    file_modules[key].append(module)
                    insideParameterBlock = False
                    insideModuleBlock = False  ###controllare
                    #print 'outside Parameter Block'
                    #print line[:-1]
                value=[]
                module=[]
                splitLine= line.split()
                key=splitLine[-1]
                #print key
                if key not in file_modules.keys():
                    file_modules[key]=[]
                #module=self.Module()
                module.append(splitLine[-2])
                #print module.label
                value.append(line[:-1])
                #print 'LABEL: ', module.label
                #print 'VALUE: ', value
                insideModuleBlock = True
                insideParameterBlock = False
            elif (line.startswith(' parameters')) and insideModuleBlock:
                insideParameterBlock = True
                value.append(line[:-1])
                #print 'inside Parameter block'
            elif line.startswith('ESModule') and insideParameterBlock:
                module.append(tuple(value))
                #print 'VALUE end ', value
                #print 'MODULE end ', module.value
                file_modules[key].append(module)
                insideParameterBlock = False
                insideModuleBlock = False
            elif line.startswith('}') and insideParameterBlock:
                module.append(tuple(value))
                #print 'VALUE end ', value
                #print 'MODULE end ', module.value
                file_modules[key].append(module)
                insideParameterBlock = False
                insideModuleBlock = False
            elif (insideParameterBlock):
                value.append(line[:-1])
                #print line[:-1]
         
                

        
        return file_modules 



                                                                                                                        
