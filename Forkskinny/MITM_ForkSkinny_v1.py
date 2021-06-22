from CPMITM import *
from gurobipy import * 

class Vars_generator:
    @staticmethod
    def genVars_input1_of_round(r):   
        return ['IS1_' + str(j) + '_r' + str(r) for j in range(16)]
 
    def genVars_input2_of_round(r): 
        return ['IS2_' + str(j) + '_r' + str(r) for j in range(16)]
            
    def genVars_input1_of_sr(r):
        return ['SR1_' + str(j) + '_r' + str(r) for j in range(16)]
        
    def genVars_input2_of_sr(r):
        return ['SR2_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars_input1_of_MixColumn(r):
        return ['IM1_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input2_of_MixColumn( r):
        return ['IM2_' + str(j) + '_r' + str(r) for j in range(16)]
        
    def genVars_ConsumedDeg_of_ART(r):
        return ['CDeg_ART_' + str(j) + '_r' + str(r) for j in range(16)]   
        
    def genVars_ConsumedDeg_of_MC(r):
        return ['CDeg_MC_' + str(j) + '_r' + str(r) for j in range(12)]  
        
    def genVars_ConsumedDeg_of_ART_dual(r):
        return ['CDeg_ART_dual' + str(j) + '_r' + str(r) for j in range(16)] 

    def genVars_ConsumedDeg_of_MCfork1():
        return ['CDeg_MC1_' + str(j) + '_fork' for j in range(12)] 
        
    def genVars_ConsumedDeg_of_MCfork2():
        return ['CDeg_MC2_' + str(j) + '_fork' for j in range(12)]  

    def genVars1_TK1(r):
        assert r >= 0
        return ['TK1_1_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars2_TK1(r):
        assert r >= 0
        return ['TK1_2_' + str(j) + '_r' + str(r) for j in range(16)]
        
    def genVars1_TK2(r):
        assert r >= 0
        return ['TK2_1_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars2_TK2(r):
        assert r >= 0
        return ['TK2_2_' + str(j) + '_r' + str(r) for j in range(16)]  

    def genVars1_TK3(r):
        assert r >= 0
        return ['TK3_1_' + str(j) + '_r' + str(r) for j in range(16)]
    
    def genVars2_TK3(r):
        assert r >= 0
        return ['TK3_2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_degree_forward():
        return ['deg_f' + str(j) for j in range(16)]
    
    def genVars_degree_backward():
        return ['deg_b' + str(j) for j in range(16)]

    def genVars_degree_forward_TK1():
        return ['degTK1_f' + str(j) for j in range(16)]        
    
    def genVars_degree_backward_TK1():
        return ['degTK1_b' + str(j) for j in range(16)]    
        
    def genVars_degree_forward_TK2():
        return ['degTK2_f' + str(j) for j in range(16)]        
    
    def genVars_degree_backward_TK2():
        return ['degTK2_b' + str(j) for j in range(16)]

    def genVars_degree_forward_TK3():
        return ['degTK3_f' + str(j) for j in range(16)]        
    
    def genVars_degree_backward_TK3():
        return ['degTK3_b' + str(j) for j in range(16)]    

    def genVars_matchvar1():
        return ['matchvar1' +str(j) for j in range(16)]
        
    def genVars_matchvar2():
        return ['matchvar2' +str(j) for j in range(16)]
        
    def genVars_matchvar11():
        return ['matchvar11' +str(j) for j in range(16)]
        
    def genVars_matchvar22():
        return ['matchvar22' +str(j) for j in range(16)]
              
    def genVars_M_matching1():
        return ['match_' + str(j)for j in range(16)]
        
    def genVars_M_matching2():
        return ['match1_' + str(j)for j in range(16)]
    
class Constraints_generator():
    
    def __init__(self, total_round, initial_round, initial_r0r1, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round
        self.r0r1 = initial_r0r1
               

    def genConstraints_of_forwardRound(self, r):

        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_sr = Vars_generator.genVars_input1_of_sr(r)
        input2_sr = Vars_generator.genVars_input2_of_sr(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
        
        
        CD_ART = Vars_generator.genVars_ConsumedDeg_of_ART(r)
        CD_ART_dual = Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)        

        if r ==  self.TR - self.r0r1 - 1 :
            next_r = 0
        elif r == self.TR -1:
            next_r = 0
        else:
            next_r = r+1
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        if r == self.TR - 2*self.r0r1 - 1:
            out11_round = Vars_generator.genVars_input1_of_round(self.TR - self.r0r1)
            out22_round = Vars_generator.genVars_input2_of_round(self.TR - self.r0r1)     
            
        
        TK1_1 = Vars_generator.genVars1_TK1(r)
        TK1_2 = Vars_generator.genVars2_TK1(r)
        TK2_1 = Vars_generator.genVars1_TK2(r)
        TK2_2 = Vars_generator.genVars2_TK2(r)
        TK3_1 = Vars_generator.genVars1_TK3(r)
        TK3_2 = Vars_generator.genVars2_TK3(r)
        constr =[]

        # - Constraints for  ART 
        for i in range(8):
            constr = constr + MITMPreConstraints.threeXOR_forward(input1_round[i],input2_round[i],TK1_1[i],TK1_2[i],TK2_1[i],TK2_2[i],TK3_1[i],TK3_2[i],\
            input1_sr[i],input2_sr[i],CD_ART[2*i],CD_ART[2*i+1])
            constr = constr + MITMPreConstraints.cd_must_from_TK_forward(input1_round[i],input2_round[i],CD_ART[2*i],CD_ART[2*i+1],CD_ART_dual[2*i],CD_ART_dual[2*i+1])
        
        for i in range(8,16):
            constr = constr + [input1_round[i] + ' - ' + input1_sr[i] + ' = 0']
            constr = constr + [input2_round[i] + ' - ' + input2_sr[i] + ' = 0']

        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input1_sr), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input2_sr), input2_mix)
    
    
        # - Constraints for MixColumns 
        CD_MC = Vars_generator.genVars_ConsumedDeg_of_MC(r)       
        for i in range(4):
            input1_col = column(input1_mix,i)
            input2_col = column(input2_mix,i)
            out1_col = column(out1_round,i)
            out2_col = column(out2_round,i)
        
            constr = constr + MITMPreConstraints.MC_forward(input1_col,input2_col,out1_col,out2_col,\
            [CD_MC[3*i],CD_MC[3*i+1],CD_MC[3*i+2]])
            
        if r == self.TR - 2*self.r0r1 - 1:   
            CD_MCfork = Vars_generator.genVars_ConsumedDeg_of_MCfork2()       
            for i in range(4):
                input1_col = column(input1_mix,i)
                input2_col = column(input2_mix,i)
                out11_col = column(out11_round,i)
                out22_col = column(out22_round,i)
            
                constr = constr + MITMPreConstraints.MC_forward(input1_col,input2_col,out11_col,out22_col,\
                [CD_MCfork[3*i],CD_MCfork[3*i+1],CD_MCfork[3*i+2]])
                                        
        return constr
        
        
        
    def genConstraints_of_backwardRound(self, r):

        input1_round = Vars_generator.genVars_input1_of_round(r)
        input2_round = Vars_generator.genVars_input2_of_round(r)
        
        input1_sr = Vars_generator.genVars_input1_of_sr(r)
        input2_sr = Vars_generator.genVars_input2_of_sr(r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(r)
       
        
        CD_ART = Vars_generator.genVars_ConsumedDeg_of_ART(r)
        CD_ART_dual = Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)       
       
        if r ==  self.TR - self.r0r1 - 1:
            next_r = 0
        elif r == self.TR -1:
            next_r = 0
        else:
            next_r = r+1
            
        out1_round = Vars_generator.genVars_input1_of_round(next_r)
        out2_round = Vars_generator.genVars_input2_of_round(next_r)
        
        if r == self.TR - 2*self.r0r1 - 1:
            out11_round = Vars_generator.genVars_input1_of_round(self.TR - self.r0r1)
            out22_round = Vars_generator.genVars_input2_of_round(self.TR - self.r0r1)        
        
        TK1_1 = Vars_generator.genVars1_TK1(r)
        TK1_2 = Vars_generator.genVars2_TK1(r)
        TK2_1 = Vars_generator.genVars1_TK2(r)
        TK2_2 = Vars_generator.genVars2_TK2(r)
        TK3_1 = Vars_generator.genVars1_TK3(r)
        TK3_2 = Vars_generator.genVars2_TK3(r)
        constr =[]

        #- Constraints for  ART
        for i in range(8):
            constr = constr + MITMPreConstraints.threeXOR_backward(input1_sr[i],input2_sr[i],TK1_1[i],TK1_2[i],TK2_1[i],TK2_2[i],TK3_1[i],TK3_2[i],\
            input1_round[i],input2_round[i],CD_ART[2*i],CD_ART[2*i+1])
            constr = constr + MITMPreConstraints.cd_must_from_TK_backward(input1_sr[i],input2_sr[i],CD_ART[2*i],CD_ART[2*i+1],CD_ART_dual[2*i],CD_ART_dual[2*i+1])
 
            
        for i in range(8,16):
            constr = constr + [input1_round[i] + ' - ' + input1_sr[i] + ' = 0']
            constr = constr + [input2_round[i] + ' - ' + input2_sr[i] + ' = 0']
            

        #- Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input1_sr), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input2_sr), input2_mix)
    
    
        #- Constraints for MixColumns
        CD_MC = Vars_generator.genVars_ConsumedDeg_of_MC(r)       
        for i in range(4):
            input1_col = column(input1_mix,i)
            input2_col = column(input2_mix,i)
            out1_col = column(out1_round,i)
            out2_col = column(out2_round,i)
        
            constr = constr + MITMPreConstraints.MC_backward(input1_col,input2_col,out1_col,out2_col,\
            [CD_MC[3*i],CD_MC[3*i+1],CD_MC[3*i+2]])
            
        if r == self.TR - 2*self.r0r1 - 1:
            CD_MCfork = Vars_generator.genVars_ConsumedDeg_of_MCfork1()       
            for i in range(4):
                out11_col = column(out11_round,i)
                out22_col = column(out22_round,i)
                input1_col = column(input1_mix,i)
                input2_col = column(input2_mix,i)        
                constr = constr + MITMPreConstraints.MC_backward(input1_col,input2_col,out11_col,out22_col,\
                [CD_MCfork[3*i],CD_MCfork[3*i+1],CD_MCfork[3*i+2]])            
                                        
        return constr            
        
              
        
    def genConstraints_TK1Schedual_forward(self, r):
        assert r < self.TR
        input1_TK = Vars_generator.genVars1_TK1(r)
        input2_TK = Vars_generator.genVars2_TK1(r)
        
        out1_TK = Vars_generator.genVars1_TK1(r + 1)
        out2_TK = Vars_generator.genVars2_TK1(r + 1)
        
        constr=[]
        constr = constr + MITMPreConstraints.equalConstraints(PT(input1_TK), out1_TK)
        constr = constr + MITMPreConstraints.equalConstraints(PT(input2_TK), out2_TK)

        return constr

    def genConstraints_TK2Schedual_forward(self, r):
        assert r < self.TR
        input1_TK = Vars_generator.genVars1_TK2(r)
        input2_TK = Vars_generator.genVars2_TK2(r)
        
        out1_TK = Vars_generator.genVars1_TK2(r + 1)
        out2_TK = Vars_generator.genVars2_TK2(r + 1)
        
        constr=[]
        constr = constr + MITMPreConstraints.equalConstraints(PT(input1_TK), out1_TK)
        constr = constr + MITMPreConstraints.equalConstraints(PT(input2_TK), out2_TK)

        return constr
        
    def genConstraints_TK3Schedual_forward(self, r):
        assert r < self.TR
        input1_TK = Vars_generator.genVars1_TK3(r)
        input2_TK = Vars_generator.genVars2_TK3(r)
        
        out1_TK = Vars_generator.genVars1_TK3(r + 1)
        out2_TK = Vars_generator.genVars2_TK3(r + 1)
        
        constr=[]
        constr = constr + MITMPreConstraints.equalConstraints(PT(input1_TK), out1_TK)
        constr = constr + MITMPreConstraints.equalConstraints(PT(input2_TK), out2_TK)

        return constr   

    
    def genConstraints_ini_degree(self):
        
        input1 = Vars_generator.genVars_input1_of_round(self.ini_r)
        input2 = Vars_generator.genVars_input2_of_round(self.ini_r)
        
        input1_TK1 = Vars_generator.genVars1_TK1(0)
        input2_TK1 = Vars_generator.genVars2_TK1(0)
        
        input1_TK2 = Vars_generator.genVars1_TK2(0)
        input2_TK2 = Vars_generator.genVars2_TK2(0)
        
        input1_TK3 = Vars_generator.genVars1_TK3(0)
        input2_TK3 = Vars_generator.genVars2_TK3(0)
        
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
        
        d1_TK1 = Vars_generator.genVars_degree_forward_TK1()
        d2_TK1 = Vars_generator.genVars_degree_backward_TK1()
        
        d1_TK2 = Vars_generator.genVars_degree_forward_TK2()
        d2_TK2 = Vars_generator.genVars_degree_backward_TK2()
        
        d1_TK3 = Vars_generator.genVars_degree_forward_TK3()
        d2_TK3 = Vars_generator.genVars_degree_backward_TK3()
        
        constr = []
        
        for j in range(16):          
            constr = constr + [input1[j] + ' - ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' - ' + input1[j] + ' + ' + d1[j] + ' >= 0']
            constr = constr + [input2[j] + ' + ' + d1[j] + ' <= 1']
            
            constr = constr + [input2[j] + ' - ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' - ' + input2[j] + ' + ' + d2[j] + ' >= 0']
            constr = constr + [input1[j] + ' + ' + d2[j] + ' <= 1']
            
            constr = constr + [input1_TK1[j] + ' - ' + d1_TK1[j] + ' >= 0']
            constr = constr + [input2_TK1[j] + ' - ' + input1_TK1[j] + ' + ' + d1_TK1[j] + ' >= 0']
            constr = constr + [input2_TK1[j] + ' + ' + d1_TK1[j] + ' <= 1']           
      
            constr = constr + [input2_TK1[j] + ' - ' + d2_TK1[j] + ' >= 0']
            constr = constr + [input1_TK1[j] + ' - ' + input2_TK1[j] + ' + ' + d2_TK1[j] + ' >= 0']
            constr = constr + [input1_TK1[j] + ' + ' + d2_TK1[j] + ' <= 1'] 
            
            constr = constr + [input1_TK2[j] + ' - ' + d1_TK2[j] + ' >= 0']
            constr = constr + [input2_TK2[j] + ' - ' + input1_TK2[j] + ' + ' + d1_TK2[j] + ' >= 0']
            constr = constr + [input2_TK2[j] + ' + ' + d1_TK2[j] + ' <= 1']           
      
            constr = constr + [input2_TK2[j] + ' - ' + d2_TK2[j] + ' >= 0']
            constr = constr + [input1_TK2[j] + ' - ' + input2_TK2[j] + ' + ' + d2_TK2[j] + ' >= 0']
            constr = constr + [input1_TK2[j] + ' + ' + d2_TK2[j] + ' <= 1'] 
            
            
            constr = constr + [input1_TK3[j] + ' - ' + d1_TK3[j] + ' >= 0']
            constr = constr + [input2_TK3[j] + ' - ' + input1_TK3[j] + ' + ' + d1_TK3[j] + ' >= 0']
            constr = constr + [input2_TK3[j] + ' + ' + d1_TK3[j] + ' <= 1']           
      
            constr = constr + [input2_TK3[j] + ' - ' + d2_TK3[j] + ' >= 0']
            constr = constr + [input1_TK3[j] + ' - ' + input2_TK3[j] + ' + ' + d2_TK3[j] + ' >= 0']
            constr = constr + [input1_TK3[j] + ' + ' + d2_TK3[j] + ' <= 1'] 
                  
      
        return constr
        

        
    def genConstraints_matching_round1(self):
    
        input1_round = Vars_generator.genVars_input1_of_round(self.mat_r)
        input2_round = Vars_generator.genVars_input2_of_round(self.mat_r)
        
        input1_sr = Vars_generator.genVars_input1_of_sr(self.mat_r)
        input2_sr = Vars_generator.genVars_input2_of_sr(self.mat_r)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(self.mat_r)
        
        
        CD_ART = Vars_generator.genVars_ConsumedDeg_of_ART(self.mat_r)
        CD_ART_dual = Vars_generator.genVars_ConsumedDeg_of_ART_dual(self.mat_r)
        
        matchvar1 = Vars_generator.genVars_matchvar1()
        matchvar2 = Vars_generator.genVars_matchvar2()
        # out1_round = Vars_generator.genVars_input1_of_round(self.mat_r+1)
        # out2_round = Vars_generator.genVars_input2_of_round(self.mat_r+1)
        
        TK1_1 = Vars_generator.genVars1_TK1(self.mat_r)
        TK1_2 = Vars_generator.genVars2_TK1(self.mat_r)
        TK2_1 = Vars_generator.genVars1_TK2(self.mat_r)
        TK2_2 = Vars_generator.genVars2_TK2(self.mat_r)
        TK3_1 = Vars_generator.genVars1_TK3(self.mat_r)
        TK3_2 = Vars_generator.genVars2_TK3(self.mat_r)
        constr =[]

        # - Constraints for  ART 
        for i in range(8):
            constr = constr + MITMPreConstraints.threeXOR_forward(input1_round[i],input2_round[i],TK1_1[i],TK1_2[i],TK2_1[i],TK2_2[i],TK3_1[i],TK3_2[i],\
            input1_sr[i],input2_sr[i],CD_ART[2*i],CD_ART[2*i+1])
            constr = constr + MITMPreConstraints.cd_must_from_TK_forward(input1_round[i],input2_round[i],CD_ART[2*i],CD_ART[2*i+1],CD_ART_dual[2*i],CD_ART_dual[2*i+1])            
                        
            
        for i in range(8,16):
            constr = constr + [input1_round[i] + ' - ' + input1_sr[i] + ' = 0']
            constr = constr + [input2_round[i] + ' - ' + input2_sr[i] + ' = 0']
            

        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input1_sr), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input2_sr), input2_mix)
    

        return constr   



    def genConstraints_matching_round2(self): 
    
        input1_round = Vars_generator.genVars_input1_of_round(self.mat_r+self.r0r1)
        input2_round = Vars_generator.genVars_input2_of_round(self.mat_r+self.r0r1)
        
        input1_sr = Vars_generator.genVars_input1_of_sr(self.mat_r+self.r0r1)
        input2_sr = Vars_generator.genVars_input2_of_sr(self.mat_r+self.r0r1)
        
        input1_mix = Vars_generator.genVars_input1_of_MixColumn(self.mat_r+self.r0r1)
        input2_mix = Vars_generator.genVars_input2_of_MixColumn(self.mat_r+self.r0r1)
        
        
        CD_ART = Vars_generator.genVars_ConsumedDeg_of_ART(self.mat_r+self.r0r1)
        CD_ART_dual = Vars_generator.genVars_ConsumedDeg_of_ART_dual(self.mat_r)
        
        matchvar11 = Vars_generator.genVars_matchvar11()
        matchvar22 = Vars_generator.genVars_matchvar22()
        # out1_round = Vars_generator.genVars_input1_of_round(self.mat_r+1)
        # out2_round = Vars_generator.genVars_input2_of_round(self.mat_r+1)
        
        TK1_1 = Vars_generator.genVars1_TK1(self.mat_r+self.r0r1)
        TK1_2 = Vars_generator.genVars2_TK1(self.mat_r+self.r0r1)
        TK2_1 = Vars_generator.genVars1_TK2(self.mat_r+self.r0r1)
        TK2_2 = Vars_generator.genVars2_TK2(self.mat_r+self.r0r1)
        TK3_1 = Vars_generator.genVars1_TK3(self.mat_r+self.r0r1)
        TK3_2 = Vars_generator.genVars2_TK3(self.mat_r+self.r0r1)
        constr =[]

        # - Constraints for  ART
        for i in range(8):
            constr = constr + MITMPreConstraints.threeXOR_forward(input1_round[i],input2_round[i],TK1_1[i],TK1_2[i],TK2_1[i],TK2_2[i],TK3_1[i],TK3_2[i],\
            input1_sr[i],input2_sr[i],CD_ART[2*i],CD_ART[2*i+1])
            constr = constr + MITMPreConstraints.cd_must_from_TK_forward(input1_round[i],input2_round[i],CD_ART[2*i],CD_ART[2*i+1],CD_ART_dual[2*i],CD_ART_dual[2*i+1])            
                        
            
        for i in range(8,16):
            constr = constr + [input1_round[i] + ' - ' + input1_sr[i] + ' = 0']
            constr = constr + [input2_round[i] + ' - ' + input2_sr[i] + ' = 0']
            

        # - Constraints for  ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input1_sr), input1_mix)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow_Skinny(input2_sr), input2_mix)
    

        return constr          
    
    def genConstraints_additional(self):
        constr = []
        CD1_f = []
        CD2_b = []
        
        CD1_f_TK = []
        CD2_b_TK = []
        
        CD1_f_TK_dual = []
        CD2_b_TK_dual = []        
        
        
        # if self.mat_r < self.ini_r:
            # for r in range(0, self.mat_r + 1):
                # CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                # CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)
                       
            # for r in range(self.ini_r, self.TR):
                # CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                # CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)    
                
            # for r in range(self.mat_r + 1, self.ini_r):
                # CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                # CD2_b_TK = CD2_b_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)
            # CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MCfork1()    
            # CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MCfork2()   
            
        if self.mat_r > self.ini_r:
            for r in range(self.ini_r, self.mat_r):
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)
                CD1_f_TK_dual = CD1_f_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)
                
            CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(self.mat_r) 
            CD1_f_TK_dual = CD1_f_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(self.mat_r)
            
            for r in range(self.TR-self.r0r1, self.mat_r+self.r0r1):    
                CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r) 
                CD1_f_TK_dual = CD1_f_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)
                
            CD1_f_TK = CD1_f_TK + Vars_generator.genVars_ConsumedDeg_of_ART(self.mat_r+self.r0r1)
            CD1_f_TK_dual = CD1_f_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(self.mat_r+self.r0r1)
                
            CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MCfork1() 
            CD1_f = CD1_f + Vars_generator.genVars_ConsumedDeg_of_MCfork2()
                
            for r in range(0, self.ini_r):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                CD2_b_TK = CD2_b_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)
                CD2_b_TK_dual = CD2_b_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)
                
            
            for r in range(self.mat_r + 1, self.TR-self.r0r1):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                CD2_b_TK = CD2_b_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)
                CD2_b_TK_dual = CD2_b_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)
     
            for r in range(self.mat_r+self.r0r1+1, self.TR):
                CD2_b = CD2_b + Vars_generator.genVars_ConsumedDeg_of_MC(r)
                CD2_b_TK = CD2_b_TK + Vars_generator.genVars_ConsumedDeg_of_ART(r)  
                CD2_b_TK_dual = CD2_b_TK_dual + Vars_generator.genVars_ConsumedDeg_of_ART_dual(r)
                
    
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()
         
        d1_TK1 = Vars_generator.genVars_degree_forward_TK1()
        d2_TK1 = Vars_generator.genVars_degree_backward_TK1()  
        
        d1_TK2 = Vars_generator.genVars_degree_forward_TK2()
        d2_TK2 = Vars_generator.genVars_degree_backward_TK2()
        
        d1_TK3 = Vars_generator.genVars_degree_forward_TK3()
        d2_TK3 = Vars_generator.genVars_degree_backward_TK3()
        
        
        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'
        # if len(CD2_b + CD2_b_TK) > 0:
            # constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1 + d1_TK1 + d1_TK2 + d1_TK3) + ' + ' + BasicTools.plusTerm(CD2_b + CD2_b_TK) + ' = 0']
        # else:
            # constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1 + d1_TK1 + d1_TK2 + d1_TK3) + ' = 0']
            
        # if len(CD1_f + CD1_f_TK) > 0:
            # constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2 + d2_TK1 + d2_TK2 + d2_TK3) + ' + ' + BasicTools.plusTerm(CD1_f + CD1_f_TK) + ' = 0']
        # else:
            # constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2 + d2_TK1 + d2_TK2 + d2_TK3) + ' = 0 ']
            
        if len(CD2_b_TK_dual) > 0:
            constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1_TK1 + d1_TK2 + d1_TK3) + ' + ' + BasicTools.plusTerm(CD2_b_TK_dual) + ' = 0']
            if len(CD2_b + CD2_b_TK) > 0:
                constr = constr + [BasicTools.plusTerm(d1) + ' - ' + BasicTools.MinusTerm(CD2_b + CD2_b_TK) + ' + ' + BasicTools.plusTerm(CD2_b_TK_dual) + ' = 0']
            else:
                constr = constr + [BasicTools.plusTerm(d1) + ' + ' + BasicTools.plusTerm(CD2_b_TK_dual) + ' = 0']
        else:
            constr = constr + ['GDeg1' + ' - ' + BasicTools.MinusTerm(d1_TK1 + d1_TK2 + d1_TK3)  + ' = 0']
            if len(CD2_b + CD2_b_TK) > 0:
                constr = constr + [BasicTools.plusTerm(d1) + ' - ' + BasicTools.MinusTerm(CD2_b + CD2_b_TK) + ' = 0']
            else:
                constr = constr + [BasicTools.plusTerm(d1) + ' = 0']
                                   
        if len(CD1_f_TK_dual) > 0:
            constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2_TK1 + d2_TK2 + d2_TK3) + ' + ' + BasicTools.plusTerm(CD1_f_TK_dual) + ' = 0'] 
            if len(CD1_f + CD1_f_TK) > 0:
                constr = constr + [BasicTools.plusTerm(d2) + ' - ' + BasicTools.MinusTerm(CD1_f + CD1_f_TK) + ' + ' + BasicTools.plusTerm(CD1_f_TK_dual) + ' = 0']
            else:
                constr = constr + [BasicTools.plusTerm(d2) + ' + ' + BasicTools.plusTerm(CD1_f_TK_dual) + ' = 0']            
        else:
            constr = constr + ['GDeg2' + ' - ' + BasicTools.MinusTerm(d2_TK1 + d2_TK2 + d2_TK3) + ' = 0']
            if len(CD1_f + CD1_f_TK) > 0:
                constr = constr + [BasicTools.plusTerm(d2) + ' - ' + BasicTools.MinusTerm(CD1_f + CD1_f_TK) + ' = 0']
            else:
                constr = constr + [BasicTools.plusTerm(d2) + ' >= 0']
            
        constr = constr + ['GDeg1' + ' >= 1']
        constr = constr + ['GDeg2' + ' >= 1']
        
        input1_mat = Vars_generator.genVars_input1_of_MixColumn(self.mat_r)
        input2_mat = Vars_generator.genVars_input2_of_MixColumn(self.mat_r) 
        
        matchvar1 = Vars_generator.genVars_matchvar1()
        matchvar2 = Vars_generator.genVars_matchvar2()
        
        if self.mat_r < self.TR - 1:
            next_r = self.mat_r + 1
        else:
            next_r = 0
            
        out1_mat = Vars_generator.genVars_input1_of_round(next_r)
        out2_mat = Vars_generator.genVars_input2_of_round(next_r)
            
        match1 = Vars_generator.genVars_M_matching1()

        
        for j in range(16):
            constr = constr + [input1_mat[j] + ' - ' + matchvar1[j] + ' >= 0']
            constr = constr + [input2_mat[j] + ' - ' + input1_mat[j] + ' + ' + matchvar1[j] + ' >= 0']
            constr = constr + [input2_mat[j] + ' + ' + matchvar1[j] + ' <= 1'] 
            
            constr = constr + [out2_mat[j] + ' - ' + matchvar2[j] + ' >= 0']
            constr = constr + [out1_mat[j] + ' - ' + out2_mat[j] + ' + ' + matchvar2[j] + ' >= 0']
            constr = constr + [out1_mat[j] + ' + ' + matchvar2[j] + ' <= 1'] 
         
        for i in range(4):
            a=column(matchvar1,i)
            b=column(matchvar2,i)
            cd=column(match1,i)
            constr = constr + MITMPreConstraints.Match(a,b,cd) 
            
            
            
        input1_mat2 = Vars_generator.genVars_input1_of_MixColumn(self.mat_r+ self.r0r1)
        input2_mat2 = Vars_generator.genVars_input2_of_MixColumn(self.mat_r+ self.r0r1)          
            
        matchvar11 = Vars_generator.genVars_matchvar11()
        matchvar22 = Vars_generator.genVars_matchvar22()
        
        if self.mat_r + self.r0r1 < self.TR - 1:
            next_r2 = self.mat_r + self.r0r1 + 1
        else:
            next_r2 = 0
            
        out1_mat2 = Vars_generator.genVars_input1_of_round(next_r2)
        out2_mat2 = Vars_generator.genVars_input2_of_round(next_r2)
            
        match2 = Vars_generator.genVars_M_matching2()

        
        for j in range(16):
            constr = constr + [input1_mat2[j] + ' - ' + matchvar11[j] + ' >= 0']
            constr = constr + [input2_mat2[j] + ' - ' + input1_mat2[j] + ' + ' + matchvar11[j] + ' >= 0']
            constr = constr + [input2_mat2[j] + ' + ' + matchvar11[j] + ' <= 1'] 
            
            constr = constr + [out2_mat2[j] + ' - ' + matchvar22[j] + ' >= 0']
            constr = constr + [out1_mat2[j] + ' - ' + out2_mat2[j] + ' + ' + matchvar22[j] + ' >= 0']
            constr = constr + [out1_mat2[j] + ' + ' + matchvar22[j] + ' <= 1']   

        for i in range(4):
            a=column(matchvar11,i)
            b=column(matchvar22,i)
            cd=column(match2,i)
            constr = constr + MITMPreConstraints.Match(a,b,cd) 
            
     
        GM = 'GMat'
        constr = constr + [GM + ' - ' + BasicTools.MinusTerm(match1+match2) + ' = 0']
        constr = constr + [GM + ' >= 1']
       
        return [constr, Deg1, Deg2, GM]
           
    def genConstraints_total(self):
        constr = []
        
        #state
        # if self.mat_r < self.ini_r:
            # for r in range(self.ini_r, self.TR):
                # constr = constr + self.genConstraints_of_forwardRound(r)
                
            
            # for r in range(0, self.mat_r):
                # constr = constr + self.genConstraints_of_forwardRound(r)
                
            # constr = constr + self.genConstraints_matching_round1()
            # constr = constr + self.genConstraints_matching_round2()    
            # for r in range(self.mat_r + 1, self.ini_r):
                # constr = constr + self.genConstraints_of_backwardRound(r)
                
                
        if self.mat_r > self.ini_r:
            
            for r in range(self.ini_r, self.mat_r):
                constr = constr + self.genConstraints_of_forwardRound(r)
                
            for r in range(self.TR-self.r0r1, self.mat_r+self.r0r1):
                constr = constr + self.genConstraints_of_forwardRound(r)
                
            constr = constr + self.genConstraints_matching_round1()
            constr = constr + self.genConstraints_matching_round2()
            
            for r in range(self.mat_r + 1, self.TR-self.r0r1):
                constr = constr + self.genConstraints_of_backwardRound(r)
                
            for r in range(self.mat_r+self.r0r1+1, self.TR):
                constr = constr + self.genConstraints_of_backwardRound(r)
                
            for r in range(0, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)
        
        #TKschedual        
        for r in range(0, self.TR):
            constr = constr + self.genConstraints_TK1Schedual_forward(r)
            constr = constr + self.genConstraints_TK2Schedual_forward(r)
            constr = constr + self.genConstraints_TK3Schedual_forward(r)
             
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

        fid = open('./forkskinny/TR' + str(self.TR) + '_ini' + str(self.ini_r) + '_r0r1_' + str(self.r0r1) + '_matr' + str(self.mat_r) + '_v1.lp', 'w')
        
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
    rd = open('./forkskinny/Result_v1_12_12(9_15_15).txt', 'w')
    rd.write('TR, ini_r, r0r1, mat_r: d1, d2, m' + '\n' )
    for r0r1 in range(15, 16):
        for TR in range(24+r0r1, 25+r0r1):     
            for ini_r in range(0, TR-2*r0r1):             
                for mat_r in range(TR-2*r0r1, TR- r0r1-1 ):
    # for r0r1 in range(15, 16):
        # for TR in range(39, 40):     
            # for ini_r in range(3, 4):             
                # for mat_r in range(13, 14):
                    if mat_r != ini_r:                        
                        name = './forkskinny/TR' + str(TR) + '_ini' + str(ini_r) + '_r0r1_' + str(r0r1) + '_matr' + str(mat_r)
                        A = Constraints_generator(TR, ini_r, r0r1, mat_r)
                        A.genModel('')
                        #cmd(4, 1, 7, 4)
                        Model = read(name + '_v1.lp')
                        Model.optimize()
                        
                        if Model.SolCount == 0:
                            pass  #rd.write('none' + '\n')
                        else:
                            
                            Model.write(name + '_v1.sol')
                            solFile = open('./' + name + '_v1.sol', 'r')  
                   
                            Sol = dict()
                    
                            for line in solFile:
                                if line[0] != '#':
                                    temp = line
                                    temp = temp.replace('-', ' ')
                                    temp = temp.split()
                                    #Sol[temp[0]] = float(temp[1]+'0')
                                    Sol[temp[0]] = float(temp[1])
                            rd.write(str(TR) + ',' + str(ini_r) + ',' + str(r0r1) + ',' + str(mat_r) + ':') 
                            rd.write(str(Sol['GDeg1'])+','+ str(Sol['GDeg2'])+ ','+ str(Sol['GMat']) + '\n')
                            rd.flush()
if __name__== "__main__":
    cmd()
    
