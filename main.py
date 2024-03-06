import generator
import generator as g
import random
import itertools


number_of_permutations = 2000 #800-5000
k = 7 #7-10
n = 300 #100-500
population = 300 #100-500
spectrum = g.generator(n = n)
k_mers_used_spectrum = len(spectrum)
number_of_gen = 100 #100-500
current_gen = 1
overlaped_perm_list = []
overlaped_perm_count = []

def fitnessiara(used, n, k):
    ratio = used / (n - k + 1)
    score = 1 - ratio
    return score

def james_nakładka(permutation, k):
    count = 1
    res = permutation[0]
    for s in permutation[1:]:
        # Get the overlap between res and s
        o = max(i for i in range(len(s) + 1) if res.endswith(s[:i]))
        if (o != 0):
            count += 1
            res += s[o:]
    return res, count


def tournament_selection(population, fitness_list):

    tournament_participants = random.sample(population, 6)
    tournament_fitness = [fitness_list[population.index(participant)] for participant in tournament_participants]

    best_index = tournament_fitness.index(max(tournament_fitness))

    return tournament_participants[best_index], tournament_fitness[best_index]

def crossover(parent1, parent2):

    kmer_child1 =[]
    kmer_child2 = []
    crossover_point = random.randint(1, len(parent1)-1)

    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    kmer_child1 = generator.generate_k_mers(child1)
    kmer_child2 = generator.generate_k_mers(child2)
    #print("\n\n", kmer_child1, "\n", kmer_child2)
    return kmer_child1, kmer_child2

def mutate_kmers(kmers, percentage):

    num = int(len(kmers) * (percentage / 100))

    mutated_kmers = []

    selected_kmers = random.sample(kmers, num)

    for kmer in selected_kmers:

        pos = random.randint(0, len(kmer)-1)
        new_base = random.choice("ACTG")
        kmer_list = list(kmer)
        kmer_list[pos] = new_base
        mutated_kmers.append("".join(kmer_list))
    for kmer in kmers:
        if kmer not in selected_kmers:
            mutated_kmers.append(kmer)
    return mutated_kmers


first_gen_fitness = []

done_permutations = 0

for permutation in itertools.permutations(spectrum):
        res, count = james_nakładka(permutation, k)

        overlaped_perm_list.append(res)
        overlaped_perm_count.append(count)
        done_permutations += 1
        first_gen_fitness.append(fitnessiara(count,n,k))
        if done_permutations == number_of_permutations:
            break
print(sum(first_gen_fitness)/len(first_gen_fitness))
#print(overlaped_perm_list)

overlaped_perm_list = overlaped_perm_list[:number_of_permutations]
overlaped_perm_count= overlaped_perm_count[:number_of_permutations]
#for c,s in zip(overlaped_perm_count,overlaped_perm_list):    ### permutacje oraz count równy ilości k-merów użytych do nakładki
#    print(f'count: {c} seq: {s}')



for current_gen in range(number_of_gen):

    fitness_list = [] ### list of fitness scores
    #Tournament
    for f in overlaped_perm_count:
        fitness_list.append(fitnessiara(f,n,k))
    new_population = []
    new_population_score = []

    while(len(new_population) < population):
        tmp_fitness_score = 0
        tmp_winner = ''
        tmp_winner,tmp_fitness_score = tournament_selection(overlaped_perm_list,fitness_list)
        new_population_score.append(tmp_fitness_score)
        new_population.append(tmp_winner)
    #for f,w in zip(new_population_score,new_population):    ### wygrani z tournament i ich fitness
    #    print(f'fitness: {f} winner: {w}')




    offspring = []
    for i in range (round(population/2)):

        r1 = random.randint(0,len(new_population)-1)
        tmp_r1 = new_population[r1]
        new_population.pop(r1)
        r2 = random.randint(0, len(new_population)-1)
        tmp_r2 = new_population[r2]
        new_population.pop(r2)
        ch1, ch2 = crossover(tmp_r1, tmp_r2)
        offspring.append(list(ch1))
        offspring.append(list(ch2))


    mutated_offspring = []


    for of in offspring:
        mutated_offspring.append(mutate_kmers(of,5))
    mutated_offspring_overlapped = []
    mutated_offspring_count = []
    mutated_offspring_fitness = []
    for i in mutated_offspring:
        x, y = james_nakładka(i, k)
        mutated_offspring_overlapped.append(x)
        mutated_offspring_count.append(y)
    for f in mutated_offspring_count:
        mutated_offspring_fitness.append(fitnessiara(f,n,k))

    print(sum(mutated_offspring_fitness)/len(mutated_offspring_fitness)) ###srednia
    #print(f'best: {min(mutated_offspring_fitness)}')  ###najlepsza