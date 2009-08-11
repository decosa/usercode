
class Action(object):

    def __init__(self,label,parameters,referenceToFunctor):

        self.label=label
        self.parameters=parameters
        self.referenceToFunctor=referenceToFunctor
        

class ConfigToolBase :

    """ Base class for PAT tools
    """

    class parameter:
        pass

    def __init__(self):
        self._label = "ConfigToolBase"
        self._parameters={}
        self._description=self.__doc__  
    def __call__(self):
        """ Call the istance 
        """
        raise NotImplementedError
    def getvalue(self,name):
        """ Return the value of parameter 'name'
        """
        return self._parameters[name].value    
    def description(self):
        """ Return a string with a detailed description of the action.
        """
        return self._description
    def addParameter(self,parname, parvalue, description):
        """ Add a parameter with its label, value, description and type to self._parameters
        """
        par=self.parameter()
        par.name=parname
        par.value=parvalue
        par.description=description
        par.type=type(parvalue)
        #print type(parvalue)
        self._parameters[par.name]=par
    def getParameters(self):
        """ Return the list of the parameters of an action.

        Each parameters is represented by a tuple containing its
        type, name, value and description.
        The type determines how the parameter is represented in the GUI.
        Possible types are: 'Category','String','Text','File','FileVector','Boolean','Integer','Float'.
        """
        #print 'Inside function parameters()'
        #for key in self._parameters.keys():
            #print key
            #print 'par name = '+self._parameters[key].name
            #print 'par value = '+str(self._parameters[key].value)
            #print 'par type = '+str(self._parameters[key].type)
        return self._parameters
                                                                        
        #raise NotImplementedError
    def setParameter(self, name, value):
        """ Change parameter 'name' to a new value
        """
        #print 'Inside function setParameters()'
        assert(self._parameters.has_key(name))
        self._parameters[name].value=value
        #print 'New parameter value ('+name + ') '+str(self._parameters[name].value)
        #raise NotImplementedError
    def dumpPython(self):
        """ Return the python code to perform the action
        """
        raise NotImplementedError
    def setComment(self, comment):
        """ Write a comment in the configuration file
        """
        outfile=open('PATconfigfile.py','a')
        outfile.write(comment+'\n')
        outfile.close()
        infile=open('PATconfigfile.py','r')
        text=infile.read()
        infile.close()
        print text
                                                        
