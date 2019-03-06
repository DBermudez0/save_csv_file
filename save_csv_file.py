def read_files(dname = 'str', file = 'str'):
      import os
      import numpy as np
      files = os.listdir(dname)
      loc = []
      header_1 = input('Enter selected header prior to the sequence of interest:')
      header_2 = input('Enter selected header after the sequence of interest:')
      for file in files:
            if file[0] != '.':
                  i = 0
                  file_full_name = ''.join([dname, file])

                  f = open(file_full_name, 'r')
                  for line in f.readlines():
                        i += 1

                        if header_1 in line[:]:
                                   loc.append(i)
                        elif header_2 in line[:]:
                                   loc.append(i)
                        elif header_2 == '':
                                    count = i
                                    loc.append(count)
                      
      return(loc)


def selec_sequence(dname = 'str'):
            import os
            import re
            name_file = input("What is the name of the selected file:")
            file_full_name = ''.join([dname, name_file])
            f = open(file_full_name, 'r')
            a = read_files(dname = dname, file = name_file)
            
            if len(a) == 1:
                  c = ''.join(f.readlines()[a[0]:])
                  return(re.sub('\n', '', c))
            else:
                  c = ''.join(f.readlines()[a[0]:(a[1]-1)])
                  return(re.sub('\n', '', c))

def reverse_compl_seq(dname = 'str'):
      sequence = selec_sequence(dname = dname)
      answer = []
      complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'a':'t', 't':'a', 'g':'c', 'c':'g'}
      for nucleotide in sequence:
           answer.append(complement[nucleotide])
      csequence = ''.join(answer[::-1])
      return(sequence, csequence)

def charposition(string, char):
      pos = []
      for n in range(len(string)):
            if string[n:n+len(char)] == char:
                  pos.append(n)
      return([x+1 for x in pos])

def cut_sequences(dname = 'str'):

      sequence, csequence = reverse_compl_seq(dname = dname)
      cut_seq = []
      cut_cseq = []
      num_PAM = int(input("How many PAM specific are there for this PAM sequence?:"))
      for k in range(0, num_PAM):
            nucleotide = input("Which nucleotide of the (PAM sequences = NGG) do you what to locate (A, T, C, or G):")
            sequence = sequence.upper()
            csequence = csequence.upper()
            loc_nucl_sq= charposition(sequence, nucleotide)
            loc_nucl_csq = charposition(csequence, nucleotide)
            loc_nucl_sq = sorted(x for x in loc_nucl_sq if x >= 20)
            loc_nucl_csq = sorted(x for x in loc_nucl_csq if x >= 20)
           
            
            for i in range(0, len(loc_nucl_sq)):
                  cut_seq.append([sequence[(loc_nucl_sq[i]-19):loc_nucl_sq[i]+1], "+"])
            for j in range(0, len(loc_nucl_csq)):
                  cut_cseq.append([csequence[(loc_nucl_csq[j]-19):loc_nucl_csq[j]+1], "-"])

             
      return(cut_seq, cut_cseq)

def save_csv_file(dname = 'str'):
      import csv
      a = cut_sequences(dname = dname)
      gRNA = a[0] + a[1]
      csv.register_dialect('myDialect', delimiter = '|', lineterminator = '\r\n\r\n')
      name_file = input("What is the name of the selected file:")
      num_of_header = input("What number of sequence header is this? (Ex:ENST00000352993.7_0):")
      with open(name_file+'_'+num_of_header+'.csv', 'w') as f:
            writer = csv.writer(f, dialect='myDialect')
            writer.writerows(gRNA)
            f.close()
            
