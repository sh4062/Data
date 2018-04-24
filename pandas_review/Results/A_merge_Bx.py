import numpy as np
import pandas as pd
import os
import argparse
import re
import xlrd


def get_py(filedir, fileA, B_pre):
    '''
    Description:
        Read files from dir    
    Args:
        filedir:dir type str
        fileA: table A's name type str
        B_pre: the prefix of table B's name which should be followed by a number type str

    Returns:
        l:List of input dataframes. type:List
    '''
    l = [""]
    fileList = os.listdir(filedir)
    for filename in fileList:
        if (filename[:len(fileA)] == (fileA)):
            l[0] = (filename)
        elif (filename[:len(B_pre)] == (B_pre)):
            l.append(filename)
    return l


def preprocess(l, PrimaryKey, A_header_index, B_header_index):
    '''
    Description:
    Preprocess data. Deal with data whose primaryKey doesn't exist
    Args:
        l:List of input dataframes. type:List
        PrimaryKey: PrimaryKey of data. type:str
        A_header_index: The index of table A's row number. type:int
        B_header_index: The index of table B's row number. type:int
    Returns:
        Table_A:Table_A. type:DataFrame
        Table_Bs:List of Table_B. type:List
    '''
    Table_A = pd.read_excel(l[0], header=A_header_index)
    Table_A_DealMissing = pd.isna(Table_A[PrimaryKey])
    for i in range(Table_A_DealMissing.size):
        if Table_A_DealMissing[i] == True:
            Table_A = Table_A.drop(i)

    Table_Bs = l[1:]
    for i in range(len(Table_Bs)):
        Table_Bs[i] = pd.read_excel(Table_Bs[i], header=B_header_index)
        Table_B_DealMissing = pd.isna(Table_Bs[i][PrimaryKey])
        for j in range(Table_B_DealMissing.size):
            if Table_B_DealMissing[j] == True:
                Table_Bs[i] = Table_Bs[i].drop(j)

    return Table_A, Table_Bs


def mergedata(Table_A, Table_Bs, PrimaryKey, G_I):
    '''
    Description:
    Merge Table_A and Table_B*
    Args:
        Table_A:Table_A. type:DataFrame
        Table_Bs:List of Table_B. type:List
        PrimaryKey: PrimaryKey of data. type:str
        G_I: Generate information index size type:int
    Returns:
        Table_A:Final Table_A
    '''
    axesjoin = list(Table_A.columns)[G_I:]
    axesjoin.append(PrimaryKey)
    for i in range(len(Table_Bs)):  
        if(Table_Bs[i][PrimaryKey].isin(Table_A[PrimaryKey])).bool():
            axesjoin.pop()
            index_update=Table_A.loc[Table_A[PrimaryKey]==Table_Bs[i][PrimaryKey][1]].index
            Table_A.loc[index_update,axesjoin]=Table_Bs[i][axesjoin].values[0]
            axesjoin.append(PrimaryKey)
        else:
            Table_A=pd.concat([Table_A,Table_Bs[i][axesjoin]],ignore_index=True)

    return Table_A
   


def savedata(Table_A, output_path, output_filename):
    '''
    Description:
    Save data
    Args:
        Table_A:Table_A. type:DataFrame
        output_path: output path type:str
        output_filename: output filename   type:str
    Returns:
        None
    '''
    writer = pd.ExcelWriter(output_path+output_filename)
    Table_A.to_excel(writer, 'sheet1',index=False)
    writer.save()


def main(args):
    l = get_py(args.filedir, args.fileA, args.B_pre)
    print(l)
    Table_A, Table_Bs = preprocess(
        l, args.PrimaryKey, args.A_header_index, args.B_header_index)
    print("----------------------------------------------------------------------------")
    print("Merge Table_A and {} Table_Bs".format(len(Table_Bs)))
    Table_A = mergedata(Table_A, Table_Bs, args.PrimaryKey, args.G_I)
    savedata(Table_A, args.output_path, args.output_filename)
    print("----------------------------------------------------------------------------")
    print("Out put file is saved as {}".format(
        args.output_path+args.output_filename))
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--filedir', type=str, default='./',

                        help='dir for the file')

    parser.add_argument('--fileA', type=str, default="Table_A",

                        help='name for fileA')

    parser.add_argument('--B_pre', type=str, default="Table_B",

                        help='Prefix file B')
    parser.add_argument('--PrimaryKey', type=str, default="c002",

                        help='PrimaryKey')
    parser.add_argument('--A_header_index', type=int, default=1,

                        help='Index of A\'s header')
    parser.add_argument('--B_header_index', type=int, default=1,

                        help='Index of B\'s header')

    parser.add_argument('--G_I', type=int, default=39,

                        help='Generate information index size')
    parser.add_argument('--output_path', type=str,

                        default='./',

                        help='path for output')
    parser.add_argument('--output_filename', type=str,

                        default='result.xlsx',

                        help='output_filename for output')

    args = parser.parse_args()

    print(args)

    main(args)
