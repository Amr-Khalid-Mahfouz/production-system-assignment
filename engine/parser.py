# goal prove citrus_fruit

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