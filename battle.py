from __future__ import annotations

"""
This module contains the Battle class which initialises and simulates a battle between two trainers

Depending on the battle mode, the battle can be set, rotate or optimised.
The battle mode determines the order in which the pokemons fight.
Two pokemons are retrieved from each team and put in a fight, where the faster pokemon attacks first.
If both pokemons are alive, they will be deducted 1 health point.
The battle continues until one of the trainers has no pokemons left.
"""

__author__ = "Aaron Lam Kong Yew"

from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode

from math import ceil
from pokemon import Pokemon # typehint

class Battle:
    """
    The Battle class initialises and simulates a battle between two trainers.
    There are three battle modes: Set, Rotate and Optimised.
    The class will determine the winner based on the battle mode selected.
    """

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        """
        Initialises the Battle class with two trainers and the battle mode
        
        Complexity:
            Best: O(1), all assignment operations are constant time
            Worst: O(1), same as best case
            
        Param:
            trainer_1: Trainer - the first trainer
            trainer_2: Trainer - the second trainer
            battle_mode: BattleMode - the battle mode selected
            criterion: str - the criterion used for OPTIMISED battle mode
            
        Returns:
            None
        """
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        """
        Simulates the battle between two trainers until one of them (or both) has no pokemons left.
        raises ValueError:
            if both trainers do not have teams
            
        Complexity:
            Let n be the value of battle_mode.
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
            Let t be the number of team members (self.team_count).
        
            n = 0 or 1:
                Best: O(comp__(set_battle) + comp__(fight_enemy_pokemon) + comp__(battle_result))
                    = O(|elem| + |elem| + 1)
                    = O(|elem|)
                Worst: O(|elem|) - same as best case
                Both best and worst for Set and Optimised battles have the same time complexity as the fight_enemy_pokemon and battle_result methods have a time complexity of O(|elem|)
                  
            n = 2: 
                Best: O(|elem| * t log t)
                Worst: O(|elem| * t^2)
                The best and worse case for Optimised battle mode will always be determined by O(comp__(Poke_team.assign_team)), which has a time complexity of O(t log t) and O(t^2) respectively.
            
            Overall complexity:
            O(comp__(commence_battle)) = O(comp__(pick_team) + comp__(assemble_team))
            
        Param:
            None
            
        Returns:
            None
        """
        n = self.battle_mode.value
        if len(self.trainer_1.get_team()) <= 0 or len(self.trainer_2.get_team()) <= 0:
            raise ValueError("Both trainers must have teams to commence battle")
        
        # determine the battle mode and enter the battle
        if n == 0:
            win_team = self.set_battle()
        elif n == 1:
            win_team = self.rotate_battle()
        elif n == 2:
            win_team = self.optimise_battle()
            
        # return the trainer of the winning team, or None if it's a draw
        if win_team == self.trainer_1.get_team():
            print(f"\n{self.trainer_1.get_name()} with {len(self.trainer_1.get_team())} pokemons left wins the battle!\n*****************************************\n{self.trainer_1.get_team()}")
            return self.trainer_1
        elif win_team == self.trainer_2.get_team():
            print(f"\n{self.trainer_2.get_name()} with {len(self.trainer_2.get_team())} pokemons left wins the battle!\n*****************************************\n{self.trainer_2.get_team()}")
            return self.trainer_2
        elif win_team is None:
            print(f"Both trainer {self.trainer_1.get_name()} and {self.trainer_2.get_name()} have no pokemons left. It's a draw!")
            return None
        
    def _create_teams(self) -> None:
        """
        Create teams for both trainers and assembles them into the appropriate ADT based on the battle mode
        raises ValueError:
            if the trainers are not instances of the Trainer class or the battle mode is not an instance of the BattleMode class
            
        Complexity:
            Let n be the value of battle_mode.
            Let t be the number of team members (self.team_count).
        
            n = 0: 
                Best: O(t + t) = O(t) - the complexity of the pick_team method plus the assemble_team method into an ArrayStack
                Worst: O(t + t) = O(t) - same as best case
                          
            n = 1: 
                Best: O(t + t) = O(t) - the complexity of the pick_team method plus the assemble_team method into a CircularQueue
                Worst: O(t + t) = O(t) - same as best case
                        
            n = 2: 
                best: O(t + t log t) = O(t log t) - the complexity of the pick_team method plus the assemble_team method into an ArraySortedList
                worst: O(t + t^2) = O(t^2) - similar to best case, except assemble_team has a time-complexity of O(t^2) due to shuffling the list
            
            Overall complexity:
            O(comp__(_create_teams)) = O(comp__(pick_team) + comp__(assemble_team))
            
        Param:
            None
            
        Returns:
            None
        """
        if not isinstance(self.trainer_1, Trainer) or not isinstance(self.trainer_2, Trainer) or not isinstance(self.battle_mode, BattleMode) or self.criterion not in PokeTeam.CRITERION_LIST:
            raise ValueError("Invalid instiantiation of Battle class")
        self.trainer_1.pick_team("Random") # pick an initial random team for both trainers
        self.trainer_2.pick_team("Random")
        print(f"Trainer {self.trainer_1.get_name()} has the following pokemons:\n===============================\n{self.trainer_1.get_team()}")
        print(f"Trainer {self.trainer_2.get_name()} has the following pokemons:\n===============================\n{self.trainer_2.get_team()}")
        
        # assemble the teams based on the battle mode
        n = self.battle_mode
        if n.value == 0:
            self.trainer_1.get_team().assemble_team(n)
            self.trainer_2.get_team().assemble_team(n)
        elif n.value == 1:
            self.trainer_1.get_team().assemble_team(n)
            self.trainer_2.get_team().assemble_team(n)
        elif n.value == 2:
            self.trainer_1.get_team().assemble_team(n, self.criterion)
            self.trainer_2.get_team().assemble_team(n, self.criterion)
            
    def set_battle(self) -> PokeTeam | None:
        """
        Set battle called by commence_battle. Each pokemon fights until it faints.
        
        Complexity:
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
        
            Best: O(|elem|) - the complexity of the fight_enemy_pokemon method
            Worst: O(|elem|) - Same as best case
    
        Param:    
            None
            
        Returns:
            PokeTeam: the winning team | None: if it's a draw
        """
        print(f"Team {self.trainer_1.get_name()} assembled Set Battle:\n===============================\n{self.trainer_1.get_team()}")
        print(f"Team {self.trainer_2.get_name()} assembled Set Battle:\n===============================\n{self.trainer_2.get_team()}")
        i = 0
        while len(self.trainer_1.get_team()) > 0 and len(self.trainer_2.get_team()) > 0:
            i += 1
            print(f"\n~ Round {i} ~")
            self.fight_enemy_pokemon() # retrieve more pokemons as long as both teams have pokemons
        return self.battle_result()
    
    def rotate_battle(self) -> PokeTeam | None:
        """
        Rotate battle called by commence_battle. Each pokemon fights then rotates to the back of the team.
        
        Complexity:
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
        
            Best: O(|elem|) - the complexity of the fight_enemy_pokemon method
            Worst: O(|elem|) - Same as best case
    
        Param:    
            None
            
        Returns:
            PokeTeam: the winning team | None: if it's a draw
        """
        print(f"Team {self.trainer_1.get_name()} assembled Rotate Battle:\n===============================\n{self.trainer_1.get_team()}")
        print(f"Team {self.trainer_2.get_name()} assembled Rotate Battle:\n===============================\n{self.trainer_2.get_team()}")
        i = 0
        while len(self.trainer_1.get_team()) > 0 and len(self.trainer_2.get_team()) > 0:
            i += 1
            print(f"\n~ Round {i} ~")
            p1, p2 = self.fight_enemy_pokemon() # retrieve more pokemons as long as both teams have pokemons
            
            # after each round, rotate both pokemons to the back of the team
            if p1.is_alive():
                self.trainer_1.get_team().rotate_pokemon()
            if p2.is_alive():
                self.trainer_2.get_team().rotate_pokemon()
        return self.battle_result()
    
    def optimise_battle(self) -> PokeTeam | None:
        """
        Optimised battle called by commence_battle. The team is sorted based on the criterion and the pokemon with the lowest/highest criterion fights first.
        
        Complexity:
            Let t be the length of a team
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
        
            Best:  O(|elem| * t log t)
                   This occurs when the assign_team has a time-complexity of O(t log t)
            
            Worst: O(|elem| * t^2)
                   This occurs when the assign_team has a time-complexity of O(t^2)
            
        Param:
            None
            
        Returns:
            PokeTeam: the winning team | None: if it's a draw
        """
        print(f"Team {self.trainer_1.get_name()} assembled Optimise Battle:\n===============================\n{self.trainer_1.get_team()}")
        print(f"Team {self.trainer_2.get_name()} assembled Optimise Battle:\n===============================\n{self.trainer_2.get_team()}")
        i = 0
        while len(self.trainer_1.get_team()) > 0 and len(self.trainer_2.get_team()) > 0:
            i += 1
            print(f"\n~ Round {i} ~")
            self.fight_enemy_pokemon() # retrieve more pokemons as long as both teams have pokemons
            
            # after each round, re-sort the team based on the criterion
            self.trainer_1.get_team().assign_team(self.criterion)
            self.trainer_2.get_team().assign_team(self.criterion)
        return self.battle_result()
    
    def fight_enemy_pokemon(self) -> Tuple[Pokemon, Pokemon]:
        """
        Retrieves the first index pokemon from each team and puts them in a fight
        
        Complexity:
            Let t be the length of a team
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
        
            Best:  O(comp__(self.fight) = O(|elem|)
                   This occurs when both pokemons are retrieved from an ArraySortedList
            Worst: O(t + comp__(self.fight)) = O(t + |elem|)
                 = O(|elem|)
                   This occues when a pokemon is retrieved from an ArrayStack or CircularQueue
                   
        Param:
            None
            
        Returns:
            Tuple[Pokemon, Pokemon]: the two pokemons that were retrieved out and fought
        """
        p1 = self.trainer_1.get_team()[0]
        p2 = self.trainer_2.get_team()[0]
        self.fight(p1, p2) # make these 2 pokemons fight each other
        return p1, p2

    def fight(self, p1: Pokemon, p2: Pokemon) -> None:
        """
        Two pokemons are put in a fight. The faster pokemon attacks first, else they attack simultaneously.
        If both pokemons are alive, they will be deducted 1 health point
        
        Complexity:
            Let t be the length of the current team
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
            
            p1 speed != p2 speed:
                    Best:  O(comp__(self.attack_and_defend)
                         = O(|elem|)
                           This occurs when the second attacker dies immediately after the first attack
                    Worst: O(comp__(self.attack_and_defend) + comp__(self.attack_and_defend) + comp__(self.deduct_two))
                         = O(|elem| + |elem| + t)
                         = O(|elem| + t)
                         = O(|elem|)
                           This occurs when both pokemons are alive after the attack and the 'deduct_two' method is called.
                           
            p1 speed == p2 speed:
                    Best:  O(comp__(self.attack_and_defend) + comp__(self.attack_and_defend))
                         = O(|elem|)
                           This occurs when both pokemons pokemons die together, so the 'deduct_two' method is not called
                    Worst: O(comp__(self.attack_and_defend) + comp__(self.attack_and_defend) + comp__(self.deduct_two))
                         = O(|elem| + |elem| + t)
                         = O(|elem| + t)
                         = O(|elem|)
                           This occurs when both pokemons are alive after the simultaneous attack and the 'deduct_two' method is called (when it has fainted)
        
        Param:
            p1: Pokemon - the first pokemon
            p2: Pokemon - the second pokemon
            
        Returns:
            None
        """
        print(f"{p1} vs {p2}")
        self.trainer_1.register_pokemon(p2) # register the enemy pokemon to a trainer's Pokedex
        self.trainer_2.register_pokemon(p1)  
        if p1.get_speed() != p2.get_speed(): # since their speeds are different, the faster pokemon attacks first
            first_attacker, second_attacker = (p1, p2) if p1.get_speed() > p2.get_speed() else (p2, p1)
            first_trainer, second_trainer = (self.trainer_1, self.trainer_2) if first_attacker == p1 else (self.trainer_2, self.trainer_1)
            self.attack_and_defend(first_attacker, second_attacker, first_trainer, second_trainer)
            if second_attacker.is_alive():
                self.attack_and_defend(second_attacker, first_attacker, second_trainer, first_trainer)
        else: # since their speeds are the same, both pokemons attack simultaneously
            self.attack_and_defend(p1, p2, self.trainer_1, self.trainer_2)
            self.attack_and_defend(p2, p1, self.trainer_2, self.trainer_1)
        if p1.is_alive() and p2.is_alive(): # if both pokemons remain alive after a clash, deduct 1 health point from each
            self.deduct_two(p1, p2)
               
    def attack_and_defend(self, attacker: Pokemon, defender: Pokemon, trainer_attacker: Trainer, trainer_defender: Trainer) -> None:
        """
        Called when a pokemon launches an attack on a slower (or eqaul speed) pokemon
        
        Complexity:
            Let |elem| be the number of overall bits used to represent the number of elements in the defending trainer's Pokedex BSet.
            Let t be the length of the defending pokemon's current team
        
            Best:  O(comp__(attacker.attack) + comp__(defender.defend) + comp__(trainer_attacker.get_pokedex_completion) + comp__(trainer_defender.get_pokedex_completion))
                 = O(comp__(TypeEffectiveness.get_effectiveness) + |elem| + |elem|) 
                 = O(|elem|)
                   This occurs when the defending pokemon's team is assembled as an ArrayStack or CircularQueue, and the 'killed' method is not called (it survives the attack)
                   
            Worst: O(comp__(TypeEffectiveness.get_effectiveness) + |elem| + |elem| + comp__(self.killed))
                 = O(|elem| + t)
                 = O(|elem|)
                   This occurs when the defending pokemon's team is assembled as an ArraySortedList and the 'killed' method is called (when it has fainted)
        
        Param:
            attacker: Pokemon - the attacking pokemon
            defender: Pokemon - the defending pokemon
            trainer_attacker: Trainer - the trainer of the attacking pokemon
            trainer_defender: Trainer - the trainer of the defending pokemon
        
        Returns:
            None
        """
        effective_damage = attacker.attack(defender) # calculate the raw damage inflicted by the attacking pokemon
        effective_damage *= (trainer_attacker.get_pokedex_completion() / trainer_defender.get_pokedex_completion()) # multiply the damage by the Pokedex completion ratio
        defender.defend(ceil(effective_damage)) # reduce the health of the defending pokemon by the net damage
        if not defender.is_alive():
            self.killed(attacker, defender, trainer_defender)
         
    def deduct_two(self, p1: Pokemon, p2: Pokemon) -> None:
        """
        Called when both pokemons are alive after a complete round of attack and defend between them.
        Deducts 1 health point from both pokemons (Since all pokemons have more than 2 defence points, the effective damage is 2/2 = 1)
        
        Complexity:
            Let t be the length of the current team
        
            Best: O(1) -  Both pokemons are alive, and 'killed' method is not called (all operations are constant time)
            Worst: O(t) - A pokemon faints and the 'killed' method is called.
                          The fainted pokemon's team is assembled as an ArraySortedList
                          The 'killed' method calls the 'remove_pokemon' method which deletes the first item from the list and shuffles the remaining items to the left.
            
        Param:
            p1: Pokemon - the first pokemon
            p2: Pokemon - the second pokemon
            
        Returns:
            None
        """
        p1.defend(2)
        p2.defend(2)
        
        # check if any of the pokemon(s) have fainted
        if not p1.is_alive() and not p2.is_alive():
            self.killed(p1, p2, self.trainer_2, together_dead=True)
            self.killed(p2, p1, self.trainer_1, together_dead=True)
        elif not p1.is_alive():
            self.killed(p2, p1, self.trainer_1)
        elif not p2.is_alive():
            self.killed(p1, p2, self.trainer_2)
       
    def killed(self, winner_pokemon: Pokemon, dead_pokemon: Pokemon, dead_trainer: Trainer, together_dead: bool = False) -> None:
        """
        Called when a pokemon has fainted. Removes the dead pokemon from the team and levels up the winner pokemon
        
        Complexity:
            Let t be the length of the current team
        
            Best: O(1) - when the fainted pokemon's team is assembled as an ArrayStack or CircularQueue
            Worst: O(t) - when the fainted pokemon's team is assembled as an ArraySortedList
                          The 'remove_pokemon' method deletes the first item from the list and shuffles the remaining items to the left.
            
        Param:
            winner_pokemon: Pokemon - the pokemon that won the round
            dead_pokemon: Pokemon - the pokemon that fainted somewhere in the round
            dead_trainer: Trainer - the trainer that lost its pokemon
            together_dead: bool - True if both pokemons fainted at the same time, so that neither of them levels up
            
        Returns:
            None
        """
        print(f"{dead_pokemon.get_name()} has fainted!")
        dead_trainer.get_team().remove_pokemon() # remove the dead pokemon from the (ADT) team
        if not together_dead: # level up the winner pokemon, that remains alive
            winner_pokemon.level_up()
            
    def battle_result(self) -> PokeTeam | None:
        """
        Returns the winning team, at the end of the Set, Rotate or Optimised battle
        
        Complexity:
            Best: O(1),  all operations are constant time, as
                         the __len__ magic method of the PokeTeam class is O(1)
            Worst: O(1), same as best case
            
        Param:
            None
            
        Returns:
            PokeTeam: the winning team | None: if it's a draw
        """
        if len(self.trainer_1.get_team()) == 0 and len(self.trainer_2.get_team()) == 0:
            return None
        elif len(self.trainer_1.get_team()) == 0:
            return self.trainer_2.get_team()
        else:
            return self.trainer_1.get_team()
            
if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    #b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
