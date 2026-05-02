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