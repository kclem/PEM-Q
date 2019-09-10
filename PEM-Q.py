#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Mengzhu
#Date:2019.9.1

"""PEM-Q
    
    This is a pipeline to analyze PEM-seq data or data similar, help you analyze repair outcome of your DNA library.

    Copyright (C) 2019  Mengzhu Liu

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Author: Mengzhu LIU
Contact: liu.mengzhu128@gmail.com/liumz@pku.edu.cn

Usage:
    PEM-Q.py <genome> <sample> <cutsite> <primer_chr> <primer_start> <primer_end> <primer_strand> <primer>

Options:
-h --help               Show this screen.
-v --version            Show version.
<genome>                reference genome(hg19/hg38/mm9/mm10).
<sample>                sample name of input file <sample>.fq.gz.
<cutsite>               position of cutsite (3' break end of positive strand)
<primer_chr>            chromosome of red primer
<primer_start>          start of red primer
<primer_end>            end of red primer
<primer_strand>         strand of red primer
<primer>                sequence of red primer

In this script, reads will be mapped by bwa-mem, BOTH single end or 
pair end reads are compatible. When analyzing PEM-seq data, you should 
also provide adapter and primer sequences, so that adapter alignment 
and no primer filter can be done.

Input file: fastq file / Output file: informative tab files
Last Update:2019.9.2

"""

import os
import sys
import threading
from time import time
from docopt import docopt

def run_script(sample=None, cutsite=None, genome=None, primer=None, primer_chr=None, primer_start=None, primer_end=None, primer_strand=None):
    
    start_time = time()
    
    # basename = "LY015B_100"
    # cutsite = "36573328"
    # genome = "hg38"
    # primer = "AGGATCTCACCCGGAACAGC"
    basename = sample
    
    os.system("mkdir log")
    
    print("######## Reads alignment... ########")
    cmd = "align_make.py {} {}_R1.fq.gz {}_R2.fq.gz -a CCACGCGTGCTCTACA -p {} -r {} -s {} -e {} -d {}".format(genome,basename,basename,primer,primer_chr,primer_start,primer_end,primer_strand)
    print(cmd)
    os.system(cmd)
    
    print("######## Barcode dedup... ########")
    cmd = "rmb_dedup.py {} 17".format(basename)
    print(cmd)
    os.system(cmd)
    
    print("######## Define transloc... ########")
    cmd = "define_transloc.py {} {}".format(basename, cutsite)
    print(cmd)
    os.system(cmd)
    
    print("######## Define indels... ########")
    cmd = "define_indel.py {} {}".format(basename, cutsite)
    print(cmd)
    os.system(cmd)
    
    print("All done, please check log files!")
    
    print("PEM-Q Done in {}s".format(round(time()-start_time, 3)))
    
def main():
    args = docopt(__doc__,version='PEM-Q 2.0')
    
    kwargs = {'sample':args['<sample>'], 'cutsite':args['<cutsite>'],'genome':args['<genome>'],\
    'primer':args['<primer>'],'primer_chr':args['<primer_chr>'],'primer_start':args['<primer_start>'],\
    'primer_end':args['<primer_end>'],'primer_strand':args['<primer_strand>']}
    
    print('[PEM-Q] genome: ' + str(kwargs['genome']))
    print('[PEM-Q] sample: ' + str(kwargs['sample']))
    print('[PEM-Q] cutsite: ' + str(kwargs['cutsite']))
    print('[PEM-Q] primer: ' + str(kwargs['primer']))
    print('[PEM-Q] primer_chr: ' + str(kwargs['primer_chr']))
    print('[PEM-Q] primer_start: ' + str(kwargs['primer_start']))
    print('[PEM-Q] primer_end: ' + str(kwargs['primer_end']))
    print('[PEM-Q] primer_strand: ' + str(kwargs['primer_strand']))
    
    try:
        run_script(**kwargs)
    except KeyboardInterrupt:
        sys.stderr.write("See you~ :)\n")
        sys.exit(0)
    
if __name__ == "__main__":
    main()
    
    