class Symbol:
    
    def __init__(self, string):
        self.string = string
    
    def __repr__(self):
        return self.string
    
    def __str__(self):
        return str(self.string)