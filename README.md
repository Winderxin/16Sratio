# 16Sratio
python script for rRNA / rDNA ratio count

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
