import os
import csv
import argparse
import re
from pathlib import Path

# This script extracts repeat annotations made via the panTE pipeline from a gff file
# and creates a gff file that can be used by table2asn for annotation submissions
# to genbank. Definitions are taken from https://www.ncbi.nlm.nih.gov/WebSub/html/annot_examples.html
# but this does not seem like an exhaustive list.

#parse commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to a "*.gff" file')
parser.add_argument('-o', '--output', help='path to an output file (default = inputfilename.fixed.gff)')
args = parser.parse_args()

if args.input:
    input_file = Path(args.input)
else:
    input_file = ("test.gff")
    #print("No input file provided, use '-i' and supply a .gff file")
    #raise SystemExit

if args.output:
    output_file = Path(args.output)
else:
    output_file = Path(os.path.join(os.getcwd(),os.path.basename(input_file)+'.fixed.gff'))

gff = {}


#If file with same outputname exists, delete it first
if os.path.isfile(output_file):
    os.unlink(output_file)


with open(input_file) as file:
    input = csv.reader(file, delimiter='\t')
    for line in input:
        if len(line) > 6:
        #look for the 'PiRATE' identifier and then check for the type of repeat
            if line[1] == "RepeatMasker" or "EAhelitron" or "RepeatModeler" or "MiteFinderII" or "LTRharvest" or "LTRdigest":
                elements = []
                for element in line:
                    elements.append(element)

                # microsatellite
                if elements[2] == "microsatellite":
                    rpt_type = "tandem"
                    elements[2] = "microsatellite"
                    if "repeat_unit" in elements[8]:
                        search = re.search('repeat_unit=(.+?)$', elements[8])
                        if search:
                            rpt_unit = search.group(1)
                            elements[8] += "; rpt_type=" + rpt_type + "; satellite_type=microsatellite" + "; rpt_unit=" + rpt_unit
                    else:
                        elements[8] += "; rpt_type=" + rpt_type + "; satellite_type=microsatellite"

                    #print(*elements, sep='\t')

                # repeat_region
                if elements[2] == "repeat_region":
                    if "repeat_family" in elements[8]:
                        search = re.search('repeat_family=(.+?)$', elements[8])
                        if search:
                            rpt_family = search.group(1)
                            if rpt_family.lower() == "ltr/gypsy":
                                elements[2] = "LTR_retrotransposon"
                                elements[8] += "; rpt_type=LTR_retrotransposon; mobile_element_type=LTR:Gypsy; rpt_family=LTR:Gypsy"
                            elif rpt_family.lower() == "ltr/copia":
                                elements[2] = "LTR_retrotransposon"
                                elements[8] += "; rpt_type=LTR_retrotransposon; mobile_element_type=LTR:Copia; rpt_family=LTR:Copia"
                            elif rpt_family.lower() == "dna/tcmar-fot1":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:TcMar-Fot1 ; rpt_family=DNA:TcMar-Fot1 "
                            elif rpt_family.lower() == "dna/tcmar-tc1":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:TcMar-Tc1 ; rpt_family=DNA:TcMar-Tc1 "
                            elif rpt_family.lower() == "dna/tcmar-tc2":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:TcMar-Tc2 ; rpt_family=DNA:TcMar-Tc2 "
                            elif rpt_family.lower() == "dna/tcmar-tc4":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:TcMar-Tc4 ; rpt_family=DNA:TcMar-Tc4 "
                            elif rpt_family.lower() == "dna/cmc-enspm":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:CMC-EnSpm ; rpt_family=DNA:CMC-EnSpm "
                            elif rpt_family.lower() == "dna/mule-mudr":
                                elements[2] = "DNA_transposon"
                                elements[8] += "; rpt_type=DNA_transposon; mobile_element_type=DNA:MULE-MuDR ; rpt_family=DNA:MULE-MuDR "
                            elif rpt_family.lower() == "line/penelope":
                                elements[2] = "LINE_element"
                                elements[8] += "; rpt_type=LINE_element; mobile_element_type=LINE:penelope ; rpt_family=LINE:penelope "
                            elif rpt_family.lower() == "artefact":
                                elements[2] = "mobile_genetic_element"
                                elements[8] += "; mobile_element_type=ARTEFACT  "
                            elif rpt_family.lower() == "unknown":
                                elements[2] = "dispersed_repeat"
                                elements[8] += "; rpt_type=dispersed  "

                        #print(*elements, sep='\t')
                    else:
                        print(elements)


                
                # print the modified list of repeat elements with a tab as the separator
                #print(*elements, sep='\t')
    
