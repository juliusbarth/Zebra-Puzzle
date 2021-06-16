# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 22:11:10 2021

@author: jfb2444
"""

# Problem:
# There are 5 houses in 5 different colors.
# In each house lives a person with a different nationality.
# These 5 owners drink a certain beverage, smoke a certain brand of cigarette and keep a certain pet.
# No owners have the same pet, brand of cigarette, or drink.

# %% Imports
import sys
from docplex.cp.model import *

# %% Data

# Dictionaries and inverse dictionaries
n = 5
Indeces = range(0,n)

Colors = {"Yellow" : 0, 
         "Blue" : 1, 
         "Red" : 2, 
         "Ivory" : 3, 
         "Green" : 4}

Nationalities = {"Norwegian" : 0, 
                 "Ukranian" : 1, 
                 "Englishman" : 2, 
                 "Spaniard" : 3, 
                 "Japenese" : 4} 

Drinks = {"Water" : 0, 
         "Tea" : 1, 
         "Milk" : 2, 
         "Orange Juice" : 3, 
         "Coffe" : 4}

Smokes = {"Kools" : 0, 
         "Chesterfield" : 1, 
         "Old Gold" : 2, 
         "Lucky Strike" : 3, 
         "Parliament" : 4}

Pets = {"Fox" : 0, 
       "Horse" : 1, 
       "Snails" : 2, 
       "Dog" : 3, 
       "Zebra" : 4}

Colors_inv = {val: key for key, val in Colors.items()}
Nationalities_inv = {val: key for key, val in Nationalities.items()}
Drinks_inv = {val: key for key, val in Drinks.items()}
Smokes_inv = {val: key for key, val in Smokes.items()}
Pets_inv = {val: key for key, val in Pets.items()}

# %% Constraint Programming Model
model = CpoModel(name="ZebraPuzzle")

# Variables (value of variable indicates which house the value from the dictionary is assigned to)
x_color = [model.integer_var(min=0, max=n-1, name="X_color" + str(j)) for j in Colors]
x_nat = [model.integer_var(min=0, max=n-1, name="X_nat" + str(j)) for j in Nationalities]
x_drink = [model.integer_var(min=0, max=n-1, name="X_drink" + str(j)) for j in Drinks]
x_smoke = [model.integer_var(min=0, max=n-1, name="X_smoke" + str(j)) for j in Smokes]
x_pet = [model.integer_var(min=0, max=n-1, name="X_pet" + str(j)) for j in Pets]

# Constraints
model.add(all_diff([x_color[j] for j in Colors_inv]))      # Each house has different color 
model.add(all_diff([x_nat[j] for j in Nationalities_inv])) # Each inhabitant has different nationality
model.add(all_diff([x_drink[j] for j in Drinks_inv]))      # Each inhabitant has different drink
model.add(all_diff([x_smoke[j] for j in Smokes_inv]))      # Each inhabitant has different smoke
model.add(all_diff([x_pet[j] for j in Pets_inv]))          # Each inhabitant has different pet

# The Englishman lives in red house
model.add(x_nat[Nationalities["Englishman"]] == x_color[Colors["Red"]])
#The Spaniard owns the dog.
model.add(x_nat[Nationalities["Spaniard"]] == x_pet[Pets["Dog"]])
# Coffee is drunk in the green house.
model.add(x_drink[Drinks["Coffe"]] == x_color[Colors["Green"]])
# The Ukrainian drinks tea.
model.add(x_nat[Nationalities["Ukranian"]] == x_drink[Drinks["Tea"]])
# The green house is immediately to the right of the ivory house.
model.add(x_color[Colors["Green"]] - x_color[Colors["Ivory"]] == 1)
# The Old Gold smoker owns snails.
model.add(x_smoke[Smokes["Old Gold"]] == x_pet[Pets["Snails"]])
# Kools are smoked in the yellow house.
model.add(x_smoke[Smokes["Kools"]] == x_color[Colors["Yellow"]])
# Milk is drunk in the middle house.
model.add(x_drink[Drinks["Milk"]] == 2)
# The Norwegian lives in the first house.
model.add(x_nat[Nationalities["Norwegian"]] == 0)
# The man who smokes Chesterfields lives in the house next to the man with the fox.
model.add(abs(x_smoke[Smokes["Chesterfield"]] - x_pet[Pets["Fox"]]) == 1)
# Kools are smoked in the house next to the house where the horse is kept.
model.add(abs(x_smoke[Smokes["Kools"]] - x_pet[Pets["Horse"]]) == 1)
# The Lucky Strike smoker drinks orange juice.
model.add(x_smoke[Smokes["Lucky Strike"]] == x_drink[Drinks["Orange Juice"]])
# The Japanese smokes Parliaments.
model.add(x_nat[Nationalities["Japenese"]] == x_smoke[Smokes["Parliament"]])
# The Norwegian lives next to the blue house.
model.add(abs(x_nat[Nationalities["Norwegian"]] - x_color[Colors["Blue"]]) == 1)

# Solve the model
print("\nSolving model....")
model_sol = model.solve(TimeLimit=10)

# Post-processing
if model_sol:
    sol_color = [model_sol[x_color[j]] for j in Colors_inv]
    sol_nat = [model_sol[x_nat[j]] for j in Nationalities_inv]
    sol_drink = [model_sol[x_drink[j]] for j in Drinks_inv]
    sol_smoke = [model_sol[x_smoke[j]] for j in Smokes_inv]
    sol_pet = [model_sol[x_pet[j]] for j in Pets_inv]
    sys.stdout.write("Solve time: " + str(model_sol.get_solve_time()) + "\n")
    
    sol = []
    for i in Indeces:
        tmpColor = Colors_inv[sol_color.index(i)]
        tmpNat = Nationalities_inv[sol_nat.index(i)]
        tmpDrink = Drinks_inv[sol_drink.index(i)]
        tmpSmoke = Smokes_inv[sol_smoke.index(i)]
        tmpPet = Pets_inv[sol_pet.index(i)]
        tmpDict = {'Index' : i, 'Color' : tmpColor, 'Nationality' : tmpNat, 
                   'Drink' : tmpDrink, 'Smoke' : tmpSmoke, 'Pet' : tmpPet}
        sol.append(tmpDict)
        
    for i in Indeces:
        sys.stdout.write("House " + str(sol[i]["Index"]) + " is " + str(sol[i]["Color"]) + 
                         " owned by " + str(sol[i]["Nationality"]) + " drinking " + 
                         str(sol[i]["Drink"]) + " smoking " + str(sol[i]["Smoke"]) + 
                         " and with " + str(sol[i]["Pet"]) + " as a pet. \n")
else:
    sys.stdout.write("No solution found\n")






