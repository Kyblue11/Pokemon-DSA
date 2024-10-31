"""
This module contains the implementation of the BattleTower class 
which is responsible for commencing battles between a player and the enemy trainers.

Both the player and the enemy trainers will have a team of Pokemon to battle with as well as a set number of lives.
Each time a battle is lost, the player or the enemy trainer will lose a life.
The Battle Tower ends when either the player or the enemy trainers run out of lives.
"""

__author__ = "Aaron Lam Kong Yew"

from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple

from random import randint
from battle import Battle, BattleMode

class BattleTower:
    """
    The BattleTower class will simulate a series of battles between the created player and enemy trainers.
    At the end of each battle, the player will either lose a life or defeat the enemy trainer.
    The Battle Tower cycle will terminate when either the player or all enemy trainers have run out of lives.
    """
    MIN_LIVES = 1
    MAX_LIVES = 3
    
    def __init__(self) -> None:
        """
        Initialises the BattleTower object.
        
        Complexity:
            Best: O(1), all assignment operations are constant time
            Worst: O(1), same as best case
            
        Param:
            None
            
        Returns:
            None
        """
        self.my_trainer = None
        self.enemy_teams = None
        self.enemy_lives = 0
        self.player_lives = 0
        self.enemies_defeated_count = 0
        
    def set_my_trainer(self, trainer: Trainer) -> None:
        """
        Registers the player's trainer to the BattleTower.
        
        Complexity:
            Best: O(comp__(random.randint))
            Worst: O(comp__(random.randint))
            
        Param:
            trainer: Trainer, the player's chosen trainer
            
        Returns:
            None
        """
        self.my_trainer = trainer
        self.player_lives = randint(self.MIN_LIVES, self.MAX_LIVES)
        
    def generate_enemy_trainers(self, num_teams: int) -> None:
        """
        Randomly generates enemy trainers and their teams, then registers them to the BattleTower.
        
        Complexity:
            Let n be num_teams
            Let t be the number of Pokemon in each enemy team, called by both 'pick_team' and 'assemble_team' methods
            
            Best: O(comp__(random.randint) + t) - Only 1 enemy team is generated
            Worst: O(n * (comp__(random.randint) + t)) - All enemy teams are generated
        
        Param:
            num_teams: int, the number of enemy trainers to generate
            
        Returns:
            None
        """
        self.enemy_teams = CircularQueue(num_teams)
        for i in range(num_teams): # create enemy trainers and assemble their teams
            enemy_trainer = Trainer('Enemy ' + str(i))
            enemy_trainer.pick_team("Random")
            enemy_trainer.get_team().assemble_team(BattleMode.ROTATE)
            enemy_trainer.life = randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES)
            self.enemy_teams.append(enemy_trainer)
            self.enemy_lives += enemy_trainer.life
            
    def battles_remaining(self) -> bool:
        """
        Returns True or False depending on whether there are still battles to be fought in the Battle Tower.
        
        Complexity:
            Best: O(1), all comparison operations are constant time
            Worst: O(1), same as best case
        
        Param:
            None
            
        Returns:
            bool: True if there are still battles to be fought, False otherwise
        """
        return True if self.player_lives > 0 and self.enemy_lives > 0 else False
    
    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Simulates a complete battle between the player and an alive enemy trainer.
        
        Complexity:
            Let |elem| be the number of overall bits used to represent the number of elements in a trainer's Pokedex BSet.
            Let t be the number of team members of a trainer
            Let m be the total number of Pokemons (size of the 'POKE_LIST' list).

            Best: O(|elem| + (t * m))
            Worst: O(|elem| + (t * m))
            
            Overall complexity:
            O(comp__(next_battle)) = O(comp__(commence_battle) + comp__(regenerate_team))
        
        Param:
            None
            
        Returns:
            Tuple[Trainer, Trainer, Trainer, int, int]: A tuple containing the following elements:
                - int: The result of the battle, 1 if the player wins, -1 if the enemy wins
                - Trainer: The player's trainer
                - Trainer: The served enemy trainer
                - int: The remaining lives of the player after the battle
                - int: The remaining lives of the enemy after the battle
        """
        print(f"Player: {self.my_trainer.name}, Lives: {self.player_lives}")
        enemy_trainer = self.enemy_teams.serve()
        print(f"Enemy Trainer: {enemy_trainer.name}, Lives: {enemy_trainer.life}")
        
        # intantiate a battle object and commence the battle
        battle = Battle(self.my_trainer, enemy_trainer, BattleMode.ROTATE)
        winner = battle.commence_battle()
        
        if winner == self.my_trainer: # player wins
            result = 1
            enemy_trainer.life -= 1
            self.enemy_lives -= 1
            self.enemies_defeated_count += 1
        else: # enemy wins
            result = -1 
            self.player_lives -= 1
            
        # regenerate the teams for the next battle, if the trainers are still alive
        self.my_trainer.get_team().regenerate_team(BattleMode.ROTATE)
        if enemy_trainer.life > 0:
            enemy_trainer.get_team().regenerate_team(BattleMode.ROTATE)
            self.enemy_teams.append(enemy_trainer)
        return result, self.my_trainer, enemy_trainer, self.player_lives, self.enemy_lives
    
    def enemies_defeated(self) -> int:
        """
        Returns the number of enemy trainers defeated by the player.
        
        Complexity:
            Best: O(1) - as self.enemies_defeated_count is a class attribute
            Worst: O(1), same as best case
        
        Param:
            None
            
        Returns:
            int: The number of enemy trainers defeated by the player
        """
        return self.enemies_defeated_count