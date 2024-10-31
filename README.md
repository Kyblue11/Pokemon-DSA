# Pokemon Battle Simulator

This project is a Pokemon Battle Simulator that allows players to simulate battles between Pokemon trainers. The battles can be conducted in three different modes: Set, Rotate, and Optimised. The project also includes various data structures and algorithms to manage Pokemon teams and simulate battles efficiently.


## Data Structures and Algorithms

The project uses various data structures to manage Pokemon teams and simulate battles:

- **ArrayStack**: A stack implementation using arrays.
- **CircularQueue**: A circular queue implementation using arrays.
- **ArraySortedList**: A sorted list implementation using arrays.
- **BSet**: A bit set implementation for managing the Pokedex.
- **ReferentialArray**: A referential array implementation.

### Time Complexity

The project includes detailed time complexity analysis for various operations and methods. Here are some examples:

- **Battle Class**:
  - `commence_battle`: O(|elem|) for Set and Rotate modes, O(|elem| * t log t) to O(|elem| * t^2) for Optimised mode.
  - `fight_enemy_pokemon`: O(|elem|) to O(t + |elem|).
  - `attack_and_defend`: O(|elem|) to O(|elem| + t).

- **PokeTeam Class**:
  - `choose_manually`: O(m) to O(num * m).
  - `regenerate_team`: O(t * m + comp__(assemble_team)).
  - `assign_team`: O(t log t) to O(t^2).
  - `assemble_team`: O(t) to O(t^2).

## Test Files

The project includes unit tests to ensure the correctness of the implementation. The test files are located in the `tests` directory:

- `test_task1.py`: Tests for `TypeEffectiveness` class.
- `test_task2.py`: Tests for `PokeTeam` and `Trainer` classes.
- `test_task3.py`: Tests for `Battle` class.
- `test_task4.py`: Tests for `BattleTower` class.

## Running the Program
### Tests
To run the tests, use the `run_tests.py` script. You can specify the task number to run specific tests or run all tests by leaving the task number blank.

```sh
python [run_tests.py](http://_vscodecontentref_/18) [task_number]
```

### Choosing Pokemon Teams
To choose your pokemons manually or generate 6 random pokemons, run the `poke_team.py` script.

```sh
python poke_team.py
```

### Simulating Battles
You, as Ash, will battle agasint in one of the following modes: Set, Rotate, or Optimised. The battle ends when all of your pokemons are defeated or you defeat all of the enemy's pokemons. To simulate 1 round of battle between two trainers, run the `run_tests.py` script with task number 3.

```sh
python run_tests.py 3
```

### Battle Tower
You can also simulate battles in the Battle Tower, where you will battle against multiple trainers, taking turns to fight each trainer's pokemons.
To simulate battles in the Battle Tower, run the `run_tests.py` script with task number 4.

```sh
python run_tests.py 4
```

## Authors
Aaron Lam

## Disclaimer
Monash University holds copyright for code inside the pokemon.py file.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.