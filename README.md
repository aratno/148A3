# CSC148-Assignment-3
The final assignment in an introductory computer science course at the University of Toronto

### Changelog:
* **Pruning**
    * 
* **Memoization**
    * Keep track of moves and their outcomes in a dictionary of form [state: outcome, state: outcome, ... state, outcome]
    * Store this dictionary in the `Game` class (because these state-outcome pairs exist on a per-game basis)
* **Myopia**
    * Restrict the depth of recursive search 
