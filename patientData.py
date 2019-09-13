'''
Created on Jul 12, 2017

@author: Heidi
'''
import math

class PatientData():
    def __init__(self, height, weight):
        self.heightcm = height
        self.weightkg = weight
        self.sex = "Male"
        self.serumcreat = 0.0
        self.age = 0
        
    def setWeight(self, weight):
        self.weightkg = weight
        
    def setHeight(self, height):
        self.heightcm = height  
        
    def setSex(self, sex):
        self.sex = sex  
        
    def setAge(self, age):
        self.age = int(age)

    def setPlasmaCreatinine(self, serumcreat):
        self.serumcreat = float(serumcreat)
            
    def determineIdealBodyWeight(self, weight):
        pass
        # Devine 
        #    men 50kg + 2.3kg for every inch over 5 ft
        #    women 45kg + 2.3kg for every inch over 5 ft
        # Robinson
        #    men 52kg + 1.9kg for each inch over 5 feet
        #    women 49 kg + 1.7 kg for each inch over 5 feet
        # Miller
        #    men 56.2 kg + 1.41 kg for each inch over 5 feet
        #    women 53.1 kg + 1.36 kg for each inch over 5 feet.
        # Hamwi
        #    men 48 kg + 2.7 kg for each inch over 5 feet
        #    women 45.5 kg + 2.2 kg for each inch over 5 feet
        # Lemmens
        #    22 x Height(in meters)2
        
    def determineBMI(self):
        return self.weightkg / (math.pow(self.heightcm/100,2))
        
    def determineBSA(self):
        return math.sqrt((self.heightcm * self.weightkg) / 3600)

    def determineCGCofactor(self):
        if(self.sex == 'Female'):
            cofactor = 0.85
        else:
            cofactor = 1.00
        return cofactor
    
    def determineCGMod(self):
        if(self.age>64):
            mod = max([1.0,self.serumcreat])
        else:
            mod = max([0.8,self.serumcreat])
        return mod
    
    def determineCrclCockroftGault(self):
#        Formula:
#       (male)          CrCl=(140-age)*kg/(72*(serum creatinine))
#       (female)        CrCl=.85*(140-age)*kg/(72*(serum creatinine))
        cofactor = self.determineCGCofactor()
        return (cofactor * (140 - self.age) * self.weightkg) / (72 * self.serumcreat)

    def determineCrClCockroftGaultMod(self):
        cofactor = self.determineCGCofactor()
        mod = self.determineCGMod()
        return (cofactor * (140 - self.age) * self.weightkg) / (72 * mod)
        #return (cofactor * (140 - self.age) * self.weightkg) / (72 * self.serumcreat)
            