"""
This module contains the implementation of the PokeTeam and Trainer classes. 

The PokeTeam class is used to manage a team of Pokemon,
such as choosing a team of Pokemon, regenerating them, or assembling them into the appropriate data structure.
The Trainer class is used to manage a trainer's team and his Pokedex,
such as picking a team of Pokemon, registering Pokemon to the Pokedex, and getting the Pokedex completion percentage.
"""

__author__ = "Aaron Lam Kong Yew"

from pokemon import *
import random
from typing import List
from battle_mode import BattleMode

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet

class PokeTeam:
    """
    This class represents a team of Pokemons stored in an ADT data structure.
    Manipulations can be done to the team such as choosing Pokemons, regenerating them, and assembling them based on the battle mode.
    """
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        """
        Initializes the PokeTeam object.

        Complexity:
            Best: O(self.TEAM_LIMIT) - to initialise an array of size TEAM_LIMIT
            Worst: O(self.TEAM_LIMIT) - same as Best
        
        Param:
            None

        Returns:
            None
        """
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_count = 0
        self.special_called = False
        self.criterion = None
        self.original_team = ArrayR(self.TEAM_LIMIT) # remembers the original team before regeneration
        
    def choose_manually(self) -> None:
        """
        Asks the user to input the number of Pokemons they want in their team and the names of the Pokemons.
        Sets the current team to the Pokemons chosen by the user.
        raises ValueError:
            if the Pokemon name input is not in the list of Pokemon names

        Complexity:
            Let m be the total number of Pokemons (size of the 'POKE_LIST' list).
            Let num be the number of Pokemons the user inputs (between 1 to 6).

            Best: O(m) - where the user chooses only 1 Pokemon.
            Worst: O(num * m) - where num is the number of Pokemons the user inputs and num represents the self.TEAM_LIMIT.

        Param:
            None

        Returns:
            None   
        """
        self.team_count = 0
        num = input("Enter the number of Pokemons you want in your team (between 1 to 6): ")
        while not num.isdigit() or int(num) < 1 or int(num) > self.TEAM_LIMIT:
            num = input("Invalid input. Please enter a number between 1 to 6: ")
        num = int(num)   
        for i in range(num):
            pokemon = input(f"Enter the name of Pokemon {i+1}: ")
            for poke in self.POKE_LIST: # try to match the input with the list of Pokemon names
                if poke().get_name() == pokemon:
                    self.team[i] = poke()
                    self.team_count += 1
                    break
            else:
                raise ValueError(f"Invalid Pokemon name: '{pokemon}'")
        self.original_team = self.team
    
    def choose_randomly(self) -> None:
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1
        self.original_team = self.team

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = "health") -> None:
        """
        Loops through the original ADT team and sets the health of each Pokemon in that team to its non-evolved original health.
        Calls the assemble_team method to assemble the team based on the battle mode and criterion given.

        Complexity:
            Let t be the number of team members (self.team_count).
            Let m be the total number of Pokemons (size of the 'POKE_LIST' list).

            Overall both best and worst time complexity when
            assemble_team -> O(t):        O(t * m + t) = O(t * (m + 1)) = O(t * m).
            assemble_team -> O(t log t):  O(t * m + t log t) = O(t * m).
            assemble_team -> O(t^2):      O(t * m + t^2) = O(t * (m + t)).

            Overall complexity:
            O(comp__(regenerate_team)) = O(t * m + comp__(assemble_team)) where comp__(assemble_team) is the time complexity of the assemble_team method,
            which is either O(t), O(t log t), or O(t^2).

        Param:
            battle_mode: BattleMode - the mode to assemble the team
            criterion: str - the criterion to sort the team for OPTIMISED mode

        Returns:
            None
        """
        for original_pokemon in self.original_team:
            for p in self.POKE_LIST: # compare each original pokemon with the list of all Pokemons
                if original_pokemon.get_evolution() == p().get_evolution(): # matches the original Pokemon with the non-evolved Pokemon by comparing the evolution line
                    original_pokemon.set_health(p().get_health())
        self.team = self.original_team
        self.assemble_team(battle_mode, criterion)
        
    def assign_team(self, criterion: str = None) -> None:
        """
        Sorts the OPTIMISED team based on the criterion given.
        raises ValueError:
            is the team type is not an ArraySortedList
            if the criterion is not in the list of criterion
            
        Complexity:
            Let t be the number of team members (self.team_count).

            Best: O(t log t) - all new items are added at the end of the list.
                               The add method uses a binary search to find the correct position
                               for the new item, which is a O(log n) operation.
            Worst: O(t^2) - new items are inserted at the beginning or in the middle of the list.
                            Shuffling the items to the right is O(t) and adding the new item is O(t).
            
        Param:
            criterion: str - the criterion to sort the team for OPTIMISED mode
            
        Returns:
            None
        """
        if type(self.team) != ArraySortedList:
            raise ValueError("Initial team must be assembled as an ArraySortedList")
        assembled_team = ArraySortedList(len(self.team))
        order = -1 if self.special_called else 1 # sorting order is reversed if special is called
        for i in range(len(self.team)):
            pokemon = self.team[i].value
            if criterion in self.CRITERION_LIST:
                
                # adds the Pokemon to the list with the criterion as the key
                assembled_team.add(ListItem(pokemon, (order * getattr(pokemon, 'get_' + criterion)(), order * i))) # an extra key is added to the ListItem to maintain the original order
            else:
                raise ValueError(f"{criterion} is not in {self.CRITERION_LIST}")
        self.team = assembled_team
        
    def assemble_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        Places the team into the appropriate data structure based on the battle mode given.
        raises ValueError:
            if the criterion is not in the list of criterion (when the battle mode is 2)
            
        Complexity:
            Let n be the value of battle_mode.
            Let t be the number of team members (self.team_count).
        
            n = 0: O(t) - The method creates an ArrayStack (O(t)) and then iterates over the team members to add them to the stack (O(t)).
            
            n = 1: O(t) - The method creates a CircularQueue (O(t)) and then iterates over the team members to add them to the queue (O(t)).
            
            n = 2: 
                Best: O(t log t) - The method creates an ArraySortedList (O(t)) and then iterates over the team members to add them to the list. 
                                   The add operation of ArraySortedList is O(log t) because it uses binary search to find where to insert the new item.
                Worst: O(t^2) -    Involves shuffling the items to the right (O(t)) and adding the new item (O(t)).
                
            Overall complexity:
            O(comp__(assemble_team)) where comp__(assemble_team) is the time complexity of the assemble_team method,
            which is either O(t), O(t log t), or O(t^2).
            
        Param:
            battle_mode: BattleMode - the mode to assemble the team
            criterion: str - the criterion to sort the team for OPTIMISED mode
            
        Returns:
            None
        """
        n = battle_mode.value
        if n == 0:
            assembled_team = ArrayStack(self.team_count)
            for i in range(self.team_count): # transfers the items to a a new stack
                assembled_team.push(self.team[i])
        elif n == 1:
            assembled_team = CircularQueue(self.team_count)
            for i in range(self.team_count): # transfers the items to a new queue
                assembled_team.append(self.team[i])
        elif n == 2:
            assembled_team = ArraySortedList(self.team_count)
            for i in range(self.team_count): # transfers the items to a new ArraySortedList
                if criterion in self.CRITERION_LIST:
                    
                    # adds the Pokemon to the list with the criterion as the key
                    assembled_team.add(ListItem(self.team[i], getattr(self.team[i], 'get_' + criterion)())) # getattr is used to combine 'get_' and the criterion string
                else:
                    raise ValueError(f"{criterion} is not in {self.CRITERION_LIST}")
        self.team = assembled_team # replaces the original stack, queue, or arraysortedlist with the new one
        self.criterion = criterion
                
    def special(self, battle_mode: BattleMode) -> None:
        """
        Changes the order of the team based on the battle mode given.
        
        Complexity:
            Let n be the value of battle_mode.
            Let t be the number of team members (self.team_count).
        
            n = 0: O(t) - The method creates two ArrayStacks (O(t)) and then iterates over the first half of the team members to reverse them.
            
            n = 1: O(t) - The method creates an ArrayStack (O(t)) and then iterates over the second half of the team members to reverse them.
            
            n = 2:
                O(comp__(assign_team)) where comp__(assign_team) is the time complexity of the assign_team method,
                
                Best: O(t log t) - The method creates an ArraySortedList (O(t)) and uses binary search to add members into specific parts of the list.
                Worst: O(t^2) -Involves shuffling the items to the right (O(t)) and adding the new item (O(t)).
                
        Param:
            battle_mode: BattleMode - the mode to assemble the team
            
        Returns:
            None 
        """
        n = battle_mode.value
        if n == 0: # reverses the front of the team by splitting it into two stacks
            temp_stack_1 = ArrayStack(self.team_count//2)
            temp_stack_2 = ArrayStack(self.team_count//2)
            for _ in range(self.team_count//2):
                temp_stack_1.push(self.team.pop())
            for _ in range(self.team_count//2):
                temp_stack_2.push(temp_stack_1.pop())
            for _ in range(self.team_count//2):
                self.team.push(temp_stack_2.pop())
                
        elif n == 1: # reverses the back of the team by using a temporary stack to store the front of the team
            temp_stack = ArrayStack(self.team_count//2)
            for _ in range(self.team_count - self.team_count//2):
                self.team.append(self.team.serve())
            for _ in range(self.team_count//2):
                temp_stack.push(self.team.serve())
            for _ in range(len(temp_stack)):
                self.team.append(temp_stack.pop())
                
        elif n == 2: # inverts the order of the team permanently
            self.special_called = not self.special_called
            self.assign_team(self.criterion)
            
    def __getitem__(self, index: int) -> Pokemon:
        """
        Retrieves the Pokemon at a specified index in the team.

        Complexity:
            Let t be the length of the team.

            self.team = ArrayStack or CircularQueue: O(t) - The method iterates over the team to find the Pokemon.
            self.team = ArraySortedList or ArrayR: O(1) - The magic method directly accesses the Pokemon at index.

        Param:
            index: int - The index of the Pokemon to retrieve from the team.

        Returns:
            pokemon: Pokemon - The Pokemon at the specified index in the team.
        """
        if type(self.team) == ArrayStack:
            temp_stack = ArrayStack(len(self.team))
            for i in range(len(self.team)):
                temp_stack.push(self.team.pop()) # transfers the items to a temporary stack until the desired index is matched
                if i == index:
                    pokemon = temp_stack.peek()
                    break
            for i in range(len(temp_stack)): # tranfers the other (non-desired) items back to the original stack
                self.team.push(temp_stack.pop())
            return pokemon   
        elif type(self.team) == CircularQueue:
            for i in range(len(self.team)): # cycles through the queue to find the desired index
                pokemon = self.team.serve()
                if i == index:
                    found_pokemon = pokemon
                self.team.append(pokemon) # serves each item back to the queue after checking it
            return found_pokemon
        elif type(self.team) == ArraySortedList:
            return self.team[index].value # directly returns the value of the item in the list
        elif type(self.team) == ArrayR:
            return self.team[index] # directly returns the value of the item in the array
        
    def __len__(self) -> int:
        """
        Retrieves the number of Pokemons in the team.
        
        Complexity:
            Best: O(1) - for ArrayStack, CircularQueue, ArraySortedList, and ArrayR.
            Worst: O(1) - Same as best case, as the magic method directly returns the length of the team.
        
        Param:
            None
            
        Returns:
            int: The number of Pokemons in the team.
        """
        if type(self.team) == ArrayR:
            return self.team_count
        else: # for ArrayStack, CircularQueue, and ArraySortedList
            return len(self.team)
        
    def __str__(self) -> str:
        """
        Retrieves the string representation of the team. Each Pokemon is separated by a newline character.
        
        Complexity:
            Let t be the length of the team (len(self.team)) or number of team members (self.team_count).
        
            Best: O(t) - The method iterates over the team length to find the Pokemon.
            Worst: O(t) - The method iterates over the team length to find the Pokemon.
            
        Param:
            None
            
        Returns:
            str: The string representation of the team.
        """
        team_str = ""
        if type(self.team) == ArrayStack:
            temp_stack = ArrayStack(len(self.team))
            for i in range(len(self.team)): # transfers each item to a temporary stack to print it, then transfers it back to the original stack
                team_str += str(self.team.peek()) + "\n"
                temp_stack.push(self.team.pop())
            for i in range(len(temp_stack)):
                self.team.push(temp_stack.pop())
        elif type(self.team) == CircularQueue:
            for i in range(len(self.team)): # serves each item to print it, then appends it back to the queue in a rotating fashion
                pokemon = self.team.serve()
                team_str += str(pokemon) + "\n"
                self.team.append(pokemon)
        elif type(self.team) == ArraySortedList:
            for i in range(len(self.team)): # directly prints the value of each item in the arraysortedlist
                team_str += str(self.team[i].value) + "\n"
        elif type(self.team) == ArrayR:
            for i in range(self.team_count): # directly prints the value of each item in the array
                team_str += str(self.team[i]) + "\n"
        return team_str
    
    def remove_pokemon(self) -> None:
        """
        Removes the first (fronnt) Pokemon in the team.
        
        Complexity:
        Let t be the length of the team (len(self.team))
        
            self.team = ArrayStack: O(1) - The method directly pops the top item from the stack.
            self.team = CircularQueue: O(1) - The method directly serves the front item from the queue.
            self.team = ArraySortedList: O(t) - The method deletes the first item from the list and shuffles the remaining items to the left.
        
        Param:
            None
            
        Returns:
            None
        """
        if type(self.team) == ArrayStack:
            self.team.pop()
        elif type(self.team) == CircularQueue:
            self.team.serve()
        elif type(self.team) == ArraySortedList:
            self.team.delete_at_index(0)
      
    def rotate_pokemon(self) -> None:
        """
        Used only for CircularQueue. Cycles the team by serving the first Pokemon and appending it to the end of the team.
        
        Complexity:
            Best: O(1) - The method serves the front item and appends it to the back of the queue.
            Worst: O(1) - Same as Best.
            
        Param:
            None
            
        Returns:
            None
        """
        pokemon = self.team.serve()
        self.team.append(pokemon)
            
class Trainer:
    """
    This class represents a Pokemon Trainer who has a team of Pokemons and a Pokedex.
    The trainer can pick Pokemons, register Pokemons to the Pokedex, and get the Pokedex completion percentage.
    """

    def __init__(self, name) -> None:
        """
        Initializes a new Trainer object.
        
        Complexity:
            Best: O(PokeTeam.TEAM_LIMIT) - to initialise a PokeTeam object with TEAM_LIMIT number of Pokemons for the trainer.
            Worst: O(PokeTeam.TEAM_LIMIT) - same as Best
        
        Param:
            name: str - the name of the trainer
            
        Returns:
            None  
        """
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet()
        
    def pick_team(self, method: str) -> None:
        """
        Picks a team for the trainer using the specified method and registers each Pokemon in the Pokedex.
        raises ValueError:
            if the method is not 'Random' or 'Manual'

        Complexity:
        Let m be the total number of Pokemons (size of the 'PokeTeam.POKE_LIST' list).
        Let t be the number of Pokemons in the team (either chosen by the user or randomly selected, up to PokeTeam.TEAM_LIMIT).

            method = 'Random':
                Best: O(comp__(choose_randomly) + t * comp__(register_pokemon)) = O(t + t) = O(t)
                Worst: O(comp__(choose_randomly) + t * comp__(register_pokemon)) = O(t + t) = O(t)
                
            method = 'Manual':
                Best: O(comp__(choose_manually) + t * comp__(register_pokemon)) = O(m + t) = O(m)
                Worst: O(comp__(choose_manually) + t * comp__(register_pokemon)) = O(t * m + t) = O(t * m)

        Param:
            method: str - The method to use to pick the team. Must only be 'Random' or 'Manual'.

        Returns:
            None
        """
        if method == 'Random':
            self.team.choose_randomly()
        elif method == 'Manual':
            self.team.choose_manually()
        else:
            raise ValueError(f"Invalid method: '{method}'. Please choose 'Random' or 'Manual'")
        for i in range(len(self.team)): # registers each Pokemon's poketype in the Pokedex
            self.register_pokemon(self.team[i])
            
    def get_team(self) -> PokeTeam:
        """
        Retrieves the pokemon team of the trainer.
        
        Complexity:
            Best: O(1) - The method directly returns the team.
            Worst: O(1) - Same as Best.
            
        Param:
            None
            
        Returns:
            PokeTeam: The team of the trainer.
        """
        return self.team

    def get_name(self) -> str:
        """
        Retrieves the name of the trainer.
        
        Complexity:
            Best: O(1) - The method directly returns the name.
            Worst: O(1) - Same as Best.
            
        Param:
            None
            
        Returns:
            str: The name of the trainer.
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Adds the Poketype of a Pokemon to the trainer's BSet Pokedex.
        
        Complexity:
            Best: O(1) - The method directly adds the Poketype of the Pokemon to the Pokedex, with 'add' and 'get_poketype' being O(1).
            Worst: O(1) - Same as Best.
            
        Param:
            pokemon: Pokemon - The Pokemon to register its Poketype to the Pokedex.
            
        Returns:
            None
        """
        self.pokedex.add(pokemon.get_poketype().value+1) # +1 is added as the BSet only accepts positive integers

    def get_pokedex_completion(self) -> float:
        """
        Retrieves the completion percentage of the trainer's Pokedex.
        
        Complexity:
            Best: O(|elem|), where |elem| is the number of overall bits used to represent the number of elements in the Pokedex BSet.
            Worst: O(|elem|), same as Best.
            
        Param:
            None
            
        Returns:
            float: The completion percentage of the trainer's Pokedex.
        """
        return round(len(self.pokedex) / len(PokeType), 2)

    def __str__(self) -> str:
        """
        Retrieves the string representation of the trainer.
        
        Complexity:
            Best: O(|elem|), where |elem| is the number of overall bits used to represent the number of elements in the Pokedex BSet.
            Worst: O(|elem|), same as Best.
            
            = O(comp__(get_pokedex_completion)) where comp__(get_pokedex_completion) is the time complexity of the get_pokedex_completion method.
            
        Param:
            None
            
        Returns:
            str: The string representation of the trainer.
        """
        return f"Trainer {self.name} Pokedex Completion: {format(self.get_pokedex_completion() * 100, '.0f')}%"

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Manual")
    print(t)
    print(t.get_team())