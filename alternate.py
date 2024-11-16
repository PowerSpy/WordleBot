import math
from collections import defaultdict

valid_words = []

with open("valid-wordle-words.txt", "r") as file:
    for line in file:
        valid_words.append(line.strip())
answers = []
with open("answers.txt", "r") as file:
    for line in file:
        answers.append(line.strip())

def fill_answers(a):
    with open("possible_answers.txt", "w") as file:
        file.writelines([f"{line}\n" for line in a])

def fill_guesses(g):
    with open("good_guesses.txt", "w") as file:
        file.writelines([f"{line}\n" for line in g])

def get_feedback(guess, answer):
    """
    Given a guess and an answer, return the feedback pattern.
    Green = correct letter, Yellow = wrong position, Gray = letter not in word
    """
    feedback = []
    answer_copy = list(answer)
    
    # First pass: Check for greens
    for i, g in enumerate(guess):
        if g == answer[i]:
            feedback.append('G')  # Green
            answer_copy[i] = None  # Remove from answer to avoid double-counting
        else:
            feedback.append(None)
    
    # Second pass: Check for yellows and grays
    for i, g in enumerate(guess):
        if feedback[i] is None:
            if g in answer_copy:
                feedback[i] = 'Y'  # Yellow
                answer_copy[answer_copy.index(g)] = None  # Remove the first occurrence
            else:
                feedback[i] = 'X'  # Gray
    
    return ''.join(feedback)

def calculate_entropy(guess, possible_answers):
    """
    Calculate the entropy of a guess based on the remaining possible answers.
    """
    feedback_groups = defaultdict(list)
    
    # Group possible answers by feedback pattern
    for answer in possible_answers:
        feedback = get_feedback(guess, answer)
        feedback_groups[feedback].append(answer)
    
    # Calculate entropy
    total_answers = len(possible_answers)
    entropy = 0
    
    for feedback, group in feedback_groups.items():
        prob = len(group) / total_answers
        entropy -= prob * math.log2(prob)
    
    return entropy

def sort_words_by_entropy(possible_words, possible_answers):
    """
    Sort words by their entropy, from highest to lowest.
    """
    word_entropy = [(word, calculate_entropy(word, possible_answers)) for word in possible_words]
    word_entropy.sort(key=lambda x: x[1], reverse=True)  # Sort by entropy, descending
    
    return [word for word, _ in word_entropy]
def main():
    excluded = ""
    let_dic = {}
    green = "-----"
    while True:
        letters = []
        valids = []
        guesses = []
        excluded_positions = {}  # Store the positions where yellow letters cannot be
        
        user = input("Enter Locked Values (green): ")
        if user == "restart" or user == "exit":
            break
        if user == "":
            user = "-----"
        green = "".join(c1 if c1.isalpha() else c2 for c1, c2 in zip(green, user))
        print("New Green:", green)
        user_guess = input("Enter string of letters (yellow): ")
        num_yellow = len(user_guess)
        for i in range(num_yellow):
            yellow_letters = user_guess[i]
            
            for yellow_letter in yellow_letters:
                forbidden_positions = input(f"Enter positions where {yellow_letter} cannot be (use _ for allowed positions): ")
                
                # Store the forbidden positions for the yellow letter
                excluded_positions[yellow_letter] = forbidden_positions
        excluded += input("Enter string of excluded words (gray): ")
        excluded = "".join(set(excluded))
        
        
        
        if green == "-----" and user_guess == None and excluded == None:
            # Write the full list of answers and guesses
            fill_answers(answers)
            fill_guesses(valid_words)
        
        if len(green) == 5:
            for i, l in enumerate(green):
                if l != "-":
                    let_dic[i] = l
        if user_guess != None:
            for l in user_guess:
                letters.append(l)
        
        # Filter valid words (these are guesses that could be valid guesses for the next guess)
        for word in valid_words:
            locked = True
            unlocked = True
            exclude = True
            for key, val in let_dic.items():
                if word[key] != val:
                    locked = False
                    break
            if not locked:
                continue
            for l in letters:
                if l not in word:
                    unlocked = False
                    break
            if locked and unlocked:
                for l in excluded:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                # Apply the yellow letter position filtering
                valid_word = True
                for yellow_letter, forbidden_positions in excluded_positions.items():
                    for i, ch in enumerate(word):
                        if ch == yellow_letter and forbidden_positions[i] == yellow_letter:
                            valid_word = False
                            break
                    if not valid_word:
                        break
                
                if valid_word:
                    valids.append(word)
        
        # Sort the valid guesses by entropy before saving
        sorted_valids = sort_words_by_entropy(valids, answers)
        fill_guesses(sorted_valids)
        
        # Filter possible answers (these are the actual possible answers that can be correct)
        for word in answers:
            locked = True
            unlocked = True
            exclude = True
            for key, val in let_dic.items():
                if word[key] != val:
                    locked = False
                    break
            if not locked:
                continue
            for l in letters:
                if l not in word:
                    unlocked = False
                    break
            if locked and unlocked:
                for l in excluded:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                # Apply the yellow letter position filtering
                valid_word = True
                for yellow_letter, forbidden_positions in excluded_positions.items():
                    for i, ch in enumerate(word):
                        if ch == yellow_letter and forbidden_positions[i] == yellow_letter:
                            valid_word = False
                            break
                    if not valid_word:
                        break
                
                if valid_word:
                    guesses.append(word)
        
        # Sort the possible answers by entropy before saving
        sorted_guesses = sort_words_by_entropy(guesses, answers)
        fill_answers(sorted_guesses)

while True:
    main()
