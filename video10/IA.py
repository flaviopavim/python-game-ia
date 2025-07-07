import random
import numpy as np

class IA:
    
    def __init__(self, genome=None):
        
        self.max_num_platforms = 10
        
        self.input_size =  5 + (self.max_num_platforms * 3) # Camada de entrada: player_x, player_y, bullet_x, bullet_y, bullet_direction
        self.hidden_size = 32 # Neuronios na camada oculta
        self.output_size = 4  # Camada de saída: left, right, jump, shoot
        
        self.fitness = 0.0 # Avaliação da performance da IA
        
        if genome:
            self.genome = genome
        else:
            # Criar pesos aleatórios para a rede neural
            self.genome = [
                np.random.rand(self.input_size, self.hidden_size),   # Pesos da camada de entrada para a camada oculta
                np.random.rand(1, self.hidden_size),                 # Pesos da camada oculta
                np.random.rand(self.hidden_size, self.output_size),  # Pesos da camada oculta para a camada de saída
                np.random.rand(1, self.output_size)                  # Bias da camada de saída
            ]
            
    def relu(self, x):
        # trazer os valores positivos
        return np.maximum(0, x)
    
    def sigmoid(self, x):
        # função sigmoide
        return 1 / (1 + np.exp(-x))
            
    def choose_action(self, player_x, player_y, enemy, bullets, platforms):
        
        player_relative_x = player_x - enemy.x
        player_relative_y = player_y - enemy.y
        
        closest_bullet_relative_x = 0
        closest_bullet_relative_y = 0
        closest_bullet_direction = -1 # -1: nenhum, 0: esquerda, 1: direita
        min_distance_bullet = float('inf')
        
        for bullet in bullets:
            if not bullet['from_enemy']: # se for tiro do player
                distance = (enemy.x - bullet['x'])**2 + (enemy.y - bullet['y'])**2
                if distance < min_distance_bullet:
                    min_distance_bullet = distance
                    closest_bullet_relative_x = bullet['x'] - enemy.x
                    closest_bullet_relative_y = bullet['y'] - enemy.y
                    closest_bullet_direction = 1 if bullet['direction'] == "right" else 0
                    
        sorted_platforms = sorted(platforms, key=lambda p: np.sqrt((enemy.x - p['x'])**2 + (enemy.y - p['y'])**2))
        platform_inputs = []
        
        for i in range(min(len(sorted_platforms), self.max_num_platforms_considered)):
            platform = sorted_platforms[i]
            platform_inputs.extend([
                platform['x'] - enemy.x,
                platform['y'] - enemy.y,
                platform['width']
            ])
        
        # Monta o vetor de entradas para a rede neural
        inputs = [
            player_relative_x,
            player_relative_y,
            closest_bullet_relative_x,
            closest_bullet_relative_y,
            closest_bullet_direction
        ]
        
        inputs.extend(platform_inputs)
        
        while len(inputs) < self.input_size:
            inputs.append(0)
            
        inputs = np.array([inputs]) # Converte para matriz 2D
        
        hidden_layer_input = np.dot(inputs, self.genome[0]) + self.genome[1] # Camada de entrada para camada oculta
        hidden_layer_output = self.relu(hidden_layer_input) # Ativação ReLU
        
        output_layer_input = np.dot(hidden_layer_output, self.genome[2]) + self.genome[3]
        actions_raw = self.sigmoid(output_layer_input) # Ativação Sigmoid
        
        actions = {
            'move_left': actions_raw[0][0] > 0.5,
            'move_right': actions_raw[0][1] > 0.5,
            'jump': actions_raw[0][2] > 0.5,
            'shoot': actions_raw[0][3] > 0.5
        }
        
        return actions
    
    def calculte_fitness(self, time_survived, damage_dealt, damage_received, jumps_count):
        
        self.fitness = 0.0
        
        self.fitness += damage_dealt * 20
        self.fitness -= damage_received * 15
        self.fitness += time_survived * 0.5
        self.fitness -= jumps_count * 0.2
        
        self.fitness = max(1.0, self.fitness)  # Garantir que a fitness nunca seja menor que 1.0
        
    #def crossover(parent1_genome, parent2_genome):
    #    child_genome = []
    #    for i in range(len(parent1_genome)):
    #        mask = np.random.rand(*parent1_genome[i].shape) < 0.5
    #        child_matrix = np.where(mask, parent1_genome[i], parent2_genome[i])
    #        child_genome.append(child_matrix)
    #    return child_genome
            
    #def mutate(genome, mutation_rate=0.1, mutation_strength=0.5):
    #    mutated_genome = []
    #    for layer in genome:
    #        mutation_mask = np.random.rand(*layer.shape) < mutation_rate
    #        mutation_values = np.random.normal(scale=mutation_strength, size=layer.shape)
    #        mutated_layer = layer + (mutation_mask * mutation_values)
    #        mutated_genome.append(mutated_layer)       
    #    return mutated_genome
    
    #def select_parents(population):
    #    tournament_size = 7
    #    candidates = random.sample(population, min(tournament_size, len(population)))
    #    candidates.sort(key=lambda ia: ia.fitness, reverse=True)
    #    return candidates[0].genome, candidates[1].genome
    
    
    def evolve_population(current_generation, target_population_size):
        
        # Ordena a população atual pela fitness em ordem decrescente
        current_generation.sort(key=lambda ia: ia.fitness, reverse=True)
        
        # Cria uma nova população com o tamanho alvo
        if not current_generation:
            return [IA() for _ in range(target_population_size)]
        
        # Inicializa a nova população
        new_population = []
        
        # Seleciona os melhores indivíduos (elite) para a nova população
        num_elite = target_population_size // 5
        num_elite = min(num_elite, len(current_generation))
        
        # Adiciona os indivíduos da elite à nova população
        for i in range(num_elite):
            new_population.append(IA(genome=current_generation[i].genome))
        
        # Preenche o restante da nova população com filhos gerados por crossover e mutação
        remaining_population_size = target_population_size - len(new_population)
        for _ in range(remaining_population_size):
            
            tournament_size = 7
        
            candidates = random.sample(current_generation, min(tournament_size, len(current_generation)))
            candidates.sort(key=lambda ia: ia.fitness, reverse=True)
            
            parent1_genome = candidates[0].genome
            parent2_genome = candidates[1].genome
            
            # Crossover entre os dois pais
            child_genome = []
            for i in range(len(parent1_genome)):
                mask = np.random.rand(*parent1_genome[i].shape) < 0.5
                child_matrix = np.where(mask, parent1_genome[i], parent2_genome[i])
                child_genome.append(child_matrix)
            
            # Mutação do filho
            mutation_rate=0.1
            mutation_strength=0.5
            
            mutated_genome = []
            for layer in child_genome:
                mutation_mask = np.random.rand(*layer.shape) < mutation_rate
                mutation_values = np.random.normal(scale=mutation_strength, size=layer.shape)
                mutated_layer = layer + (mutation_mask * mutation_values)
                mutated_genome.append(mutated_layer)
            
            # Adiciona o filho mutado à nova população
            new_population.append(IA(genome=mutated_genome))
            
        # Garante que a nova população atinja o tamanho alvo
        while len(new_population) < target_population_size:
            new_population.append(IA())
            
        return new_population