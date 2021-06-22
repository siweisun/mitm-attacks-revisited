from CPMITM import *
from gurobipy import * 


class Vars_generator:
    @staticmethod
    def genVars_input1_of_round(r):   
        if r >= 0:
            return ['IS1_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['ImS1_' + str(j) + '_r_minus' + str(-r) for j in range(16)]
 
    def genVars_input2_of_round(r): 
        if r >= 0:
            return ['IS2_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['ImS2_' + str(j) + '_r_minus' + str(-r) for j in range(16)]
    
    def genVars_input1_of_MixColumn(r):
        return ['IM1_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input2_of_MixColumn( r):
        return ['IM2_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_input1_of_AK(r):
        return ['IAK1_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input2_of_AK(r):
        return ['IAK2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_AllOne1_of_MixColumn(r):
        return ['AO1_' + str(j) + '_r' + str(r) for j in range(4)]
    
    def genVars_AllOne2_of_MixColumn(r):
        return ['AO2_' + str(j) + '_r' + str(r) for j in range(4)]

    def genVars_AllZero_of_MixColumn_KeyAddition(r):
        return ['AZ_MC_KAD_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_OR_MixColumn_KeyAddition(r):
        return ['OR_MC_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_AllZero_of_MixColumn(r):
        return ['AZ_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_SumOne_of_MixColumn(r):
        return ['GSO_'  + str(j) + '_r' + str(r) for j in range(4)]
    
    def genVars_Exist_dubbleZero(r):
        return ['EDZ_' + str(j) + '_r' + str(r) for j in range(4)]
    
    def genVars_ConsumedDeg_of_MixColumn(r):
        return ['CDeg_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_AllOne1_of_Keyaddition(r):
        if r >= 0:
            return ['AO1_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['AO1_KAD_' + str(j) + '_r_minus' + str(-r) for j in range(16)]
    
    def genVars_AllOne2_of_Keyaddition(r):
        if r >= 0:
            return ['AO2_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['AO2_KAD_' + str(j) + '_r_minus' + str(-r) for j in range(16)] 
        
    def genVars_AllZero1_of_Keyaddition(r):
        
        if r >= 0:
            return ['AZ1_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['AZ1_KAD_' + str(j) + '_r_minus' + str(-r) for j in range(16)]

    def genVars_AllZero2_of_Keyaddition(r):
        if r >= 0:
            return ['AZ2_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['AZ2_KAD_' + str(j) + '_r_minus' + str(-r) for j in range(16)]

    def genVars_ConsumedDeg_of_Keyaddition(r):
        if r >= 0:
            return ['CDeg_KAD_' + str(j) + '_r' + str(r) for j in range(16)]
        else:
            return ['CDeg_KAD_' + str(j) + '_r_minus' + str(-r) for j in range(16)]
                  
    def genVars1_subkeys(r):
        assert r >= 0
        return ['SK1_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars2_subkeys(r):
        assert r >= 0
        return ['SK2_' + str(j) + '_r' + str(r) for j in range(16)]  
    
    def genVars_degree_forward():
        return ['deg_f' + str(j) for j in range(16)]
    
    def genVars_degree_backward():
        return ['deg_b' + str(j) for j in range(16)]

    def genVars_degree_forward_key():
        return ['degSk_f' + str(j) for j in range(16)]
    
    def genVars_degree_backward_key():
        return ['degSk_b' + str(j) for j in range(16)]
    
    def genVars_M1_matching():
        return ['m1_' + str(j)for j in range(4)]
    
    def genVars_M2_matching():
        return ['m2_' + str(j) for j in range(4)]
    
    def genVars_M3_matching():
        return ['m3_' + str(j) for j in range(4)]

    def genVars_M4_matching():
        return ['m4_' + str(j) for j in range(4)]
    
class Constraints_generator():
    
    def __init__(self, total_round, initial_round, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round

        
    def gensubConstraints_MixColumn_backward(self, input1_col, input2_col, out1_col, out2_col, Allzero_col, EDZ, Allone1, Allone2, CD_col , GSum_one):
        #_col means a 4 dim vector        
        constr = []
        for i in range(4):
            constr = constr + MITMPreConstraints.Determine_Allzero([input1_col[i], input2_col[i]], Allzero_col[i])
        constr = constr + MITMPreConstraints.Determine_ExistOne(Allzero_col, EDZ)
        
        #if (0,0) belongs  the input column
        constr = constr + [BasicTools.plusTerm(out1_col) + ' + 4 ' + EDZ + ' <= 4']
        constr = constr + [BasicTools.plusTerm(out2_col) + ' + 4 ' + EDZ + ' <= 4']
        
        #if (0,0) does not belong the input column and determine whether the second input column are all ones
        constr = constr + MITMPreConstraints.Determine_Allone(input2_col, Allone2)
        constr = constr + [GSum_one + ' - ' + BasicTools.MinusTerm(input2_col) + ' - ' + BasicTools.MinusTerm(out2_col) + ' = 0']
        constr = constr + [GSum_one + ' - 5 ' + Allone2 + ' <= 3']
        constr = constr + [GSum_one + ' - 8 ' + Allone2 + ' >= 0']            
                    
        constr = constr + MITMPreConstraints.Determine_Allone(input1_col, Allone1)        
        constr = constr + [BasicTools.plusTerm(out1_col) + ' - 4 ' + Allone1 + ' = 0']
      
        #consume degrees
        for i in range(4):
            constr = constr + MITMPreConstraints.Consume_degree(Allone2, out2_col[i], CD_col[i])
        return constr
    
    def gensubConstraints_MixColumn_KeyAddition_backward(self, input1_col, input2_col, input1_MC_KAD_col, input2_MC_KAD_col, OR_MC_KAD_col, out1_col, out2_col, Allzero_col, Allzero_MC_KAD_col, EDZ, Allone1, Allone2, CD_col, GSum_one):
        #_col means a 4 dim vector        
        constr = []
        for i in range(4):
            constr = constr + MITMPreConstraints.Determine_Allzero([input1_col[i], input2_col[i]], Allzero_col[i])
            constr = constr + MITMPreConstraints.Determine_Allzero([input1_MC_KAD_col[i], input2_MC_KAD_col[i]], Allzero_MC_KAD_col[i])
        constr = constr + MITMPreConstraints.Determine_ExistOne(Allzero_col + Allzero_MC_KAD_col, EDZ)
        
        constr = constr + [BasicTools.plusTerm(out1_col) + ' + 4 ' + EDZ + ' <= 4']
        constr = constr + [BasicTools.plusTerm(out2_col) + ' + 4 ' + EDZ + ' <= 4']
        
        constr = constr + MITMPreConstraints.Determine_Allone(input1_col + input1_MC_KAD_col, Allone1)
        constr = constr + [BasicTools.plusTerm(out1_col) + ' - 4 ' + Allone1 + ' = 0']
        
        constr = constr + MITMPreConstraints.Determine_Allone(input2_col + input2_MC_KAD_col, Allone2)
        for i in range(4):
            constr = constr + MITMPreConstraints.OR_backward(input1_col[i], input2_col[i], input1_MC_KAD_col[i], input2_MC_KAD_col[i], OR_MC_KAD_col[i])
        constr = constr + [GSum_one + ' + ' + BasicTools.plusTerm(OR_MC_KAD_col) + ' - ' + BasicTools.MinusTerm(out2_col) + ' = 4']
        constr = constr + [GSum_one + ' - 5 ' + Allone2 +  ' - ' + EDZ + ' <= 3']
        constr = constr + [GSum_one + ' - 8 ' + Allone2 + ' >= 0']

        #consume degrees
        for i in range(4):
            constr = constr + MITMPreConstraints.Consume_degree(Allone2, out2_col[i], CD_col[i])
        return constr                

    def genConstraints_of_forwardRound(self, r):

        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(r)
        input2_AK = Vars_generator.genVars_input2_of_AK(r)
        
        Allone1 = Vars_generator.genVars_AllOne1_of_MixColumn(r) 
        Allone2 = Vars_generator.genVars_AllOne2_of_MixColumn(r)
        
        Sum_one = Vars_generator.genVars_SumOne_of_MixColumn(r)
        
        CD = Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
        
        Allzero = Vars_generator.genVars_AllZero_of_MixColumn(r)
        EDZ = Vars_generator.genVars_Exist_dubbleZero(r)
        
        Allone1_KAD = Vars_generator.genVars_AllOne1_of_Keyaddition(r)
        Allone2_KAD = Vars_generator.genVars_AllOne2_of_Keyaddition(r)
        Allzero1_KAD = Vars_generator.genVars_AllZero1_of_Keyaddition(r)
        CD_KAD = Vars_generator.genVars_ConsumedDeg_of_Keyaddition(r)
       
        if r < self.TR - 1:
            next_r = r + 1
        else:
            next_r = -1
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        
        SK1 = Vars_generator.genVars1_subkeys(r + 1)
        SK2 = Vars_generator.genVars2_subkeys(r + 1)
        constr =[]

        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input2_round), input2_mix)
    
    
        # - Constraints for MixColumns
        if r < self.TR and (r != self.mat_r):
            for j in range(4):
                input1_col = column(input1_mix, j)
                input2_col = column(input2_mix, j)
                out1_col = column(input1_AK, j)
                out2_col = column(input2_AK, j)
                                
                #determine whether (0,0) belongs the input column, if exists, then EDZ[j] = 1
                AO_col = column(Allzero, j)
                for i in range(4):
                    constr = constr + MITMPreConstraints.Determine_Allzero([input1_col[i], input2_col[i]], AO_col[i])
                constr = constr + MITMPreConstraints.Determine_ExistOne(AO_col, EDZ[j])
                
                #if (0,0) belongs  the input column
                constr = constr + [BasicTools.plusTerm(out1_col) + ' + 4 ' + EDZ[j] + ' <= 4']
                constr = constr + [BasicTools.plusTerm(out2_col) + ' + 4 ' + EDZ[j] + ' <= 4']
                
                #if (0,0) does not belong the input column and determine wether the first input column are all ones
                constr = constr + MITMPreConstraints.Determine_Allone(input1_col, Allone1[j])
                constr = constr + [Sum_one[j] + ' - ' + BasicTools.MinusTerm(input1_col) + ' - ' + BasicTools.MinusTerm(out1_col) + ' = 0']
                constr = constr + [Sum_one[j] + ' - 5 ' + Allone1[j] + ' <= 3']
                constr = constr + [Sum_one[j] + ' - 8 ' + Allone1[j] + ' >= 0']            
                            
                constr = constr + MITMPreConstraints.Determine_Allone(input2_col, Allone2[j])
                for i in range(4):
                    constr = constr + [out2_col[i] + ' - ' + Allone2[j] + ' = 0']
              
                #consume degrees
                CD_col = column(CD, j)
                for i in range(4):
                    constr = constr + MITMPreConstraints.Consume_degree(Allone1[j], out1_col[i], CD_col[i])
                
        # constraints for key addition
        for j in range(16):
            constr = constr + MITMPreConstraints.XOR_forward([input1_AK[j], SK1[j]], [input2_AK[j], SK2[j]], out1_round[j], out2_round[j], Allone1_KAD[j], Allone2_KAD[j], Allzero1_KAD[j], CD_KAD[j])
                                        
        return constr

    def genConstraints_of_backwardRound(self, r):
       
        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(r)
        input2_AK = Vars_generator.genVars_input2_of_AK(r)
        
        Allone1 = Vars_generator.genVars_AllOne1_of_MixColumn(r)
        Allone2 = Vars_generator.genVars_AllOne2_of_MixColumn(r)
                
        GSum_one = Vars_generator.genVars_SumOne_of_MixColumn(r)
        
        CD = Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
        
        AZ = Vars_generator.genVars_AllZero_of_MixColumn(r)
        EDZ = Vars_generator.genVars_Exist_dubbleZero(r) 
        
        AZ_MC_KAD = Vars_generator.genVars_AllZero_of_MixColumn_KeyAddition(r)
        OR_MC_KAD = Vars_generator.genVars_OR_MixColumn_KeyAddition(r)

        if r < self.TR - 1:
            next_r = r + 1
        else:
            next_r = -1
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)

        SK1 = Vars_generator.genVars1_subkeys(r + 1)
        SK2 = Vars_generator.genVars2_subkeys(r + 1)
    
        constr =[]
                   
        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input2_round), input2_mix)
     
        if r < self.TR :    
            # - Constraints for MixColumns and KeyAddition       
            for j in range(4):
                input1_col = column(out1_round, j)
                input2_col = column(out2_round, j)
                input1_MC_KAD_col = column(SK1, j)
                input2_MC_KAD_col = column(SK2, j)
                out1_col = column(input1_mix, j)
                out2_col = column(input2_mix, j)
                
                Allzero_col = column(AZ, j)
                Allzero_MC_KAD_col = column(AZ_MC_KAD, j)
                
                CD_col = column(CD, j)
                
                OR_MC_KAD_col = column(OR_MC_KAD, j)
                
                constr = constr + self.gensubConstraints_MixColumn_KeyAddition_backward(input1_col, input2_col, input1_MC_KAD_col, input2_MC_KAD_col, OR_MC_KAD_col, out1_col, out2_col, Allzero_col, Allzero_MC_KAD_col, EDZ[j], Allone1[j], Allone2[j], CD_col, GSum_one[j])

        return constr
              
        
    def genConstraints_KeySchedual(self, r):
        assert r <= self.TR
        input1_key = Vars_generator.genVars1_subkeys(r)
        input2_key = Vars_generator.genVars2_subkeys(r)
        
        out1_key = Vars_generator.genVars1_subkeys(r + 1)
        out2_key = Vars_generator.genVars2_subkeys(r + 1)
        
        constr = []      
        
        # - Constraints for  Keyschedual
        if (r%2)==0:
            constr = constr + MITMPreConstraints.equalConstraints(keyrotation(input1_key), out1_key)
            constr = constr + MITMPreConstraints.equalConstraints(keyrotation(input2_key), out2_key)
        else:
            constr = constr + MITMPreConstraints.equalConstraints(keyrotation(out1_key), input1_key)
            constr = constr + MITMPreConstraints.equalConstraints(keyrotation(out2_key), input2_key)
        return constr

    
    def genConstraints_ini_degree(self):
        
        input1 = Vars_generator.genVars_input1_of_round(self.ini_r)
        input2 = Vars_generator.genVars_input2_of_round(self.ini_r)
        
        input1_key = Vars_generator.genVars1_subkeys(0)
        input2_key = Vars_generator.genVars2_subkeys(0)
        
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
        
        d1_key = Vars_generator.genVars_degree_forward_key()
        d2_key = Vars_generator.genVars_degree_backward_key()
        
        constr = []
        
        for j in range(16):
            
            constr = constr + [input1[j] + ' - ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' - ' + input1[j] + ' + ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' + ' + d1[j] + ' <= 1']
            
            constr = constr + [input2[j] + ' - ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' - ' + input2[j] + ' + ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' + ' + d2[j] + ' <= 1']
            
            constr = constr + [input1_key[j] + ' - ' + d1_key[j] + ' >= 0']
            constr = constr + [input2_key[j] + ' - ' + input1_key[j] + ' + ' + d1_key[j] + ' >= 0']
            constr = constr + [input2_key[j] + ' + ' + d1_key[j] + ' <= 1']           
      
            constr = constr + [input2_key[j] + ' - ' + d2_key[j] + ' >= 0']
            constr = constr + [input1_key[j] + ' - ' + input2_key[j] + ' + ' + d2_key[j] + ' >= 0']
            constr = constr + [input1_key[j] + ' + ' + d2_key[j] + ' <= 1']  
      
        return constr
        
    def genConstraints_minus1(self):
        constr = []
        input1 = Vars_generator.genVars_input1_of_round(-1)
        input2 = Vars_generator.genVars_input2_of_round(-1)
        
        out1 = Vars_generator.genVars_input1_of_round(0)
        out2 = Vars_generator.genVars_input2_of_round(0)

        Allone1_KAD = Vars_generator.genVars_AllOne1_of_Keyaddition(-1)
        Allone2_KAD = Vars_generator.genVars_AllOne2_of_Keyaddition(-1)
        Allzero1_KAD = Vars_generator.genVars_AllZero1_of_Keyaddition(-1)
        Allzero2_KAD = Vars_generator.genVars_AllZero2_of_Keyaddition(-1)
        CD_KAD = Vars_generator.genVars_ConsumedDeg_of_Keyaddition(-1)
        
        sk1 = Vars_generator.genVars1_subkeys(0)
        sk2 = Vars_generator.genVars2_subkeys(0)
               
        for j in range(16):
            if self.mat_r < self.ini_r:
                constr = constr + MITMPreConstraints.XOR_forward([input1[j], sk1[j]], [input2[j], sk2[j]], out1[j], out2[j], Allone1_KAD[j], Allone2_KAD[j], Allzero2_KAD[j], CD_KAD[j])

            if self.mat_r > self.ini_r:
                constr = constr + MITMPreConstraints.XOR_backward([out1[j], sk1[j]], [out2[j], sk2[j]], input1[j], input2[j], Allone1_KAD[j], Allone2_KAD[j], Allzero1_KAD[j], CD_KAD[j])
     
        return constr
        
    def genConstraints_matching_round(self): 
        constr = []
        input1_round = Vars_generator.genVars_input1_of_round(self.mat_r)
        input2_round = Vars_generator.genVars_input2_of_round(self.mat_r)
        
        if self.mat_r < self.TR - 1:
            next_r = self.mat_r + 1
        else:
            next_r = -1
        
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(self.mat_r)
        
        input1_AK = Vars_generator.genVars_input1_of_AK(self.mat_r)
        input2_AK = Vars_generator.genVars_input2_of_AK(self.mat_r)
        

        SK1 = Vars_generator.genVars1_subkeys(self.mat_r + 1)
        SK2 = Vars_generator.genVars2_subkeys(self.mat_r + 1)
        
        Allzero1_KAD = Vars_generator.genVars_AllZero1_of_Keyaddition(self.mat_r)
       
        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input1_round), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Saturnin(input2_round), input2_mix)
        
        #constraints for keyadditon
        for j in range(16):
            constr = constr + MITMPreConstraints.XOR_Mat(out1_round[j], out2_round[j], SK1[j], SK2[j], input1_AK[j], input2_AK[j], Allzero1_KAD[j])
        return constr      
    
    def genConstraints_additional(self):
        constr = []
        CD1_f = []
        CD2_b = []
        
        CD1_f_KAD = []
        CD2_b_KAD = []
        
        
        if self.mat_r < self.ini_r:
            CD1_f_KAD = CD1_f_KAD + Vars_generator.genVars_ConsumedDeg_of_Keyaddition(-1)
            for r in range(0, self.mat_r):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                CD1_f_KAD = CD1_f_KAD + Vars_generator.genVars_ConsumedDeg_of_Keyaddition(r)
                
            
            for r in range(self.ini_r, self.TR):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                CD1_f_KAD = CD1_f_KAD + Vars_generator.genVars_ConsumedDeg_of_Keyaddition(r)
               
                
            for r in range(self.mat_r + 1, self.ini_r):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
        
                
        if self.mat_r > self.ini_r:
            for r in range(self.ini_r, self.mat_r - 1):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
                CD1_f_KAD = CD1_f_KAD + Vars_generator.genVars_ConsumedDeg_of_Keyaddition(r)
             
            CD2_b_KAD = CD2_b_KAD + Vars_generator.genVars_ConsumedDeg_of_Keyaddition(-1)    
            for r in range(0, self.ini_r):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)
            
            for r in range(self.mat_r + 1, self.TR):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MixColumn(r)              
        
    
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
         
        d1_key = Vars_generator.genVars_degree_forward_key()
        d2_key = Vars_generator.genVars_degree_backward_key()
        
        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'
        
        if len(CD2_b + CD2_b_KAD) > 0:
            constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1 + d1_key) + ' + ' + BasicTools.plusTerm(CD2_b + CD2_b_KAD) + ' = 0']
        else:
            constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1 + d1_key) + ' = 0']
            
        if len(CD1_f + CD1_f_KAD) > 0:
            constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2 + d2_key) + ' + ' + BasicTools.plusTerm(CD1_f + CD1_f_KAD) + ' = 0']
        else:
            constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2 + d2_key) + ' = 0 ']
            
        constr = constr + ['GDeg1' + ' >= 1']
        constr = constr + ['GDeg2' + ' >= 1']
        
       
        Input1_mat = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        out2_mat = Vars_generator.genVars_input2_of_AK(self.mat_r)
            
        Gsum = Vars_generator.genVars_SumOne_of_MixColumn(self.mat_r)
        m1 = Vars_generator.genVars_M1_matching()
        m2 = Vars_generator.genVars_M2_matching()
        m3 = Vars_generator.genVars_M3_matching()
        m4 = Vars_generator.genVars_M4_matching()
        
        for j in range(4):
            constr = constr + [Gsum[j] + ' - ' + BasicTools.MinusTerm(column(Input1_mat, j) + column(out2_mat, j)) + ' = 0']

            constr = constr + ['8 ' + m1[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['1 ' + m1[j] + ' - ' + Gsum[j] + ' >= -7']
            
            constr = constr + ['7 ' + m2[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['2 ' + m2[j] + ' - ' + Gsum[j] + ' >= -6']
#            
            constr = constr + ['6 ' + m3[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['3 ' + m3[j] + ' - ' + Gsum[j] + ' >= -5']
#            
            constr = constr + ['5 ' + m4[j] + ' - ' + Gsum[j] + ' <= 0']
            constr = constr + ['4 ' + m4[j] + ' - ' + Gsum[j] + ' >= -4']
        
#       
        GM = 'GMat'
        constr = constr + [GM + ' - ' + BasicTools.MinusTerm(m1 + m2 + m3 + m4) + ' = 0']
        constr = constr + [GM + ' >= 1']
       
        return [constr, Deg1, Deg2, GM]
           
    def genConstraints_total(self):
        constr = []
        
        constr = constr + self.genConstraints_ini_degree()
        
        #state
        if self.mat_r < self.ini_r:
            for r in range(self.ini_r, self.TR):
                constr = constr + self.genConstraints_of_forwardRound(r)
                
            constr = constr + self.genConstraints_minus1()
            
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
            
            constr = constr + self.genConstraints_minus1()
            
            for r in range(0, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)
        
        #keyschedual
         
        for r in range(0, self.TR+1):
            constr = constr + self.genConstraints_KeySchedual(r)
             
             
        #degree
        constr = constr + self.genConstraints_ini_degree()
        
        #mathcing and additional
        constr = constr + self.genConstraints_additional()[0]
        
        return constr     
        

    def genModel(self, filename):

        V = set([])
        constr = list([])
        constr = constr + self.genConstraints_total()
        
        constr = constr + ['GObj - GDeg1 <= 0']
        constr = constr + ['GObj - GDeg2 <= 0']
        constr = constr + ['GObj - GMat <= 0']
        V = BasicTools.getVariables_From_Constraints(constr)
        fid = open('./Model/TR' + str(self.TR) + '_ini' + str(self.ini_r) + '_matr' + str(self.mat_r) + '.lp', 'w')
        
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
    rd = open('./Model/Result_7.txt', 'w')
    rd.write('TR, ini_r, mat_r: d1, d2, m' + '\n' )
    for TR in range(7, 8):
        for ini_r in range(0, TR):
            for mat_r in range(0, TR):
                if mat_r != ini_r:                                                               
                    name = './Model/TR' + str(TR) + '_ini' + str(ini_r) + '_matr' + str(mat_r)
                    A = Constraints_generator(TR, ini_r, mat_r)
                    A.genModel('')
                    Model = read(name + '.lp')
                    Model.optimize()
                    
                    if Model.SolCount == 0:
                        pass  #rd.write('none' + '\n')
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
                        rd.write(str(Sol['GDeg1'])+','+ str(Sol['GDeg2'])+ ','+ str(Sol['GMat']) + '\n')
                        rd.flush()
if __name__== "__main__":
    cmd()
    
