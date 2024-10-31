"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""

__author__ = "Aaron Lam Kong Yew"

from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
from math import ceil

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """
    EFFECT_TABLE = ArrayR(len(PokeType))
    with open('type_effectiveness.csv', newline='') as csvfile:
        lines = csvfile.readlines()
        for i, line in enumerate(lines[1:]):
            row_values = line.strip().split(',') # each row is a list of values
            row_array = ArrayR(len(PokeType)) # create an array to store the row values
            for j, value in enumerate(row_values): 
                row_array[j] = float(value) # store each value in the array
            EFFECT_TABLE[i] = row_array

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        """
        return cls.EFFECT_TABLE[attack_type.value][defend_type.value]

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon
        """
        return (len(PokeType))


class Pokemon(ABC): # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health
    
    def set_health(self, health: int) -> None:
        """
        Sets the current health of the Pokemon.
        
        Complexity:
            O(1) for best and worst case - direct assignment operation

        Args:
            health (int): The new health value of the Pokemon.
        
        Returns:
            None
        """
        self.health = health
        
    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> float:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
        """
        defence = other_pokemon.get_defence()
        battle_power = self.get_battle_power()
        if defence < battle_power / 2:
            damage = battle_power - defence
        elif defence < battle_power:
            damage = ceil((battle_power * 5/8) - (defence / 4))
        else:
            damage = ceil(battle_power / 4)

        effective_damage = damage * TypeEffectiveness.get_effectiveness(self.get_poketype(), other_pokemon.get_poketype())
        return effective_damage
    
    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index\
            (self.name) != len(self.evolution_line)-1:
            self._evolve()

    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
        """
        evolved_name = self.evolution_line[self.evolution_line.index(self.name)+1]
        print(f"{self.name} will evolve into {evolved_name}!")
        self.name = evolved_name
        self.battle_power = self.battle_power * 1.5
        self.health = self.health * 1.5
        self.speed = self.speed * 1.5
        self.defence = self.defence * 1.5

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"
