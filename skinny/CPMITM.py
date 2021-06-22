from abc import ABCMeta, abstractmethod
from functools import reduce
import math
import random

class BasicTools:
    @staticmethod
    def plusTerm(in_vars):
        t = ''
        for v in in_vars:
            t = t + v + ' + '
        return t[0:-3]

    @staticmethod
    def MinusTerm(in_vars):
        t = ''
        for v in in_vars:
            t = t + v + ' - '
        return t[0:-3]

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace('+', ' ')
            temp = temp.replace('-', ' ')
            temp = temp.replace('>=', ' ')
            temp = temp.replace('<=', ' ')
            temp = temp.replace('=', ' ')
            temp = temp.split()
            for v in temp:
                if not v.isdecimal():
                    V.add(v)
        return V


class MITMPreConstraints:
    @staticmethod
    def cd_must_from_TK_forward(x1,y1,x2,y2,x3,y3): #if (x1,y1)=(0,1), then x2+y2=x3+y3+1, else x2=x3,y2=y3, which use to get the necessary CD from TK
        constr=[]
        constr=constr+[x2 + ' - ' + x3 + ' >= 0']
        constr=constr+[y2 + ' - ' + y3 + ' >= 0']
        constr=constr+[y1 + ' - ' + x2 + ' - ' + y2 + ' + ' + x3 + ' + ' + y3 + ' >= 0']
        constr=constr+[x3 + ' - ' + x1 + ' - ' + x2 + ' - ' + y2 + ' + ' + y3 + ' >= -1']
        constr=constr+[x1 + ' - ' + y1 + ' + ' + y2 + ' - ' + x3 + ' - ' + y3 + ' >= -1']
        constr=constr+[x1 + ' - ' + y1 + ' + ' + x2 + ' - ' + x3 + ' - ' + y3 + ' >= -1']
        return constr

    @staticmethod
    def cd_must_from_TK_backward(x1,y1,x2,y2,x3,y3): #if (x1,y1)=(1,0), then x2+y2=x3+y3+1, else x2=x3,y2=y3, which use to get the necessary CD from TK
        constr=[]
        constr=constr+[x2 + ' - ' + x3 + ' >= 0']
        constr=constr+[y2 + ' - ' + y3 + ' >= 0']
        constr=constr+[x1 + ' - ' + x2 + ' - ' + y2 + ' + ' + x3 + ' + ' + y3 + ' >= 0']
        constr=constr+[x3 + ' - ' + y1 + ' - ' + x2 + ' - ' + y2 + ' + ' + y3 + ' >= -1']
        constr=constr+[y1 + ' - ' + x1 + ' + ' + x2 + ' - ' + x3 + ' - ' + y3 + ' >= -1']
        constr=constr+[y1 + ' - ' + x1 + ' + ' + y2 + ' - ' + x3 + ' - ' + y3 + ' >= -1']
        return constr

    
    @staticmethod  #XOR^+ -RULE
    def XOR_forward(V1_in, V2_in, V1_out, V2_out, cd): #XOR+ rule
        constr=[]
        constr=constr+[V2_in[0] + ' - ' + V2_out + ' >= 0']
        constr=constr+[V1_in[1] + ' - ' + V1_out + ' + ' + cd + ' >= 0']
        constr=constr+[V2_in[1] + ' - ' + V2_out + ' >= 0']
        constr=constr+[V2_out + ' - ' + V2_in[0] + ' - ' + V2_in[1] + ' >= -1']
        constr=constr+[V1_in[0] + ' - ' + V1_out + ' + ' + cd + ' >= 0']
        constr=constr+[V1_out + ' - ' + V1_in[0] + ' - ' + V1_in[1] + ' - 2 ' + cd + ' >= -1']
        constr=constr+[V2_out + ' - ' + cd + ' >= 0']
        return constr


    @staticmethod  #XOR^- -RULE
    def XOR_backward(V1_in, V2_in, V1_out, V2_out, cd):  #XOR- rule
        constr=[]
        constr=constr+[V1_in[0] + ' - ' + V1_out + ' >= 0']
        constr=constr+[V2_in[1] + ' - ' + V2_out + ' + ' + cd + ' >= 0']
        constr=constr+[V1_in[1] + ' - ' + V1_out + ' >= 0']
        constr=constr+[V1_out + ' - ' + V1_in[0] + ' - ' + V1_in[1] + ' >= -1']
        constr=constr+[V2_in[0] + ' - ' + V2_out + ' + ' + cd + ' >= 0']
        constr=constr+[V2_out + ' - ' + V2_in[0] + ' - ' + V2_in[1] + ' - 2 ' + cd + ' >= -1']
        constr=constr+[V1_out + ' - ' + cd + ' >= 0']
        return constr
        
    @staticmethod #3-XOR^+ -RULE
    def threeXOR_forward(x1, y1, x2, y2, x3, y3, x4, y4, out1, out2, cd1, cd2): 
        constr=[]   
        constr=constr+[out1 + ' - ' + x1 + ' - ' + x2 + ' - ' + x3 + ' - ' + x4 + ' - 2 ' + cd1 + ' - 2 ' + cd2 + ' >= -3']
        constr=constr+[x1 + ' + ' + x2 + ' + ' + x3 + ' + ' + x4 + ' - 4 ' + out1 + ' + ' + out2 + ' + 3 ' + cd1 + ' >= 0']
        constr=constr+[y1 + ' + ' + y3 + ' + ' + y4 + ' - 2 ' + out2 + ' - ' + cd1 + ' >= 0']
        constr=constr+[cd1 + ' - ' + cd2 + ' >= 0']
        constr=constr+[y2 + ' - ' + out2 + ' >= 0']
        constr=constr+[y1 + ' + ' + y2 + ' + ' + y3 + ' + ' + y4 + ' + ' + out1 + ' - ' + out2 + ' - 3 ' + cd1 + ' - ' + cd2 + ' >= 0']
        constr=constr+[out2 + ' - ' + y1 + ' - ' + y2 + ' - ' + y3 + ' - ' + y4 + ' >= -3']
        constr=constr+[x1 + ' + ' + y1 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x2 + ' + ' + y2 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x3 + ' + ' + y3 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x4 + ' + ' + y4 + ' - ' + cd1 + ' >= 0']
        constr=constr+[y1 + ' - ' + out2 + ' >= 0']
        constr=constr+[y3 + ' - ' + out2 + ' >= 0']
        constr=constr+[y4 + ' - ' + out2 + ' >= 0']
        constr=constr+[x1 + ' - ' + out1 + ' + ' + cd1 + ' >= 0']
        constr=constr+[x2 + ' - ' + out1 + ' + ' + cd1 + ' >= 0']
        constr=constr+[x3 + ' - ' + out1 + ' + ' + cd1 + ' >= 0']
        constr=constr+[x4 + ' - ' + out1 + ' + ' + cd1 + ' >= 0']
        return constr 
        
    @staticmethod #3-XOR^- -RULE
    def threeXOR_backward(x1, y1, x2, y2, x3, y3, x4, y4, out1, out2, cd1, cd2): 
        constr=[]   
        constr=constr+[out2 + ' - ' + y1 + ' - ' + y2 + ' - ' + y3 + ' - ' + y4 + ' - 2 ' + cd1 + ' - 2 ' + cd2 + ' >= -3']
        constr=constr+[y1 + ' + ' + y2 + ' + ' + y3 + ' + ' + y4 + ' - 4 ' + out2 + ' + ' + out1 + ' + 3 ' + cd1 + ' >= 0']
        constr=constr+[x1 + ' + ' + x2 + ' + ' + x3 + ' - 2 ' + out1 + ' - ' + cd1 + ' >= 0']
        constr=constr+[out2 + ' - ' + cd2 + ' >= 0']
        constr=constr+[x1 + ' + ' + x2 + ' + ' + x3 + ' + ' + x4 + ' + ' + out2 + ' - ' + out1 + ' - 3 ' + cd1 + ' - ' + cd2 + ' >= 0']
        constr=constr+[out1 + ' - ' + x1 + ' - ' + x2 + ' - ' + x3 + ' - ' + x4 + ' >= -3']
        constr=constr+[x1 + ' + ' + y1 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x2 + ' + ' + y2 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x3 + ' + ' + y3 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x4 + ' + ' + y4 + ' - ' + cd1 + ' >= 0']
        constr=constr+[x1 + ' - ' + out1 + ' >= 0']
        constr=constr+[x3 + ' - ' + out1 + ' >= 0']
        constr=constr+[x4 + ' - ' + out1 + ' >= 0']
        constr=constr+[x2 + ' - ' + out1 + ' >= 0']
        constr=constr+[y1 + ' - ' + out2 + ' + ' + cd1 + ' >= 0']
        constr=constr+[y2 + ' - ' + out2 + ' + ' + cd1 + ' >= 0']
        constr=constr+[y3 + ' - ' + out2 + ' + ' + cd1 + ' >= 0']
        constr=constr+[y4 + ' - ' + out2 + ' + ' + cd1 + ' >= 0']
        return constr
        
    @staticmethod
    def Match(a, b, cd):  #Constraints for the Ending States.(match)
        constr=[]
        constr=constr+[] 
        constr=constr+['2 ' + a[0]+ ' + ' + a[2]+ ' + 2 ' + b[0] +  ' + 3 ' + b[1]+ ' + 4 ' + b[2]+  ' + 4 ' + b[3]+ ' - 5 ' + cd[0] + ' - 3 '+cd[1]+' - 4 '+cd[2]+ ' - 4 '+ cd[3]+ ' >= 0' ]
        constr=constr+[cd[0]+' - ' + cd[1]+ ' >= 0']
        constr=constr+[cd[1]+' - ' + cd[2]+ ' >= 0']
        constr=constr+[cd[2]+' - ' + cd[3]+ ' >= 0']
        constr=constr+['3 ' + a[0] +  ' + 3 ' + a[1] +  ' + 2 ' + a[2] +  ' + 3 ' + a[3] +  ' + 2 ' + b[1] +  ' + 2 ' + b[3] +  ' - 5 ' + cd[0] + ' - 4 ' + cd[1]+' - 3 ' + cd[2] +' - 3 ' + cd[3] + ' >= 0'] 
        constr=constr+['- 3 ' + a[0] + ' - 2 ' + a[1] + ' - 2 ' + a[2] + ' - 4 ' + a[3] + ' - 4 ' + b[0] + ' - 4 ' + b[1] +  ' - ' + b[2] + ' - 3 ' + b[3] + ' + 4 ' + cd[0] + ' + 3 ' + cd[1] + ' + 2 ' + cd[2] + ' + ' + cd[3] + ' >= -13'] 
        constr=constr+['2 ' + a[0] + ' + 3 ' + a[2] + ' + 4 ' + b[0] + ' + 3 ' + b[1] +   ' + 2 ' + b[2] +   ' + ' + b[3] + ' - 5 ' + cd[0] + ' - 3 ' + cd[1] + ' - 3 ' + cd[2] + ' - 4 ' + cd[3] + ' >= 0'] 
        constr=constr+['- ' + a[0] + ' - ' + a[1] + ' - ' + a[2] + ' + ' + a[3] + ' - 2 ' + b[1] + ' - ' + b[2] + ' - ' + b[3] + ' + ' + cd[0] + ' + ' + cd[1] + ' + ' + cd[2] + ' - ' + cd[3] +  ' >= -4'] 
        constr=constr+['- 2 ' + a[0] + ' - ' + a[1] + ' - 2 ' + a[2] + ' - 4 ' + a[3] + ' - 2 ' + b[0] + ' - ' + b[1] + ' - ' + b[2] + ' - 2 ' + b[3] + ' + 2 ' + cd[0] + ' + 2 ' + cd[1] + ' + ' + cd[2] + ' + ' + cd[3] + ' >= -9'] 
        constr=constr+['2 ' + a[0] + ' + 3 ' + a[1] + ' + ' + a[2] + ' + 3 ' + b[0] + ' + 2 ' + b[1] + ' + ' + b[3] + ' - 4 ' + cd[0] + ' - 2 ' + cd[1] +' - 3 ' + cd[2] + ' - 3 ' + cd[3] + ' >= 0'] 
        constr=constr+['2 ' + a[0] + ' + ' + a[2] + ' + 3 ' + a[3] + ' + 2 ' + b[1] + ' + 3 ' + b[2] + ' + ' + b[3] + ' - 4 ' + cd[0] + ' - 2 ' + cd[1] +' - 3 ' + cd[2] + ' - 3 ' + cd[3] + ' >= 0']
        constr=constr+['- ' + a[0] + ' - ' + b[1] + ' + ' + cd[0] + ' >= -1'] 
        constr=constr+['- 2 ' + a[0] + ' - 3 ' + a[1] + ' - 3 ' + a[2] + ' - ' + b[1] + ' - ' + b[2] + ' - 2 ' + b[3] + ' + 2 ' + cd[0] + ' + ' + cd[1] + ' + ' + cd[2] + ' >= -8'] 
        constr=constr+['2 ' + a[1] + ' + ' + a[2] + ' + 2 ' + a[3] + ' + 3 ' + b[1] + ' + ' + b[3] + ' - 3 ' + cd[0] + ' - ' + cd[1] + ' - 2 ' + cd[2] + ' - 3 ' + cd[3] + ' >= 0']
        constr=constr+['3 ' + a[0] + ' + 2 ' + a[1] + ' + 2 ' + a[2] + ' + ' + b[0] + ' + ' + b[1] + ' + 3 ' + b[3] + ' - 4 ' + cd[0] + ' - 2 ' + cd[1] + ' - 3 ' + cd[2] + ' - 3 ' + cd[3] + ' >= 0']
        constr=constr+['- ' + a[0] + ' - ' + a[2] + ' - ' + a[3] + ' - ' + b[0] + ' - ' + b[1] + ' - ' + b[3] + ' + ' + cd[0] + ' + ' + cd[1] + ' + ' + cd[2] + ' >=  -4']
        constr=constr+['- ' + a[0] + ' - ' + a[1] + ' - ' + a[2] + ' - ' + a[3] + ' - ' + b[0] + ' - ' + b[1] + ' - ' + b[2] + ' - ' + b[3] + ' + ' + cd[1] + ' + ' + cd[2] + ' + ' + cd[3] + ' >= -5']
        constr=constr+['- ' + a[1] + ' - ' + a[2] + ' + ' + b[1] + ' - ' + b[2] + ' + ' + b[3] + ' + ' + cd[0] + ' - ' + cd[2] + ' - ' + cd[3] + ' >= -2'] 
        constr=constr+['3 ' + a[0] + ' + 2 ' + a[2] + ' + 3 ' + a[3] + ' + ' + b[1] + ' + 2 ' + b[2] + ' + ' + b[3] + ' - 4 ' + cd[0] + ' - 2 ' + cd[1] + ' - 3 ' + cd[2] + ' - 3 ' + cd[3] + ' >= 0']
        constr=constr+['- ' + a[3] + ' - ' + b[0] + ' - ' + b[3] + ' + ' + cd[0] + ' >= -2'] 
        constr=constr+['- ' + a[0] + ' + ' + a[3] + ' + ' + b[1] + ' - ' + b[2] + ' - ' + b[3] + ' - ' + cd[0] + ' + ' + cd[1] + ' - ' + cd[2] + ' - ' + cd[3] + ' >= -3'] 
        constr=constr+['- ' + a[0] + ' - ' + a[2] + ' - 2 ' + b[1] + ' - ' + b[3] + ' + ' + cd[0] + ' + ' + cd[1] + ' >= -3'] 
        constr=constr+['- 2 ' + a[0] + ' - 2 ' + a[1] + ' - ' + a[2] + ' - 2 ' + a[3] + ' - 2 ' + b[0] + ' - ' + b[1] + ' - 2 ' + b[2] + ' + ' + cd[0] + ' + 2 ' + cd[1] + ' + ' + cd[2] + ' >= -8'] 
        constr=constr+[a[0] + ' - ' + a[3] + ' + ' + b[0] + ' - ' + b[1] + ' + ' + b[3] + ' - ' + cd[0] + ' - ' + cd[2] + ' - ' + cd[3] + ' >= -2']
        return constr
        

    
    @staticmethod #Mixcolumns
    def MC_forward(input1_col, input2_col, output1_col, output2_col, cd):
        constr=[]
        constr=constr+MITMPreConstraints.XOR_forward([input1_col[0],input1_col[2]],[input2_col[0],input2_col[2]],output1_col[3],output2_col[3],cd[0])
        constr=constr+MITMPreConstraints.XOR_forward([output1_col[3],input1_col[3]],[output2_col[3],input2_col[3]],output1_col[0],output2_col[0],cd[1])
        constr=constr+[output1_col[1] + ' - ' + input1_col[0] + ' = 0']
        constr=constr+[output2_col[1] + ' - ' + input2_col[0] + ' = 0']
        constr=constr+MITMPreConstraints.XOR_forward([input1_col[1],input1_col[2]],[input2_col[1],input2_col[2]],output1_col[2],output2_col[2],cd[2])       
        return constr
             

    @staticmethod #Mixcolumns
    def MC_backward(input1_col, input2_col, output1_col, output2_col, cd):
        constr=[]
        constr=constr+[output1_col[1] + ' - ' + input1_col[0] + ' = 0']
        constr=constr+[output2_col[1] + ' - ' + input2_col[0] + ' = 0']    
        constr=constr+MITMPreConstraints.XOR_backward([output1_col[1],output1_col[3]],[output2_col[1],output2_col[3]],input1_col[2],input2_col[2],cd[0]) 
        constr=constr+MITMPreConstraints.XOR_backward([input1_col[2],output1_col[2]],[input2_col[2],output2_col[2]],input1_col[1],input2_col[1],cd[1])
        constr=constr+MITMPreConstraints.XOR_backward([output1_col[0],output1_col[3]],[output2_col[0],output2_col[3]],input1_col[3],input2_col[3],cd[2])
        return constr     

        
    @staticmethod #AddRoundTweakey
    def ART_forward(input1, input2, TK1_1, TK2_1, TK1_2, TK2_2, TK1_3, TK2_3,inter1_var, inter2_var, output1, output2, cd): 
        constr=[]
        constr=constr+MITMPreConstraints.XOR_forward([input1,TK1_1],[input2,TK2_1],inter1_var[0],inter2_var[0],cd[0])
        constr=constr+MITMPreConstraints.XOR_forward([inter1_var[0],TK1_2],[inter2_var[0],TK2_2],inter1_var[1],inter2_var[1],cd[1])
        constr=constr+MITMPreConstraints.XOR_forward([inter1_var[1],TK1_3],[inter2_var[1],TK2_3],output1,output2,cd[2])
        return constr
         

    @staticmethod #AddRoundTweakey
    def ART_backward(input1, input2, TK1_1, TK2_1, TK1_2, TK2_2, TK1_3, TK2_3,inter1_var, inter2_var, output1, output2, cd): 
        constr=[]
        constr=constr+MITMPreConstraints.XOR_backward([output1,TK1_1],[output2,TK2_1],inter1_var[0],inter2_var[0],cd[0])
        constr=constr+MITMPreConstraints.XOR_backward([inter1_var[0],TK1_2],[inter2_var[0],TK2_2],inter1_var[1],inter2_var[1],cd[1])
        constr=constr+MITMPreConstraints.XOR_backward([inter1_var[1],TK1_3],[inter2_var[1],TK2_3],input1,input2,cd[2])
        return constr    


    @staticmethod
    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']
        return c


def column(A, j):
    return [A[j], A[j+4], A[j+8], A[j+12]]
    
   
def ShiftRow_Skinny(A):  #ShiftRow
    return [A[0], A[1], A[2], A[3],\
            A[7], A[4], A[5], A[6],\
            A[10],A[11],A[8], A[9],\
            A[13],A[14],A[15],A[12]]
            
def PT(A):
    return [A[9], A[15], A[8], A[13],\
            A[10], A[14], A[12], A[11],\
            A[0],A[1],A[2], A[3],\
            A[4],A[5],A[6],A[7]]

def main():
    pass

if __name__ == '__main__':
    a=MITMPreConstraints.Match(['a1','a2','a3','a4'],['b1','b2','b3','b4'],['cd1','cd2','cd3','cd4'])
    for i in a:
        print(i)
