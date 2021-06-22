from CPMITM import *
from gurobipy import * 


class Vars_generator:
    @staticmethod
    def genVars_input1_of_round(r):   
        if r >= 0:
            return ['IS1_' + str(j) + '_r' + str(r) for j in range(128)]
 
    def genVars_input2_of_round(r): 
        if r >= 0:
            return ['IS2_' + str(j) + '_r' + str(r) for j in range(128)]
    
    def genVars_input1_of_MixColumn(r):
        return ['IM1_' + str(j) + '_r' + str(r) for j in range(128)]

    def genVars_input2_of_MixColumn( r):
        return ['IM2_' + str(j) + '_r' + str(r) for j in range(128)]
    
    def genVars_input1_of_AK(r):
        return ['IAK1_' + str(j) + '_r' + str(r) for j in range(128)]

    def genVars_input2_of_AK(r):
        return ['IAK2_' + str(j) + '_r' + str(r) for j in range(128)]
        
    def genVars_T1():
        return  ['T1_' + str(j) for j in range(128)]
    
    def genVars_T2():
        return  ['T2_' + str(j) for j in range(128)]    

    def genVars_ConsumedDeg_of_AKT():
        return ['CDeg_T' + str(j) for j in range(128)]        

    def genVars_AllOne1_of_MixColumn(r):
        return ['AO1_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_AllOne2_of_MixColumn(r):
        return ['AO2_' + str(j) + '_r' + str(r) for j in range(16)]

    
    def genVars_AllZero_of_MixColumn(r):
        return ['AZ_' + str(j) + '_r' + str(r) for j in range(128)]
    
    def genVars_SumOne_of_MixColumn(r):
        return ['GSO_'  + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_Exist_dubbleZero(r):
        return ['EDZ_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_ConsumedDeg_of_MixColumn(r):
        return ['CDeg_' + str(j) + '_r' + str(r) for j in range(128)]

    
    def genVars_degree_forward():
        return ['deg_f' + str(j) for j in range(128)]
    
    def genVars_degree_backward():
        return ['deg_b' + str(j) for j in range(128)]
    
    def genVars_M1_matching():
        return ['m1_' + str(j)for j in range(16)]
    
    def genVars_M2_matching():
        return ['m2_' + str(j) for j in range(16)]
    
    def genVars_M3_matching():
        return ['m3_' + str(j) for j in range(16)]

    def genVars_M4_matching():
        return ['m4_' + str(j) for j in range(16)]
        
    def genVars_M5_matching():
        return ['m5_' + str(j) for j in range(16)]
    
    def genVars_M6_matching():
        return ['m6_' + str(j) for j in range(16)]
    
    def genVars_M7_matching():
        return ['m7_' + str(j) for j in range(16)]

    def genVars_M8_matching():
        return ['m8_' + str(j) for j in range(16)]  
       
    
class Constraints_generator():
    
    def __init__(self, total_round, initial_round, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round

        
    def gensubConstraints_MixColumn_backward(self, input1_col, input2_col, out1_col, out2_col, Allzero_col, EDZ, Allone1, Allone2, CD_col , GSum_one):
        #_col means a 8 dim vector        
        constr = []
        for i in range(8):
            constr = constr + MITMPreConstraints.Determine_Allzero([input1_col[i], input2_col[i]], Allzero_col[i])
        constr = constr + MITMPreConstraints.Determine_ExistOne(Allzero_col, EDZ)
        
        #if (0,0) belongs  the input column
        constr = constr + [BasicTools.plusTerm(out1_col) + ' + 8 ' + EDZ + ' <= 8']
        constr = constr + [BasicTools.plusTerm(out2_col) + ' + 8 ' + EDZ + ' <= 8']
        
        #if (0,0) does not belong the input column and determine whether the second input column are all ones
        constr = constr + MITMPreConstraints.Determine_Allone(input2_col, Allone2)
        constr = constr + [GSum_one + ' - ' + BasicTools.MinusTerm(input2_col) + ' - ' + BasicTools.MinusTerm(out2_col) + ' = 0']
        constr = constr + [GSum_one + ' - 9 ' + Allone2 + ' <= 7']
        constr = constr + [GSum_one + ' - 16 ' + Allone2 + ' >= 0']            
                    
        constr = constr + MITMPreConstraints.Determine_Allone(input1_col, Allone1)        
        constr = constr + [BasicTools.plusTerm(out1_col) + ' - 8 ' + Allone1 + ' = 0']
      
        #consume degrees
        for i in range(8):
            constr = constr + MITMPreConstraints.Consume_degree(Allone2, out2_col[i], CD_col[i])
        return constr
                   

    def genConstraints_of_forwardRound(self, r):

        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(r)
        input2_AK = Vars_generator.genVars_input2_of_AK(r)
        
        T1 = Vars_generator.genVars_T1()
        T2 = Vars_generator.genVars_T2()         
        
        Allone1 = Vars_generator.genVars_AllOne1_of_MixColumn(r)
        Allone2 = Vars_generator.genVars_AllOne2_of_MixColumn(r)
        
        Sum_one = Vars_generator.genVars_SumOne_of_MixColumn(r)
        
        CD = Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
        
        CD_T = Vars_generator.genVars_ConsumedDeg_of_AKT()        
        
        Allzero = Vars_generator.genVars_AllZero_of_MixColumn(r)
        EDZ = Vars_generator.genVars_Exist_dubbleZero(r)
        

       
        if r < self.TR - 1:
            next_r = r + 1
        else:
            next_r = 0
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        
        constr =[]

        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input2_round), input2_mix)


        if r < self.TR - 1:
            constr = constr + MITMPreConstraints.equalConstraints(out1_round, input1_AK)
            constr = constr + MITMPreConstraints.equalConstraints(out2_round, input2_AK) 
        else:
            for j in range(128):
                constr = constr + MITMPreConstraints.XOR_forward([input1_AK[j],T1[j]],[input2_AK[j],T2[j]],out1_round[j],out2_round[j],CD_T[j])
                
    
        # - Constraints for MixColumns

        for j in range(16):
            input1_col = column512(input1_mix, j)
            input2_col = column512(input2_mix, j)
            out1_col = column512(input1_AK, j)
            out2_col = column512(input2_AK, j)           
            
            #determine whether (0,0) belongs the input column, if exists, then EDZ[j] = 1
            AO_col = column512(Allzero, j)
            for i in range(8):
                constr = constr + MITMPreConstraints.Determine_Allzero([input1_col[i], input2_col[i]], AO_col[i])
            constr = constr + MITMPreConstraints.Determine_ExistOne(AO_col, EDZ[j])
            
            #if (0,0) belongs  the input column
            constr = constr + [BasicTools.plusTerm(out1_col) + ' + 8 ' + EDZ[j] + ' <= 8']
            constr = constr + [BasicTools.plusTerm(out2_col) + ' + 8 ' + EDZ[j] + ' <= 8']
            
            #if (0,0) does not belong the input column and determine whether the first input column are all ones
            constr = constr + MITMPreConstraints.Determine_Allone(input1_col, Allone1[j])
            constr = constr + [Sum_one[j] + ' - ' + BasicTools.MinusTerm(input1_col) + ' - ' + BasicTools.MinusTerm(out1_col) + ' = 0']
            constr = constr + [Sum_one[j] + ' - 9 ' + Allone1[j] + ' <= 7']
            constr = constr + [Sum_one[j] + ' - 16 ' + Allone1[j] + ' >= 0']            
                        
            constr = constr + MITMPreConstraints.Determine_Allone(input2_col, Allone2[j])
            for i in range(8):
                constr = constr + [out2_col[i] + ' - ' + Allone2[j] + ' = 0']
          
            #consume degrees
            CD_col = column512(CD, j)
            for i in range(8):
                constr = constr + MITMPreConstraints.Consume_degree(Allone1[j], out1_col[i], CD_col[i])
                
            
        return constr

    def genConstraints_of_backwardRound(self, r):
       
        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(r)
        input2_AK = Vars_generator.genVars_input2_of_AK(r)
        
        T1 = Vars_generator.genVars_T1()
        T2 = Vars_generator.genVars_T2()         
        
        Allone1 = Vars_generator.genVars_AllOne1_of_MixColumn(r) 
        Allone2 = Vars_generator.genVars_AllOne2_of_MixColumn(r)
        
        
        GSum_one = Vars_generator.genVars_SumOne_of_MixColumn(r)
        
        CD = Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
        
        CD_T = Vars_generator.genVars_ConsumedDeg_of_AKT()         
        
        AZ = Vars_generator.genVars_AllZero_of_MixColumn(r)
        EDZ = Vars_generator.genVars_Exist_dubbleZero(r) 
        

        if r < self.TR - 1:
            next_r = r + 1
        else:
            next_r = 0
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
    
        constr =[]
            
        
        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input2_round), input2_mix)

        if r < self.TR - 1:
            constr = constr + MITMPreConstraints.equalConstraints(out1_round, input1_AK)
            constr = constr + MITMPreConstraints.equalConstraints(out2_round, input2_AK) 
        else:
            for j in range(128):
                constr = constr + MITMPreConstraints.XOR_backward([out1_round[j],T1[j]],[out2_round[j],T2[j]],input1_AK[j],input2_AK[j],CD_T[j])            


        for j in range(16):
            input1_col = column512(input1_AK, j)
            input2_col = column512(input2_AK, j)
            out1_col = column512(input1_mix, j)
            out2_col = column512(input2_mix, j)
            
            Allzero_col = column512(AZ, j)
            
            CD_col = column512(CD, j)
            
            constr = constr + self.gensubConstraints_MixColumn_backward(input1_col, input2_col, out1_col, out2_col, Allzero_col, EDZ[j], Allone1[j], Allone2[j], CD_col, GSum_one[j])

        return constr
              

    
    def genConstraints_ini_degree(self):
        
        input1 = Vars_generator.genVars_input1_of_round(self.ini_r)
        input2 = Vars_generator.genVars_input2_of_round(self.ini_r)
        
        
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
        
        constr = []
        
        for j in range(128):
        
            constr = constr + [input1[j] + ' - ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' - ' + input1[j] + ' + ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' + ' + d1[j] + ' <= 1']
            
            constr = constr + [input2[j] + ' - ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' - ' + input2[j] + ' + ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' + ' + d2[j] + ' <= 1']
            
      
        return constr
        
        
    def genConstraints_matching_round(self):
        constr = []
        input1_round = Vars_generator.genVars_input1_of_round(self.mat_r)
        input2_round = Vars_generator.genVars_input2_of_round(self.mat_r)
        
        if self.mat_r < self.TR -1:
            next_r = self.mat_r+1
        else :
            next_r = 0
        
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(self.mat_r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(self.mat_r)
        input2_AK = Vars_generator.genVars_input2_of_AK(self.mat_r)
        
       
        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(SR_Groestl512(input2_round), input2_mix)
        
        if self.mat_r < self.TR - 1:
            constr = constr + MITMPreConstraints.equalConstraints(out1_round, input1_AK)
            constr = constr + MITMPreConstraints.equalConstraints(out2_round, input2_AK) 
        else:
            for i in range(0,8):
                for j in range(8,16):
                    constr = constr + [input1_AK[16*i+j] + ' - ' + out1_round[16*i+j] + ' = 0']
                    constr = constr + [input2_AK[16*i+j] + ' - ' + out2_round[16*i+j] + ' = 0']


        return constr      
    
    def genConstraints_additional(self):
        constr = []
        CD1_f = []
        CD2_b = []
               
        if self.mat_r < self.ini_r:

            for r in range(0, self.mat_r):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
           
            for r in range(self.ini_r, self.TR):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                                
            for r in range(self.mat_r + 1, self.ini_r):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)     
                
        if self.mat_r > self.ini_r:
            for r in range(self.ini_r, self.mat_r):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                
            for r in range(0, self.ini_r):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
            
            for r in range(self.mat_r + 1, self.TR):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                
        T1 = Vars_generator.genVars_T1() #the cell of T must be constant or unknown
        T2 = Vars_generator.genVars_T2()
        
        for i in range(0,8):
            for j in range(0,16):
                if j < 8:
                    constr = constr + [T1[16*i+j] + ' = 0']
                    constr = constr + [T2[16*i+j] + ' = 0']  
                else:
                    constr = constr + [T1[16*i+j] + ' - ' + T2[16*i+j] + ' = 0']
        
            
        constr = constr + ['Gt' + ' - ' + BasicTools.MinusTerm(T1) + ' = 0']  
    
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
                
        
        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'
        
        constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1) + ' = 0']
        constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2) + ' = 0']
        
        
        if len(CD2_b) > 0:
            constr = constr + ['GCD1' + ' - ' + BasicTools.MinusTerm(CD2_b) + ' = 0']
        else :
            constr = constr + ['GCD1' + ' = 0']
            
        if len(CD1_f) > 0:
            constr = constr + ['GCD2' + ' - ' + BasicTools.MinusTerm(CD1_f) + ' = 0'] 
        else:
            constr = constr + ['GCD2' + ' = 0']

        constr = constr + ['GDeg1 - GDoF1 - GCD1 = 0']
        constr = constr + ['GDeg2 - GDoF2 - GCD2 = 0']
        constr = constr + ['2 GDoF1' + ' - ' + 'Gt' + ' > 0']
        constr = constr + ['2 GDoF2' + ' - ' + 'Gt' + ' > 0']
        
        constr = constr + ['2 GDeg1' +  ' < 64']
        constr = constr + ['2 GDeg2' +  ' < 64']        
              
        
        Input1_mat = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        out2_mat = Vars_generator.genVars_input2_of_AK(self.mat_r)
            
        Gsum = Vars_generator.genVars_SumOne_of_MixColumn(self.mat_r)
        m1 = Vars_generator.genVars_M1_matching()
        m2 = Vars_generator.genVars_M2_matching()
        m3 = Vars_generator.genVars_M3_matching()
        m4 = Vars_generator.genVars_M4_matching()
        m5 = Vars_generator.genVars_M5_matching()
        m6 = Vars_generator.genVars_M6_matching()
        m7 = Vars_generator.genVars_M7_matching()
        m8 = Vars_generator.genVars_M8_matching()
        
        for j in range(16):
            constr = constr + [Gsum[j] + ' - ' + BasicTools.MinusTerm(column512(Input1_mat, j) + column512(out2_mat, j)) + ' = 0']

            constr = constr + ['16 ' + m1[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['1 ' + m1[j] + ' - ' + Gsum[j] + ' >= -15']
            
            constr = constr + ['15 ' + m2[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['2 ' + m2[j] + ' - ' + Gsum[j] + ' >= -14']
           
            constr = constr + ['14 ' + m3[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['3 ' + m3[j] + ' - ' + Gsum[j] + ' >= -13']
          
            constr = constr + ['13 ' + m4[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['4 ' + m4[j] + ' - ' + Gsum[j] + ' >= -12']
            
            constr = constr + ['12 ' + m5[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['5 ' + m5[j] + ' - ' + Gsum[j] + ' >= -11']
            
            constr = constr + ['11 ' + m6[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['6 ' + m6[j] + ' - ' + Gsum[j] + ' >= -10']
           
            constr = constr + ['10 ' + m7[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['7 ' + m7[j] + ' - ' + Gsum[j] + ' >= -9']
           
            constr = constr + ['9 ' + m8[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['8 ' + m8[j] + ' - ' + Gsum[j] + ' >= -8']           
              
        GM = 'GMat'
        constr = constr + [GM + ' - ' + BasicTools.MinusTerm(m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8) + ' = 0']
        constr = constr + [GM + ' - ' + 'Gt' + ' <= 0']
        constr = constr + ['2 GMat' + ' - ' + 'Gt' + ' > 0']
       
        return [constr, Deg1, Deg2, GM]
           
    def genConstraints_total(self):
        constr = []
        
        constr = constr + self.genConstraints_ini_degree()
        
        #state
        if self.mat_r < self.ini_r:
            for r in range(self.ini_r, self.TR):
                constr = constr + self.genConstraints_of_forwardRound(r)              
            
            for r in range(0, self.mat_r):
                constr = constr + self.genConstraints_of_forwardRound(r)
                
            constr = constr + self.genConstraints_matching_round()
                
            for r in range(self.mat_r + 1, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)
                
                
        if self.mat_r > self.ini_r:
            
            for r in range(self.ini_r, self.mat_r):
                constr = constr + self.genConstraints_of_forwardRound(r)
                
            constr = constr + self.genConstraints_matching_round()
            
            for r in range(self.mat_r + 1, self.TR):
                constr = constr + self.genConstraints_of_backwardRound(r)        
            
            for r in range(0, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)
        
             
        #degree
        constr = constr + self.genConstraints_ini_degree()
        
        #mathcing and additional
        constr = constr + self.genConstraints_additional()[0]
        
        input1_AK = Vars_generator.genVars_input1_of_AK(self.TR - 1)
        input2_AK = Vars_generator.genVars_input2_of_AK(self.TR - 1)
        input1_round = Vars_generator.genVars_input1_of_round(0)
        input2_round = Vars_generator.genVars_input2_of_round(0)
        if self.mat_r > self.ini_r:
            for i in range(0,8):
                for j in range(0,8):
                    constr = constr + [input1_AK[16*i+j] + ' = 0']
                    constr = constr + [input2_AK[16*i+j] + ' = 0']
        else:
            for i in range(0,8):
                for j in range(0,8):
                    constr = constr + [input1_round[16*i+j] + ' = 0']
                    constr = constr + [input1_round[16*i+j] + ' = 0']
        
        return constr     
        

    def genModel(self, filename):

        V = set([])
        constr = list([])
        constr = constr + self.genConstraints_total()
        
        constr = constr + ['2 GDoF1 - Gt >= 2']
        constr = constr + ['2 GDoF2 - Gt >= 2']
        constr = constr + ['2 GMat - Gt >= 2']
        constr = constr + ['Gt >= 2']
        
        constr = constr + ['GObj - 2 GDoF1 + Gt <= 0']
        constr = constr + ['GObj - 2 GDoF2 + Gt <= 0']
        constr = constr + ['GObj - 2 GMat + Gt <= 0']
        constr = constr + ['GObj - Gt <= 0']
        
        V = BasicTools.getVariables_From_Constraints(constr)
        fid = open('./Model512/TR' + str(self.TR) + '_ini' + str(self.ini_r) + '_matr' + str(self.mat_r) + '.lp', 'w')
        
        fid.write('Maximize' + '\n')
        fid.write('GObj' + '\n')
        fid.write('\n')
        fid.write('Subject To')
        fid.write('\n')
        for c in constr:
            fid.write(c)
            fid.write('\n')        

        GV = []
        BV =[]
        for v in V:
            if v[0] == 'G':
                GV.append(v)
            else:
                BV.append(v)
                

        fid.write('Binary' + '\n')
        for bv in BV:
            fid.write(bv + '\n')
            
        fid.write('Generals' + '\n')
        for gv in GV:
            fid.write(gv + '\n') 
            
        fid.close()

def cmd():
    rd = open('./Model512/Result_8_notatlast.txt', 'w')
    rd.write('TR, ini_r, mat_r: d1, d2, m, t' + '\n' )
    for TR in range(8, 9):
        for ini_r in range(0, TR):
            for mat_r in range(0, TR-1):
                if mat_r != ini_r:                        
                    name = './Model512/TR' + str(TR) + '_ini' + str(ini_r) + '_matr' + str(mat_r)
                    A = Constraints_generator(TR, ini_r, mat_r)
                    A.genModel('')
                    Model = read(name + '.lp')
                    Model.optimize()
                    
                    if Model.SolCount == 0:
                        pass  
                    else:
                        
                        Model.write(name + '.sol')
                        solFile = open('./' + name + '.sol', 'r')  
               
                        Sol = dict()
                
                        for line in solFile:
                            if line[0] != '#':
                                temp = line
                                temp = temp.replace('-', ' ')
                                temp = temp.split()
                                Sol[temp[0]] = int(temp[1])
                        rd.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':') 
                        rd.write(str(Sol['GDoF1'])+','+ str(Sol['GDoF2'])+ ','+ str(Sol['GMat'])+ ','+ str(Sol['Gt']) + '\n')
                        rd.flush()
if __name__== "__main__":
    cmd()
    
