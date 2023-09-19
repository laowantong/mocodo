from collections import namedtuple
from random import choice, random, randrange, sample

from .fitness import fitness
from ..argument_parser import rate, positive_integer
from ..mcd import Mcd

def arrange(source, subargs, has_expired):
    
    mcd = Mcd(source)
    layout_data = mcd.get_layout_data()
    links = layout_data["links"]
    successors = layout_data["successors"]
    col_count = layout_data["col_count"]
    row_count = layout_data["row_count"]
    multiplicity = layout_data["multiplicity"]

    verbose = subargs.get("verbose", False)
    population_size = positive_integer(subargs.get("population_size", 1000)) # number of individuals to evolve
    max_generations = positive_integer(subargs.get("max_generations", 300))
    plateau = positive_integer(subargs.get("plateau", 30)) # maximal number of consecutive generations without improvement
    crossover_rate = rate(subargs.get("crossover_rate", 0.9))
    mutation_rate = rate(subargs.get("mutation_rate", 0.06))
    sample_size = positive_integer(subargs.get("sample_size", 7))
    verbose = bool(subargs.get("verbose") is not None) # -r arrange:verbose => {"verbose": ""} => True

    def make_individual():
        """ Construct a chromosome. Select a random node for the first gene. The next ones are chosen
            sequentially. When a gene has another gene to the west, the corresponding node is preferably
            selected among the successors of the latter. NB: Applying the same technic for the north and
            nortwest directions produces better individual, but worse final results. """
        pool = list(range(box_count))
        chromosome = [pool.pop(randrange(box_count))]
        (x, y) = (0, 0)
        for i in range(1, box_count):
            x += 1
            if x == col_count:
                x = 0
                y += 1
                candidates = set()
            else:
                candidates = successors[chromosome[i-1]].intersection(pool)
            chromosome.append(pool.pop(pool.index(choice(tuple(candidates))) if candidates else randrange(len(pool))))
        return Individual(evaluate(chromosome), chromosome)

    def crossover(chromosome_1, chromosome_2):
        """ Produce two children for a given pair of individuals. A random rectangular zone is first selected.
            The corresponding genes in the first individual are copied in the first child. The remaining places
            are filled with the genes of the second individual taken one by one. Symmetrical operations for the
            second child. """
        (x1, y1) = (randrange(col_count), randrange(row_count))
        (x2, y2) = (randrange(x1+1, col_count+1), randrange(y1+1, row_count+1))
        def mate(chromosome_1, chromosome_2):
            used = set(chromosome_1[x+y*col_count] for x in range(x1, x2) for y in range(y1, y2))
            not_used = (allele for allele in chromosome_2 if allele not in used)
            return [chromosome_1[x+y*col_count] if x1 <= x < x2 and y1 <= y < y2 else next(not_used) for y in range(row_count) for x in range(col_count)]
        return (mate(chromosome_1, chromosome_2), mate(chromosome_2, chromosome_1))

    def next_population():
        """ Evolve the population. The best individual is kept. The others are selected by tournament.
            Some selected pairs produce two children. Each selected individual may mutate at certain
            places. Mutation of a gene simply consists in swapping it with another one. """
        result = [best]
        while len(result) < population_size:
            chromosomes = crossover(tournament(), tournament()) if random() < crossover_rate else [tournament()]
            for chromosome in chromosomes:
                for i in range(box_count):
                    if random() < mutation_rate:
                        j = randrange(box_count)
                        (chromosome[i], chromosome[j]) = (chromosome[j], chromosome[i])
                result.append(Individual(evaluate(chromosome), chromosome))
        return result[:population_size]

    def tournament():
        """ Return a COPY of the best chromosome selected among a random sample. """
        return min(sample(population, sample_size)).chromosome[:]
    
    evaluate = fitness(links, multiplicity, col_count, row_count)
    Individual = namedtuple("Individual", ["score", "chromosome"])
    box_count = col_count * row_count
    patience = plateau
    previous_best_score = None
    population = sorted([make_individual() for _ in range(population_size)])
    best = population[0]
    for generation in range(max_generations):
        if best.score == previous_best_score:
            patience -= 1
        else:
            if verbose:
                print("% 3d: %s" % (generation, best.score))
            previous_best_score = best.score
            patience = plateau
        if best.score == (0, 0) or patience == 0 or has_expired():
            # Even if the best individual is not perfect, we stop here
            # without raising an exception.
            break
        population = sorted(next_population())
        best = population[0]
        generation += 1
    result = {
        "distances": best.score[1],
        "crossings": best.score[0],
        "layout": best.chromosome
    }
    mcd.set_layout(**result)
    return mcd.get_clauses()
    
if __name__ == "__main__":
    # python -m mocodo.rewrite._arrange_ga

    from time import time
    import random
    from ..argument_parser import parsed_arguments
    from ..mcd import Mcd

    clauses = """
        SUSPENDISSE: diam
        SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
        CONSECTETUER: elit, sed
        MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

        DF, 11 LOREM, 1N SUSPENDISSE
        LOREM: ipsum, dolor, sit
        TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
        DIGNISSIM: ligula, massa, varius

        DF, 11 RISUS, 0N RISUS
        AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
        RISUS: ultricies, _cras, elementum
        SEMPER, 0N RISUS, 1N DIGNISSIM
    """
    params = parsed_arguments()
    mcd = Mcd(clauses.replace("  ", ""), **params)
    starting_time = time()
    random.seed(42)
    rearrangement = arrange(mcd, {}, lambda: False)
    if rearrangement:
        print()
        mcd.set_layout(**rearrangement)
        print(mcd.get_clauses())
        print()
        print("Cumulated distances:", rearrangement["distances"])
        print("Duration:", time() - starting_time)
        print()
