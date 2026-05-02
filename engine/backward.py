def isGoal(facts, rules, rule, goal):
    if goal in facts:
        return True

    if rule == 'False':
        return False
    
    for condition in rule.conditions:
        if condition == 'diameter > 2':
            facts.append(rule.conclusion)
            return True

        if len(rule.operators) and rule.operators[0] == 'AND':
            if isGoal(facts, rules, rules.get(condition, 'False'), condition):
                continue
            else:
                return False
        else:
            if isGoal(facts, rules, rules.get(condition, 'False'), condition):
                facts.append(rule.conclusion)
                return True
            continue
    
    if len(rule.operators) and rule.operators[0] == 'AND':
        facts.append(rule.conclusion)
        return True
    
    return False

def backward_chaining(rules, facts, goal):
    return isGoal(facts,rules,rules[goal],goal)

if __name__ == "__main__":
    pass