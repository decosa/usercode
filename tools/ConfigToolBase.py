import FWCore.ParameterSet.Config as cms  

class Action(object):

    def __init__(self,label,parameters=[],referenceToFunctor=None, bool=True):

        self.label=label
        self.parameters=parameters
        self.referenceToFunctor=referenceToFunctor
  
    def dumpPython(self):
        self.referenceToFunctor.setParameters(self.parameters)
        return self.referenceToFunctor.dumpPython()
    
class parameter:
    pass

class ConfigToolBase(object) :

    """ Base class for PAT tools
    """
    _label="ConfigToolBase"
    def __init__(self):
        self._parameters={}
        self._description=self.__doc__  
    def __call__(self):
        """ Call the istance 
        """
        raise NotImplementedError
    def __copy__(self):
        c=type(self)()
        c.setParameters(self.getParameters().copy())
        return c
    def setDefaultParameters(self):
        pass
    def parameters(self):
        parameters={}
        for key in self._defaultParameters.keys():
            parameters[key]=self._defaultParameters[key].value
        return parameters
    def getvalue(self,name):
        """ Return the value of parameter 'name'
        """
        return self._parameters[name].value
    def getvalueNew(self,name):
        """ Return the value of parameter 'name'
        """
        return self._parameters[name]
    def description(self):
        """ Return a string with a detailed description of the action.
        """
        return self._description
    ### addParameter must be replaced by addParameterNew, as soon as the migration of tool is completed
    def addParameter(self,parname, parvalue, description):
        """ Add a parameter with its label, value, description and type to self._parameters
        """
        par=parameter()
        par.name=parname
        par.value=parvalue
        par.description=description
        par.type=type(parvalue)
        #print type(parvalue)
        self._parameters[par.name]=par
        
    def addParameterNew(self,dict,parname, parvalue, description,Type=None):
        """ Add a parameter with its label, value, description and type to self._parameters
        """
        par=parameter()
        par.name=parname
        par.value=parvalue
        par.description=description
        print Type==None
        if Type==None:
            par.type=type(parvalue)
        else: par.type=Type
        print 'TYPE', par.type
        dict[par.name]=par
        
    def getParameters(self):
        """ Return the list of the parameters of an action.

        Each parameters is represented by a tuple containing its
        type, name, value and description.
        The type determines how the parameter is represented in the GUI.
        Possible types are: 'Category','String','Text','File','FileVector','Boolean','Integer','Float'.
        """
        return self._parameters

    def getDefaults(self):
        return self._defaultParameters
    
    ### setParameter must be replaced by setParameterNew, as soon as the migration of tool is completed
    def setParameter(self, name, value):
        """ Change parameter 'name' to a new value
        """
        self._parameters[name].value=value
    def setParameterNew(self, name, value):
        """ Change parameter 'name' to a new value
        """
        self._parameters[name]=value
        
    def setParameters(self, parameters):
        self._parameters=parameters
        
    def dumpPython(self):
        """ Return the python code to perform the action
        """
        raise NotImplementedError
    def setComment(self, comment):
        """ Write a comment in the configuration file
        """
        dumpPython='#'+comment+'\n'
        return dumpPython

    ### typeError and instanceError must be deleted after exporting the new defaultparameter system to all the tools 
    def typeError(self,value,type):
        return "The type for parameter "+'"'+str(value)+'"'+" is not "+'"'+type+'"'

    def instanceError(self,value,obj):
        return "Parameter "+'"'+str(value)+'"'+" is not an instance of object "+'"'+obj+'"'                                                 

    def errorMessage(self,value,type):
        return "The type for parameter "+'"'+str(value)+'"'+" is not "+'"'+str(type)+'"'

    def typeErrorNew(self,value,type):
        if not isinstance(value,type):
            raise TypeError(self.errorMessage(value,type))
        
