from engine import parser

rules_path = r'data\rules.txt'
facts_path = r'data\facts.txt'

parsed_facts = parser.split_file(facts_path)
parsed_rules = parser.split_file(rules_path)

rule = parser.Rule()
rule.split_rule(parsed_rules[4])

print(rule)

facts = parser.facts_base()

for sent in parsed_facts:
    facts.add_fact(sent)

print(facts)