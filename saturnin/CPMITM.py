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
    def Consume_degree(Allone, V, cd):
        constr = []
        constr = constr + [cd + ' - ' + V + ' <= 0']
        constr = constr + [cd + ' - ' + V + ' + ' + Allone + ' >= 0']
        constr = constr + [cd + ' + ' + V + ' + ' + Allone + ' <= 2']
        return constr
    
    @staticmethod
    def Determine_Allone(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' - ' + BasicTools.MinusTerm(V_in) + ' >= ' + str(1-m)]
        constr = constr + [BasicTools.plusTerm(V_in) + ' - ' + str(m) + ' ' + V_out + ' >= 0']
        return constr

    @staticmethod
    def Determine_Allzero(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' + ' + BasicTools.plusTerm(V_in) + ' >= ' + str(1)]
        for j in range(m):
            constr = constr + [V_in[j] + ' + ' + V_out + ' <= 1']
        return constr   

    @staticmethod
    def Determine_ExistOne(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [str(m) + ' ' + V_out + ' - ' + BasicTools.MinusTerm(V_in) + ' >= ' + str(0)]
        constr = constr + [V_out + ' - ' + BasicTools.MinusTerm(V_in) + ' <= ' + str(0)]
        return constr 
        
    @staticmethod
    def XOR_forward(V1_in, V2_in, V1_out, V2_out, Allone1, Allone2, Allzero, cd):
        constr=[]
        constr=constr+[V2_in[0] + ' - ' + V2_out + ' >= 0']
        constr=constr+[V1_in[1] + ' - ' + V1_out + ' + ' + cd + ' >= 0']
        constr=constr+[V2_in[1] + ' - ' + V2_out + ' >= 0']
        constr=constr+[V2_out + ' - ' + V2_in[0] + ' - ' + V2_in[1] + ' >= -1']
        constr=constr+[V1_in[0] + ' - ' + V1_out + ' + ' + cd + ' >= 0']
        constr=constr+[V1_out + ' - ' + V1_in[0] + ' - ' + V1_in[1] + ' - 2 ' + cd + ' >= -1']
        constr=constr+[V2_out + ' - ' + cd + ' >= 0']
        return constr


    @staticmethod
    def XOR_backward(V1_in, V2_in, V1_out, V2_out, Allone1, Allone2, Allzero, cd):
        constr=[]
        constr=constr+[V1_in[0] + ' - ' + V1_out + ' >= 0']
        constr=constr+[V2_in[1] + ' - ' + V2_out + ' + ' + cd + ' >= 0']
        constr=constr+[V1_in[1] + ' - ' + V1_out + ' >= 0']
        constr=constr+[V1_out + ' - ' + V1_in[0] + ' - ' + V1_in[1] + ' >= -1']
        constr=constr+[V2_in[0] + ' - ' + V2_out + ' + ' + cd + ' >= 0']
        constr=constr+[V2_out + ' - ' + V2_in[0] + ' - ' + V2_in[1] + ' - 2 ' + cd + ' >= -1']
        constr=constr+[V1_out + ' - ' + cd + ' >= 0']
        return constr
        
        
    @staticmethod
    def OR_backward(V1, V2, V3, V4, OR):
        constr=[]
        constr=constr+[V1 + ' + ' + V3 + ' - ' + OR + ' >= 0']
        constr=constr+[V2 + ' - ' + V1 + ' + ' + OR + ' >= 0']
        constr=constr+[V4 + ' - ' + V3 + ' + ' + OR + ' >= 0']
        constr=constr+[V2 + ' + ' + V4 + ' + ' + OR + ' <= 2']
        constr=constr+[V1 + ' - ' + V4 + ' - ' + OR + ' >= -1']
        constr=constr+[V3 + ' - ' + V2 + ' - ' + OR + ' >= -1']
        return constr
       
    
    @staticmethod
    def XOR_Mat(V1, V2, V3, V4, V5, V6, allzero):
        constr=[]
        constr=constr+[V3 + ' - ' + V5 + ' >= 0']
        constr=constr+[V2 + ' - ' + V6 + ' >= 0']
        constr=constr+[V6 + ' - ' + V2 + ' - ' + V3 + ' >= -1']
        constr=constr+[V1 + ' - ' + V5 + ' >= 0']
        constr=constr+[V5 + ' - ' + V1 + ' - ' + V3 + ' >= -1']
        constr=constr+[V6 + ' - ' + V2 + ' - ' + V4 + ' >= -1']
        constr=constr+[V3 + ' + ' + V4 + ' - ' + V6 + ' >= 0']
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
    

def ShiftRow_Saturnin(A):
    return [A[0], A[4], A[8], A[12],\
            A[1], A[5], A[9], A[13],\
            A[2], A[6], A[10], A[14],\
            A[3], A[7], A[11], A[15]]
                      
def keyrotation(A):
    return [A[5], A[6], A[7], A[8],\
            A[9], A[10], A[11], A[12],\
            A[13], A[14], A[15], A[0],\
            A[1], A[2], A[3], A[4]]

def main():
    pass

if __name__ == '__main__':
    a=MITMPreConstraints.XOR_forward('ab','cd','e','f','x5','x6','x7','cd')
    print(a)
