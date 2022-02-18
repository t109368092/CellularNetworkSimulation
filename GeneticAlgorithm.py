import random
import copy
import numpy as np
from math import prod
import statistics

from NetworkSettings import NetworkSettings, GAParameters

class GeneticAlgorithmData:
    dc_ue_mapping_table = {}
    ue_gene_mappig_table = {}
    num_of_dc_ue = 0
    current_chromosome_index = 0
    current_chromosome = []
    chromosomes = []
    chromosomes_data = {"throughput": {}, "fairness": [], "delay": {"data_amount": 0, "queue_time": 0}, "loss": {"drop_data_amount": 0, "sent_data_amount": 0}}
    chromosomes_data_buffer = []
    chromosomes_fitness = []
    selected_chromosomes = []
    best_chromosome_fitness = 0
    min_max_data = {"delay_min": 10000, "delay_max": 0, "loss_min": 10000, "loss_max": 0}


class GeneticAlgorithm:
    def chromosomes_generate():
        ue_gene_mapping_index = 0
        for ue, mapping_bs in NetworkSettings.ue_to_bs_mapping_table.items():
            if len(mapping_bs) == 2:
                GeneticAlgorithmData.dc_ue_mapping_table[ue] = mapping_bs
                GeneticAlgorithmData.ue_gene_mappig_table[ue] = ue_gene_mapping_index
                ue_gene_mapping_index += 1
        GeneticAlgorithmData.num_of_dc_ue = len(GeneticAlgorithmData.dc_ue_mapping_table)

        for _ in range(GAParameters.population_size):
            chromosome = []
            for _ in range(GeneticAlgorithmData.num_of_dc_ue):
                rand_ratio = random.randint(1, 10)
                chromosome.append(rand_ratio)
            
            GeneticAlgorithmData.chromosomes.append(chromosome)
        print("GeneticAlgorithmData.chromosomes: ", GeneticAlgorithmData.chromosomes)

    def save_data_to_buffer():
        GeneticAlgorithm.min_max_update()
        GeneticAlgorithmData.chromosomes_data_buffer.append(GeneticAlgorithmData.chromosomes_data)
        GeneticAlgorithmData.chromosomes_data = {"throughput": {}, "fairness": [], "delay": {"data_amount": 0, "queue_time": 0}, "loss": {"drop_data_amount": 0, "sent_data_amount": 0}}

    def change_current_chromosome():
        if GeneticAlgorithmData.current_chromosome_index < GAParameters.population_size:
            GeneticAlgorithmData.current_chromosome = GeneticAlgorithmData.chromosomes[GeneticAlgorithmData.current_chromosome_index]
            GeneticAlgorithmData.current_chromosome_index += 1
        else:
            GeneticAlgorithm.fitness_calculate()
            if GAParameters.select_method == 1:
                GeneticAlgorithm.select_method_1()
            if GAParameters.select_method == 2:
                GeneticAlgorithm.select_method_2()
            GeneticAlgorithm.crossover()
            print("GeneticAlgorithmData.chromosomes: ", GeneticAlgorithmData.chromosomes)
            GeneticAlgorithmData.chromosomes_fitness = []
            GeneticAlgorithmData.chromosomes_data_buffer = []
            GeneticAlgorithmData.current_chromosome = GeneticAlgorithmData.chromosomes[0]
            GeneticAlgorithmData.current_chromosome_index = 1

    def select_method_1():
        GeneticAlgorithmData.selected_chromosomes = []
        
        for _ in range(GAParameters.population_size):
            choice = random.sample(GeneticAlgorithmData.chromosomes, 2)
            choice_index = [GeneticAlgorithmData.chromosomes.index(choice[0]), GeneticAlgorithmData.chromosomes.index(choice[1])]
            if GeneticAlgorithmData.chromosomes_fitness[choice_index[0]] >= GeneticAlgorithmData.chromosomes_fitness[choice_index[1]]:
                GeneticAlgorithmData.selected_chromosomes.append(choice[0])
            elif GeneticAlgorithmData.chromosomes_fitness[choice_index[0]] < GeneticAlgorithmData.chromosomes_fitness[choice_index[1]]:
                GeneticAlgorithmData.selected_chromosomes.append(choice[1])

    def select_method_2():
        GeneticAlgorithmData.selected_chromosomes = []
        chromosomes_copy = copy.deepcopy(GeneticAlgorithmData.chromosomes)
        chromosomes_fitness_copy = copy.deepcopy(GeneticAlgorithmData.chromosomes_fitness)

        for _ in range(int(GAParameters.population_size / 2)):
            max_chromosome_index = chromosomes_fitness_copy.index(max(chromosomes_fitness_copy))
            GeneticAlgorithmData.selected_chromosomes.append(chromosomes_copy[max_chromosome_index])
            del chromosomes_copy[max_chromosome_index]
            del chromosomes_fitness_copy[max_chromosome_index]
        GeneticAlgorithmData.selected_chromosomes = GeneticAlgorithmData.selected_chromosomes * 2

        if len(GeneticAlgorithmData.selected_chromosomes) < GAParameters.population_size:
            max_chromosome_index = chromosomes_fitness_copy.index(max(chromosomes_fitness_copy))
            GeneticAlgorithmData.selected_chromosomes.append(chromosomes_copy[max_chromosome_index])

        random.shuffle(GeneticAlgorithmData.selected_chromosomes)

    def crossover():
        GeneticAlgorithmData.chromosomes = []

        for i in range(int(len(GeneticAlgorithmData.selected_chromosomes) / 2)):
            crossover_index = random.randint(1, GeneticAlgorithmData.num_of_dc_ue - 1)
            crossovered_chromosome_A = GeneticAlgorithmData.selected_chromosomes[2 * i][:crossover_index] + GeneticAlgorithmData.selected_chromosomes[2 * i + 1][crossover_index:]
            crossovered_chromosome_B = GeneticAlgorithmData.selected_chromosomes[2 * i + 1][:crossover_index] + GeneticAlgorithmData.selected_chromosomes[2 * i][crossover_index:]

            GeneticAlgorithmData.chromosomes.append(crossovered_chromosome_A)
            GeneticAlgorithmData.chromosomes.append(crossovered_chromosome_B)

        if len(GeneticAlgorithmData.selected_chromosomes) % 2 == 1:
            GeneticAlgorithmData.chromosomes.append(GeneticAlgorithmData.selected_chromosomes[-1])

        for i in range(len(GeneticAlgorithmData.selected_chromosomes)):
            mutation = random.uniform(0, 1)
            if mutation < GAParameters.mutation_rate:
                GeneticAlgorithmData.chromosomes[i][random.randint(0, GeneticAlgorithmData.num_of_dc_ue - 1)] = random.randint(1, 10)

    def fitness_calculate():
        for chromosome_data in GeneticAlgorithmData.chromosomes_data_buffer:
            if GAParameters.fitness_method == 1:
                throughput_sum = 0
                for ue_id, data_amount in chromosome_data["throughput"].items():
                    throughput_sum += data_amount

                if throughput_sum > GeneticAlgorithmData.best_chromosome_fitness:
                    GeneticAlgorithmData.best_chromosome_fitness = throughput_sum

                GeneticAlgorithmData.chromosomes_fitness.append(throughput_sum)

            elif GAParameters.fitness_method == 2:
                if NetworkSettings.fairness_method == 1:
                    throughput_sum = 0
                    square_throughput_sum = 0
                    for ue_id, data_amount in chromosome_data["throughput"].items():
                        throughput_sum += data_amount
                        square_throughput_sum += (data_amount ** 2)

                    jain_fairness = (throughput_sum ** 2) / (len(chromosome_data["throughput"]) * square_throughput_sum)

                    if jain_fairness > GeneticAlgorithmData.best_chromosome_fitness:
                        GeneticAlgorithmData.best_chromosome_fitness = jain_fairness

                    GeneticAlgorithmData.chromosomes_fitness.append(jain_fairness)

                if NetworkSettings.fairness_method == 2:
                    avg_jain_fairness = sum(chromosome_data["fairness"]) / len(chromosome_data["fairness"])

                    if avg_jain_fairness > GeneticAlgorithmData.best_chromosome_fitness:
                        GeneticAlgorithmData.best_chromosome_fitness = avg_jain_fairness

                    GeneticAlgorithmData.chromosomes_fitness.append(avg_jain_fairness)

            elif GAParameters.fitness_method == 3:
                avg_delay = chromosome_data["delay"]["queue_time"] / chromosome_data["delay"]["data_amount"]
                avg_loss = chromosome_data["loss"]["drop_data_amount"] / (chromosome_data["loss"]["drop_data_amount"] + chromosome_data["loss"]["sent_data_amount"])
                normalized_avg_delay = (avg_delay - GeneticAlgorithmData.min_max_data["delay_max"]) / (GeneticAlgorithmData.min_max_data["delay_min"] - GeneticAlgorithmData.min_max_data["delay_max"])
                normalized_avg_loss = (avg_loss - GeneticAlgorithmData.min_max_data["loss_max"]) / (GeneticAlgorithmData.min_max_data["loss_min"] - GeneticAlgorithmData.min_max_data["loss_max"])
                delay_loss_indicator = normalized_avg_delay + normalized_avg_loss

                if delay_loss_indicator > GeneticAlgorithmData.best_chromosome_fitness:
                    GeneticAlgorithmData.best_chromosome_fitness = delay_loss_indicator

                GeneticAlgorithmData.chromosomes_fitness.append(delay_loss_indicator)

        print("Fitness: ", GeneticAlgorithmData.chromosomes_fitness)
        print("Best Fitness: ", GeneticAlgorithmData.best_chromosome_fitness)
        mean = statistics.mean(GeneticAlgorithmData.chromosomes_fitness)
        print("Mean Fitness: ", mean)

    def min_max_update():
        avg_delay = GeneticAlgorithmData.chromosomes_data["delay"]["queue_time"] / GeneticAlgorithmData.chromosomes_data["delay"]["data_amount"]
        if avg_delay > GeneticAlgorithmData.min_max_data["delay_max"]:
            GeneticAlgorithmData.min_max_data["delay_max"] = avg_delay
        if avg_delay < GeneticAlgorithmData.min_max_data["delay_min"]:
            GeneticAlgorithmData.min_max_data["delay_min"] = avg_delay

        avg_loss = GeneticAlgorithmData.chromosomes_data["loss"]["drop_data_amount"] / (GeneticAlgorithmData.chromosomes_data["loss"]["drop_data_amount"] + GeneticAlgorithmData.chromosomes_data["loss"]["sent_data_amount"])
        if avg_loss > GeneticAlgorithmData.min_max_data["loss_max"]:
            GeneticAlgorithmData.min_max_data["loss_max"] = avg_loss
        if avg_loss < GeneticAlgorithmData.min_max_data["loss_min"]:
            GeneticAlgorithmData.min_max_data["loss_min"] = avg_loss
        #print(GeneticAlgorithmData.min_max_data["delay_max"])
        #print(GeneticAlgorithmData.min_max_data["delay_min"])

    def current_split_ratio(ue_id):
        split_ratio = GeneticAlgorithmData.current_chromosome[GeneticAlgorithmData.ue_gene_mappig_table[ue_id]]

        return split_ratio