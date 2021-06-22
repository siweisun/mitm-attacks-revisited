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
    def XOR_forward(V1_in, V2_in, V1_out, V2_out, cd):
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
    def XOR_backward(V1_in, V2_in, V1_out, V2_out, cd):
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
    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']

        return c
    

def column(A, j):
    return [A[j], A[j+8], A[j+16], A[j+24], A[j+32], A[j+40], A[j+48], A[j+56]]
    
def column512(A, j):
    return [A[j], A[j+16], A[j+32], A[j+48], A[j+64], A[j+80], A[j+96], A[j+112]]

def SR_Groestl(A):
    return [A[0], A[1], A[2],  A[3],  A[4],  A[5],  A[6],  A[7],\
            A[9], A[10],A[11], A[12], A[13], A[14], A[15], A[8],\
            A[18],A[19],A[20], A[21], A[22], A[23], A[16], A[17],\
            A[27],A[28],A[29], A[30], A[31], A[24], A[25], A[26],\
            A[36],A[37],A[38], A[39], A[32], A[33], A[34], A[35],\
            A[45],A[46],A[47], A[40], A[41], A[42], A[43], A[44],\
            A[54],A[55],A[48], A[49], A[50], A[51], A[52], A[53],\
            A[63],A[56],A[57], A[58], A[59], A[60], A[61], A[62]]

def SR_Groestl512(A):
    return [A[0],  A[1],  A[2],   A[3],   A[4],  A[5],   A[6],   A[7],  A[8],  A[9],  A[10],  A[11],  A[12],  A[13],  A[14],  A[15],\
            A[17], A[18], A[19],  A[20],  A[21], A[22],  A[23],  A[24], A[25], A[26], A[27],  A[28],  A[29],  A[30],  A[31],  A[16],\
            A[34], A[35], A[36],  A[37],  A[38], A[39],  A[40],  A[41], A[42], A[43], A[44],  A[45],  A[46],  A[47],  A[32],  A[33],\
            A[51], A[52], A[53],  A[54],  A[55], A[56],  A[57],  A[58], A[59], A[60], A[61],  A[62],  A[63],  A[48],  A[49],  A[50],\
            A[68], A[69], A[70],  A[71],  A[72], A[73],  A[74],  A[75], A[76], A[77], A[78],  A[79],  A[64],  A[65],  A[66],  A[67],\
            A[85], A[86], A[87],  A[88],  A[89], A[90],  A[91],  A[92], A[93], A[94], A[95],  A[80],  A[81],  A[82],  A[83],  A[84],\
            A[102],A[103],A[104], A[105], A[106],A[107], A[108], A[109],A[110],A[111],A[96],  A[97],  A[98],  A[99],  A[100], A[101],\
            A[123],A[124],A[125], A[126], A[127],A[112], A[113], A[114],A[115],A[116],A[117], A[118], A[119], A[120], A[121], A[122]]


def main():
    pass

if __name__ == '__main__':
    a=MITMPreConstraints.XOR_forward('ab','cd','e','f','x5','x6','x7','cd')
    print(a)
