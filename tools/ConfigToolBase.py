
class ConfigToolBase :

    #__doc__
    #parameters
    #label
    #description

    class parameter:
        pass

    class status:

        def __init__(self, label='ConfigToolBase', parameters={}):
            self.label=label
            self.parameters=parameters
    
    def __init__(self):
        self.label = "ConfigToolBase"
                    
    def __call__(self):
        """ Call the function 
        """
        raise NotImplementedError
    def description(self):
        """ Return a string with a detailed description of the action.
        """
        raise NotImplementedError
    def getParameters(self):
        """ Return the list of the parameters of an action.

        Each parameters is represented by a tuple containing its
        type, name, value and description.
        The type determines how the parameter is represented in the GUI.
        Possible types are: 'Category','String','Text','File','FileVector','Boolean','Integer','Float'.
        """
        raise NotImplementedError
    #def dumpPython(self):
     #   """ Return the python code to perform the action
      #  """
       # raise NotImplementedError
    def setParameter(self, name, value):
        """ Change parameter 'name' to a new value
        """
        raise NotImplementedError
    def setComment(self):
        """ Write a comment in the configuration file
        """
        raise NotImplementedError
