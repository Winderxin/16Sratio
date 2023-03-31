#!/sdd/project/fengxin/Bin/miniconda3/bin/python

# Author: fengxin
# Date: 20230331

import sys

if len(sys.argv) < 5:
    print("""
Usage:
    16Sratio.py [sample list] [otu table] [output] [method(1,2,3,4)]
        
    sample list format:
        sample1.rRNA\tsample1.rDNA
        sample2.rRNA\tsample2.rDNA
    method:
        1: RNA>0 and DNA=0 --> 16S ratio=100; RNA=0 and DNA=0 --> 16S ratio=0
        2: when DNA=0 --> DNA=1
        3: every DNA number +1
        4: every RNA and DNA number +1
""")
    sys.exit(1)

import pandas as pd

def method1(tab, sample):
    ratio  = pd.DataFrame(index=tab.index)
    for pairsample in sample:
        [rRNA, rDNA] = pairsample.split()
        title    = rRNA + '_' + rDNA + '-16Sratio'
        tempdata = pd.DataFrame(tab[[rRNA,rDNA]])
        tempratio = pd.DataFrame(tempdata[rRNA] / tempdata[rDNA])
        tempratio.columns = [title]
        tempratio.loc[tempdata[(tempdata[rRNA] >0)&(tempdata[rDNA]==0)].index] = 100
        tempratio.loc[tab[(tempdata[rRNA]==0)&(tempdata[rDNA]==0)].index] = 0
        ratio    = pd.merge(ratio, tempdata, left_index=True, right_index=True)
        ratio    = pd.merge(ratio, tempratio, left_index=True, right_index=True)
    return ratio

def method2(tab, sample):
    ratio  = pd.DataFrame(index=tab.index)
    for pairsample in sample:
        [rRNA, rDNA] = pairsample.split()
        title     = rRNA + '_' + rDNA + '-16Sratio'
        tempdata  = pd.DataFrame(tab[[rRNA,rDNA]])
        tempdata[rDNA].loc[tempdata[rDNA]==0] = 1
        tempratio = pd.DataFrame(tempdata[rRNA] / tempdata[rDNA])
        tempratio.columns = [title]
        ratio     = pd.merge(ratio, tempdata, left_index=True, right_index=True)
        ratio     = pd.merge(ratio, tempratio, left_index=True, right_index=True)
    return ratio

def method3(tab, sample):
    ratio  = pd.DataFrame(index=tab.index)
    for pairsample in sample:
        [rRNA, rDNA] = pairsample.split()
        title     = rRNA + '_' + rDNA + '-16Sratio'
        tempdata  = pd.DataFrame(tab[[rRNA,rDNA]])
        tempdata[[rDNA]] += 1
        tempratio = pd.DataFrame(tempdata[rRNA] / tempdata[rDNA])
        tempratio.columns = [title]
        ratio     = pd.merge(ratio, tempdata, left_index=True, right_index=True)
        ratio     = pd.merge(ratio, tempratio, left_index=True, right_index=True)
    return ratio

def method4(tab, sample):
    ratio  = pd.DataFrame(index=tab.index)
    for pairsample in sample:
        [rRNA, rDNA] = pairsample.split()
        title     = rRNA + '_' + rDNA + '-16Sratio'
        tempdata  = pd.DataFrame(tab[[rRNA,rDNA]])
        tempdata  = tempdata + 1
        tempratio = pd.DataFrame(tempdata[rRNA] / tempdata[rDNA])
        tempratio.columns = [title]
        ratio     = pd.merge(ratio, tempdata, left_index=True, right_index=True)
        ratio     = pd.merge(ratio, tempratio, left_index=True, right_index=True)
    return ratio

def main():
    samples = []
    with open(sys.argv[1], 'r') as Sample:
        for line in Sample:
            samples.append(line.strip())

    otudata = pd.read_csv(sys.argv[2], sep='\t', header=0, index_col=0)
    outtab  = pd.DataFrame()
    if sys.argv[4] == '1':
        outtab = method1(otudata, samples)
    elif sys.argv[4] == '2':
        outtab = method2(otudata, samples)
    elif sys.argv[4] == '3':
        outtab = method3(otudata, samples)
    elif sys.argv[4] == '4':
        outtab = method4(otudata, samples)
    else:
        print("Wrong method, allowed method is one of 1 2 3 4\n")
        sys.exit(1)

    outtab.to_csv(sys.argv[3], sep='\t', header=1, index=1)

if __name__ == '__main__':
    main()
