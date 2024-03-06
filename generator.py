import random
#import radom


def generate_k_mers(seq, k=7):
    oligos = set()
    for i in range(len(seq)-k+1):
        tmp_k_mer = seq[i:i+k]
        oligos.add(tmp_k_mer)
    return oligos

def james_błond(k_mers,number_mutations):
    #print(len(k_mers))
    type_m = [0,1] # 0 - negatywny   1 - pozytywny
    for i in range(number_mutations):
        typ = random.choice(type_m)
        if typ == 0:   # mutacja negatywna
            k_mers.pop(random.randint(0,len(k_mers)))

        if typ == 1:   # mutacja pozytywna
            tmp_k_mer = ""
            for i in range(7):
                tmp_k_mer+=random.choice("AGTC")
                while(tmp_k_mer in k_mers):
                    tmp_k_mer += random.choice("AGTC")
            k_mers.append(tmp_k_mer)
    return k_mers

def generator(n = 200, k=7, mutations=5): #len-dł seq, k-podciag;;
    seq = ""
    k_mers = list()
    for i in range(n):
        seq+=random.choice('ACTG')

    k_mers = list(generate_k_mers(seq,k)) #lista podciągów bez powtórzeń
    number_of_mutations = round((mutations/100)*len(seq))
    k_mers_after_mutation = james_błond(k_mers,number_of_mutations)
    return k_mers_after_mutation

