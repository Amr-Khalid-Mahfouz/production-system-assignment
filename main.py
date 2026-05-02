from time import sleep
import os
from pathlib import Path

from engine import parser
from engine.backward import backward_chaining
from engine.forward import forward_chaining


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def show_rules(rules):
    print("rules:")
    for enum, (conclusion, rule) in enumerate(rules.items(), start=1):
        print(f"rule {enum}:")
        print(f"""
  {rule.conditions}\n
  {rule.operators}\n
  {rule.conclusion}
""")

def show_facts(facts):
    print("facts:")
    for fact, value in facts.facts.items():
        print(f"{fact} is {value}")

data_dir = Path(__file__).parent / "data"
rules_path = data_dir / "rules.txt"
facts_path = data_dir / "facts.txt"

parsed_facts = parser.split_file(facts_path)
parsed_rules = parser.split_file(rules_path)

rule = parser.Rule()
rule.split_rule(parsed_rules[0])

facts = parser.facts_base()

for sent in parsed_facts:
    facts.add_fact(sent)

rules = {}
for r in parsed_rules:
    rule = parser.Rule()
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
        result = backward_chaining(rules, parsed_facts, "citrus_fruit")
        print(f"Backward Chaining Result for 'citrus_fruit': {result}")
    elif choice == '2':
        result = forward_chaining(rules, parsed_facts)
        print(f"Forward Chaining Result: {result}")
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

if __name__ == "__main__":
    main_menu()