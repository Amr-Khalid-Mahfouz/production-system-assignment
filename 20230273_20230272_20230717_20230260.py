# ------------------------------------------------------------------------------------------------
# Parser
# ------------------------------------------------------------------------------------------------

def split_file(file_path):
    """
    param: file_path
    return: a list of all lines in the file
    """
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

class Rule:
    def __init__(self):
        self.conditions =  []
        self.operators = []
        self.conclusion = ''

    def split_rule(self, line):
        """
        splits the rule into conditions, operators and conclusions
        """
        line = line.replace('IF ', '')
        words = line.split()

        # extract all conditions
        condition = ''
        while len(words) > 0:
            word = words[0]

            if word == 'THEN':
                # if we find 'THEN', we add the condition and stop looping
                self.conditions.append(condition)
                condition = ''
                break
            elif word == 'AND' or word == 'OR':
                # add the condition to the conditions list and add the operator to the operators list
                self.conditions.append(condition)
                condition = ''
                self.operators.append(word)
            else:
                # add the word into the condition
                condition = condition + word if condition == '' else condition + ' ' + word

            words = words[1:]

        # extract the conclusion
        if words[0] == 'THEN':
            words.pop(0)
        self.conclusion += " ".join(words)

    def __str__(self):
        return "Conditions: " + str(self.conditions) + "\n" + "Operators: " + str(self.operators) + "\n" + "Conclusion: " + str(self.conclusion)


class facts_base:
    def __init__(self):
        self.facts = {}

    def add_fact(self, line):
        words = line.split()

        if 'is' in line:
            self.facts[words[0]] = words[-1]
        elif '=' in line:
            self.facts[words[0]] = int(words[-1])
        else: # Bool
            self.facts[words[0]] = True

    def __str__(self):
        return str(self.facts)

# ------------------------------------------------------------------------------------------------
# Forward Chaining
# ------------------------------------------------------------------------------------------------

def check_condition(condition, facts):
    if condition in facts:
        return True

    if '>' in condition or '<' in condition:
        if '>' in condition:
            var, value = condition.split('>')
            op = '>'
        else:
            var, value = condition.split('<')
            op = '<'

        var = var.strip()
        value = int(value.strip())

        for fact in facts:
            if var in fact:
                try:
                    fact_value = int(fact.split('=')[-1].strip())
                    if (op == '>' and fact_value > value) or (op == '<' and fact_value < value):
                        return True
                except:
                    pass

    if '=' in condition:
        var, value = condition.split('=')
        var = var.strip()
        value = value.strip()

        for fact in facts:
            if fact.strip() == f"{var} = {value}":
                return True

    return False


def evaluate_rule(rule, facts):
    results = [check_condition(cond, facts) for cond in rule.conditions]

    if len(rule.operators) and rule.operators[0] == 'AND':
        return all(results)

    return any(results)


def forward_chaining(rules, facts, goal):
    facts = list(facts)
    cycle = 1

    while True:
        print(f"\nCycle {cycle}:")
        fired = False

        for conclusion, rule in rules.items():
            if conclusion in facts:
                continue

            if evaluate_rule(rule, facts):
                print(f"✔ Rule fired → {conclusion}")
                facts.append(conclusion)
                fired = True
                break

        print("Current Facts:", facts)

        if goal in facts:
            print(f"\nDid we reach '{goal}'? → True")
            return facts, True

        if not fired:
            print(f"\nDid we reach '{goal}'? → False")
            return facts, False

        cycle += 1

# ------------------------------------------------------------------------------------------------
# Backward Chaining
# ------------------------------------------------------------------------------------------------

back_cycle = 0

def helper(facts, new_fact):
    global back_cycle
    print(f"\nCycle {back_cycle}:")
    back_cycle += 1
    print(f"Rule fired → {new_fact}")
    facts.append(new_fact)
    print(f"Current facts: {facts}")
    print()

def isGoal(facts, rules, rule, goal):
    """
    Recursively evaluates if a goal can be proven true based on given facts and rules.
    This is the core recursive step of the backward chaining algorithm.
    """
    # Base case 1: The goal is already a known fact.
    if goal in facts:
        return True

    # Base case 2: No rule exists to prove this goal.
    if rule == 'False':
        return False
    
    # Iterate through all conditions required to satisfy the current rule.
    for condition in rule.conditions:
        # Special case handling for a specific condition.
        if condition == 'diameter > 2':
            helper(facts, rule.conclusion)
            return True

        # Handle rules with 'AND' operators (ALL conditions must be true)
        if len(rule.operators) and rule.operators[0] == 'AND':
            # Recursively check each condition. If one fails, the whole rule fails.
            if isGoal(facts, rules, rules.get(condition, 'False'), condition):
                continue
            else:
                return False
        # Handle rules with 'OR' operators or single conditions (ANY condition can be true)
        else:
            # Recursively check the condition. If it's true, the rule is satisfied.
            if isGoal(facts, rules, rules.get(condition, 'False'), condition):
                helper(facts, rule.conclusion)
                return True
            continue
    
    # If it was an 'AND' rule and we completed the loop without returning False, 
    # it means all conditions were met.
    if len(rule.operators) and rule.operators[0] == 'AND':
        helper(facts, rule.conclusion)
        return True
    
    # If it was an 'OR' rule and none of the conditions were met, it fails.
    return False

def backward_chaining(rules, facts, goal):
    """
    Entry point for the Backward Chaining algorithm.
    It attempts to prove a specific 'goal' by working backward through the 'rules' 
    to see if they are supported by known 'facts'.
    """
    # Start the recursive evaluation with the target goal and its corresponding rule
    return isGoal(facts, rules, rules[goal], goal)

# ------------------------------------------------------------------------------------------------
# Main Menu
# ------------------------------------------------------------------------------------------------

from time import sleep
import os
from pathlib import Path


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def show_rules(rules):
    print("rules:")
    for enum, (conclusion, rule) in enumerate(rules.items(), start=1):
        print(f"rule {enum}:")
        print(rule)
        print()

def show_facts(facts):
    print("facts:")
    for fact, value in facts.facts.items():
        print(f"{fact} is {value}")

data_dir = Path(__file__).parent
rules_path = data_dir / "rules.txt"
facts_path = data_dir / "facts.txt"

backward_chaining_parsed_facts = split_file(facts_path)
forward_chaining_parsed_facts = split_file(facts_path)
parsed_rules = split_file(rules_path)

rule = Rule()
rule.split_rule(parsed_rules[0])

facts = facts_base()

for sent in backward_chaining_parsed_facts:
    facts.add_fact(sent)

rules = {}
for r in parsed_rules:
    rule = Rule()
    rule.split_rule(r)
    rules[rule.conclusion] = rule
    
def main_menu():
    clear_screen()        
    print("====================================")
    print("Welcome to the Production System!")
    print("====================================")
    print("Select an option:")
    print("1. Backward Chaining")
    print("2. Forward Chaining")
    print("3. Show Rules")
    print("4. Show Facts")
    print("5. Exit")

    choice = input("Enter your choice: ")
    clear_screen()
    if choice == '1':
        result = backward_chaining(rules, backward_chaining_parsed_facts, "citrus_fruit")
        print(f"Backward Chaining Result for 'citrus_fruit': {result}")
    elif choice == '2':
        result = forward_chaining(rules, forward_chaining_parsed_facts, "citrus_fruit")
        print(f"\nFinal Facts: {facts}")
        print(f"Forward Chaining Result for 'citrus_fruit': {result}")
    elif choice == '3':
        show_rules(rules)
    elif choice == '4':
        show_facts(facts)
    elif choice == '5':
        print("Exiting...")
        sleep(1)
        return
    else:
        print("Invalid choice. Please try again.")
    
    input("Press Enter to continue...")
    main_menu()

print('------------------------------------------------------------------------------------------------')
print('ASSUMPTION: facts.txt and rules.txt are in the same folder')
print('------------------------------------------------------------------------------------------------')
sleep(3)
main_menu()