from logic import *

variables = {}
open_list ="[({"
close_list = "])}"
parentheses_map = {')': '(', ']': '[', '}': '{'}

def open_parantheses_counter(terme):
    indexes = [i for i, char in enumerate(terme) if char in open_list]
    return len(indexes), indexes


# comme celle d avant 
def close_parantheses_counter(terme):
    indexes = [i for i, char in enumerate(terme) if char in close_list]
    return len(indexes), indexes

# teste si toutes les ouvertes ont ete fermees et quil n y a pas par exemple le cas )(...
def balancedParantheses(terme):
    stack = []
    
    for char in terme:
        if char in parentheses_map.values():  # If it's an opening parenthesis
            stack.append(char)
        elif char in parentheses_map:  # If it's a closing parenthesis
            if stack and stack[-1] == parentheses_map[char]:
                stack.pop()
            else:
                return False
    return not stack

#renvoie le nombre de parentheses ouvertes qui est aussi le nombre de couples de parenthèses que le terme compte
def parantheses_couples(terme):
    assert balancedParantheses(terme), "Not balanced Terme"
    return (open_parantheses_counter(terme)[0])

def findOpeningParanthesesIndex(terme, closeParentheseIndex):


    openParenthesis = parentheses_map[terme[closeParentheseIndex]]
    openParantheseIndex = closeParentheseIndex
    counter = 1

    while(counter > 0):
        openParantheseIndex -=1
        char = terme[openParantheseIndex]
        if char == openParenthesis:
            counter -= 1
        elif char in close_list: #elif char in set(parentheses_map.keys()): could be a better solution since set lookups are O(1)
            counter += 1
    return openParantheseIndex



# on lui donne l indice dune parenthese ouverte et renvoie l indice de la parenthese fermante
def findClosingParanthesesIndex(terme, openParentheseIndex):

    assert balancedParantheses(terme), "Not balanced Terme"
    stack = []
    for index in range(openParentheseIndex, len(terme)):
        char = terme[index]
        if char in parentheses_map:
            stack.append(char)
        elif char in parentheses_map.values():
            if not stack:
                raise ValueError("Unmatched closing parenthesis at index {}".format(index))
            last_open = stack.pop()
            if parentheses_map[last_open] != char:
                raise ValueError("Mismatched parentheses at index {}".format(index))
            if not stack:
                return index
    raise ValueError("No matching closing parenthesis found")


# renvoie ce qu'il y a entre la parenthese ouverte a l indice i et sa parethese fermante
def getTermFromParantheses(terme,i):
    return terme[i+1:findClosingParanthesesIndex(terme,i)]

def getTermsFromParantheses(terme):
    terms = []
    i = 0
    while i < len(terme):
        if terme[i] in open_list:
            try:
                term = getTermFromParantheses(terme, i)
                terms.append(term)
                i = findClosingParanthesesIndex(terme, i)
            except ValueError as e:
                print(f"Error: {e}")
                break
        i += 1
    return terms

#fonction qui enleve les espaces successifs et laisse un seul espace
def remove_multiple_spaces(terme):
    return ' '.join(terme.split())

def checkType(terme):
    if not terme:
        return None
    
    firstChar = terme[0]
    lastChar = terme[-1]
    if firstChar == "#":
        return ABS
    elif  firstChar in open_list: # this is just a cleaner way for checking
        terms = getTermsFromParantheses(terme)
        if len(terms) == 1 and lastChar in close_list:
            return checkType(getTermFromParantheses(terme,0))
        else:
            return APP
    elif all(char not in terme for char in " ()#.[{]}"):
        return VAR
    else:
        return APP

def isVariable(terme):
    return checkType(terme) == VAR

def isAbstraction(terme):
    return checkType(terme) == ABS

def isApplication(terme):
    return checkType(terme) == APP


#on prend l input de labs en chaine de caractères
def extractInputFromAbs(terme):
    
    if not isinstance(terme, str) or not terme:
        raise ValueError("Invalid input: Input must be a non-empty string")
    
    if checkType(terme) != ABS:
        return ''
    
    beforePeriod,separator,_ = terme.partition('.')
    
    if not separator:
        raise ValueError("Invalid input: Missing '.' in abstraction")
    
    return beforePeriod[1:]


# on prend l output en chaine de caractères
def extractOutputFromAbs(terme):
    if not isinstance(terme, str):
        raise TypeError("Input must be a string")
    
    index_of_point = terme.find('.')
    if index_of_point == -1:
        raise ValueError("Invalid input: Missing '.' in abstraction")
    
    if checkType(terme) != ABS:
        raise ValueError("Invalid input: Term is not of type ABS")
    
    return terme[index_of_point + 1:]

def buildVar(terme):

    if not isinstance(terme, str):
        raise TypeError("Input must be a string")
    
    if checkType(terme) != VAR:
        raise ValueError("Invalid input: Term is not of type VAR")
    # print(terme)
    if terme[0] not in open_list:
        if terme in variables:
            return variables[terme]
        else:
            newVar = new_var(freshVar())
            variables[terme] = newVar
            return variables[terme]
    else :
        return buildTerm(getTermFromParantheses(terme,0))

def buildAbs(terme):
    assert checkType(terme) == ABS, f"Expected ABS type, got {checkType(terme)}"

    input = extractInputFromAbs(terme)
    output = extractOutputFromAbs(terme)

    if terme[0] not in open_list:
        return new_abs(buildTerm(input), buildTerm(output))
    else:
        return buildTerm(getTermFromParantheses(terme,0))

def extract_terms(text):
    terms = []
    current_term = ""
    paranthesis_level = 0

    for char in text:
        if char in open_list:
            if current_term:
                terms.append(current_term)
                current_term = ""
            current_term += char
            paranthesis_level += 1
        elif char in close_list:
            paranthesis_level -= 1
            current_term += char
            if paranthesis_level == 0:
                terms.append(current_term)
                current_term = ""
        elif char == " " and paranthesis_level == 0:
            if current_term:
                terms.append(current_term)
                current_term = ""
        else:
            current_term += char
    if current_term:
        terms.append(current_term)
    return terms


def buildApp(terme):
    if not isinstance(terme, str):
        raise TypeError("Input term must be a string")

    assert checkType(terme) == APP, "Input term must be of type APP"
    
    liste_de_termes = extract_terms(terme)
    if not liste_de_termes: return None

    t = buildTerm(liste_de_termes[0])
    for k in range(1, len(liste_de_termes)):
        if liste_de_termes[k] == '': return t
        t = new_app(t, buildTerm(liste_de_termes[k]))
    
    return t
    
def buildTerm(terme):
    if isVariable(terme): return buildVar(terme)
    elif isAbstraction(terme): return buildAbs(terme)
    elif isApplication(terme): return buildApp(terme)

def parseTerm(terme):
    return (buildTerm(remove_multiple_spaces(terme)))