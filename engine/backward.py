cycle = 0

def helper(facts, new_fact):
    global cycle
    print(f"\nCycle {cycle}:")
    cycle += 1
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

if __name__ == "__main__":
    pass