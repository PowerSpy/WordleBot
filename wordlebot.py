import math
from collections import defaultdict

def load_words(): 
    valid_words = []

    with open("valid-wordle-words.txt", "r") as file:
        for line in file:
            valid_words.append(line.strip())
    answers = []
    with open("answers.txt", "r") as file:
        for line in file:
            answers.append(line.strip())
    return valid_words, answers

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
            feedback.append('2')  # Green
            answer_copy[i] = None  # Remove from answer to avoid double-counting
        else:
            feedback.append(None)
    
    # Second pass: Check for yellows and grays
    for i, g in enumerate(guess):
        if feedback[i] is None:
            if g in answer_copy:
                feedback[i] = '1'  # Yellow
                answer_copy[answer_copy.index(g)] = None  # Remove the first occurrence
            else:
                feedback[i] = '0'  # Gray
    
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
    excluded_letters = ""
    locked_positions = {}
    locked_letters = "-----"
    yellow_excluded_positions = {}  # Store the positions where yellow letters cannot be
    sorted_valid_answers = answers
    while True:
        yellow_letters_list = []
        valid_guesses = []
        valid_answers = []

        yellow_input = ""
        green_input = ""

        while True:
            guessed_word = input("What word did you try: ")
            if len(guessed_word) == 5 or len(guessed_word) == 0:
                break
            else:
                if guessed_word == "exit":
                    return
                print("Bad input try again!")

        # (ex: 02001, 0 = gray, 1 = yellow, 2 = green)
        while True:
            info = input("Provide information for each letter: ")
            if len(info) == 5 or len(info) == 0:
                break
            else:
                if info == "exit":
                    return
                print("Bad input try again!")
        if info != "22222":
            try:
                sorted_valid_answers.remove(guessed_word)
            except:
                pass
        elif info == "":
            info = "00000"
        for ind, (c, i) in enumerate(zip(guessed_word, info)):
            if i == "0":
                excluded_letters+=c
                green_input += "-"
            elif i == "1":
                yellow_input += c
                green_input += "-"
                if c in yellow_excluded_positions:
                    # Convert the string to a list, modify it, and convert it back to a string
                    yellow_list = list(yellow_excluded_positions[c])
                    yellow_list[ind] = c
                    yellow_excluded_positions[c] = "".join(yellow_list)
                else:
                    yellow_excluded_positions[c] = "-----"
                    yellow_list = list(yellow_excluded_positions[c])
                    yellow_list[ind] = c
                    yellow_excluded_positions[c] = "".join(yellow_list)
            elif i  == "2":
                green_input += c
        locked_letters = "".join(c1 if c1.isalpha() else c2 for c1, c2 in zip(locked_letters, green_input))
        excluded_letters = "".join(
                letter
                for letter in set(excluded_letters)
                if letter not in locked_letters.replace("-", "") and letter not in yellow_excluded_positions
            )
        
        print(locked_letters, excluded_letters, yellow_excluded_positions)
        
        if locked_letters == "-----" and yellow_input == None and excluded_letters == None:
            # Write the full list of answers and guesses
            fill_answers(answers)
            fill_guesses(valid_words)
        
        if len(locked_letters) == 5:
            for i, l in enumerate(locked_letters):
                if l != "-":
                    locked_positions[i] = l
        if yellow_input != None:
            for l in yellow_input:
                yellow_letters_list.append(l)
        
        # Filter valid words (these are guesses that could be valid guesses for the next guess)
        for word in valid_words:
            locked = True
            unlocked = True
            exclude = True
            for key, val in locked_positions.items():
                if word[key] != val:
                    locked = False
                    break
            if not locked:
                continue
            for l in yellow_letters_list:
                if l not in word:
                    unlocked = False
                    break
            if locked and unlocked:
                for l in excluded_letters:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                # Apply the yellow letter position filtering
                valid_word = True
                for yellow_letter, forbidden_positions in yellow_excluded_positions.items():
                    for i, ch in enumerate(word):
                        if ch == yellow_letter and forbidden_positions[i] == yellow_letter:
                            valid_word = False
                            break
                    if not valid_word:
                        break
                
                if valid_word:
                    valid_guesses.append(word)
        
        # Sort the valid guesses by entropy before saving
        sorted_valid_guesses = sort_words_by_entropy(valid_guesses, answers)
        fill_guesses(sorted_valid_guesses)
        
        # Filter possible answers (these are the actual possible answers that can be correct)
        for word in sorted_valid_answers:
            locked = True
            unlocked = True
            exclude = True
            for key, val in locked_positions.items():
                if word[key] != val:
                    locked = False
                    break
            if not locked:
                continue
            for l in yellow_letters_list:
                if l not in word:
                    unlocked = False
                    break
            if locked and unlocked:
                for l in excluded_letters:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                # Apply the yellow letter position filtering
                valid_word = True
                for yellow_letter, forbidden_positions in yellow_excluded_positions.items():
                    for i, ch in enumerate(word):
                        if ch == yellow_letter and forbidden_positions[i] == yellow_letter:
                            valid_word = False
                            break
                    if not valid_word:
                        break
                
                if valid_word:
                    valid_answers.append(word)
        
        # Sort the possible answers by entropy before saving
        sorted_valid_answers = sort_words_by_entropy(valid_answers, answers)
        fill_answers(sorted_valid_answers)

def solve_wordle(answer, answers, initial_guess = "crane"):
    excluded_letters = ""
    locked_positions = {}
    locked_letters = "-----"
    yellow_excluded_positions = {}  # Store the positions where yellow letters cannot be
    guessed_word = initial_guess
    guesses = 0
    sorted_valid_answers = answers
    while True:
        yellow_letters_list = []
        valid_guesses = []
        valid_answers = []

        yellow_input = ""
        green_input = ""

        # (ex: 02001, 0 = gray, 1 = yellow, 2 = green)
        info = get_feedback(guessed_word, answer)
        guesses += 1
        print(guessed_word)
        print(info)
        if guessed_word == answer:
            return guesses
        try:
            sorted_valid_answers.remove(guessed_word)
        except:
            pass
        for ind, (c, i) in enumerate(zip(guessed_word, info)):
            if i == "0":
                excluded_letters+=c
                green_input += "-"
            elif i == "1":
                yellow_input += c
                green_input += "-"
                if c in yellow_excluded_positions:
                    # Convert the string to a list, modify it, and convert it back to a string
                    yellow_list = list(yellow_excluded_positions[c])
                    yellow_list[ind] = c
                    yellow_excluded_positions[c] = "".join(yellow_list)
                else:
                    yellow_excluded_positions[c] = "-----"
                    yellow_list = list(yellow_excluded_positions[c])
                    yellow_list[ind] = c
                    yellow_excluded_positions[c] = "".join(yellow_list)
            elif i  == "2":
                green_input += c
        locked_letters = "".join(c1 if c1.isalpha() else c2 for c1, c2 in zip(locked_letters, green_input))
        excluded_letters = "".join(
                letter
                for letter in set(excluded_letters)
                if letter not in locked_letters.replace("-", "") and letter not in yellow_excluded_positions
            )
        
        
        if len(locked_letters) == 5:
            for i, l in enumerate(locked_letters):
                if l != "-":
                    locked_positions[i] = l
        if yellow_input:
            yellow_letters_list = list(yellow_input)
        for word in sorted_valid_answers:
            locked = True
            unlocked = True
            exclude = True
            for key, val in locked_positions.items():
                if word[key] != val:
                    locked = False
                    break
            if not locked:
                continue
            for l in yellow_letters_list:
                if l not in word:
                    unlocked = False
                    break
            if locked and unlocked:
                for l in excluded_letters:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                # Apply the yellow letter position filtering
                valid_word = True
                for yellow_letter, forbidden_positions in yellow_excluded_positions.items():
                    for i, ch in enumerate(word):
                        if ch == yellow_letter and forbidden_positions[i] == yellow_letter:
                            valid_word = False
                            break
                    if not valid_word:
                        break
                
                if valid_word:
                    valid_answers.append(word)
        
        # Sort the possible answers by entropy before saving
        sorted_valid_answers = sort_words_by_entropy(valid_answers, answers)
        guessed_word = sorted_valid_answers[0]

# def solve_wordle(answer, answers):
#     """
#     Solve a Wordle puzzle given the answer.
#     :param answer: The actual answer to guess.
#     :param valid_words: List of all valid guesses.
#     :param answers: List of all possible answers.
#     :return: Number of guesses it took to solve the puzzle.
#     """
#     excluded_letters = ""
#     locked_positions = {}
#     locked_letters = "-----"
#     yellow_excluded_positions = {}
#     yellow_letters_list = []

#     guesses = 0
#     guess = "crane"
#     while True:
#         yellow_input = ""
#         green_input = ""
#         valid_answers = []
        
#         # Get feedback for the current guess
#         info = get_feedback(guess, answer)
#         guesses += 1
#         print(guess, info)
        
#         # Break the loop if the guess is correct
#         if guess == answer:
#             return guesses
        
#         # Process the feedback and update variables
#         for ind, (c, i) in enumerate(zip(guess, info)):
#             if i == "0":  # Gray (excluded)
#                 excluded_letters += c
#                 green_input += "-"
#             elif i == "1":  # Yellow (wrong position)
#                 yellow_input += c
#                 green_input += "-"
#                 if c in yellow_excluded_positions:
#                     yellow_list = list(yellow_excluded_positions[c])
#                     yellow_list[ind] = c
#                     yellow_excluded_positions[c] = "".join(yellow_list)
#                 else:
#                     yellow_excluded_positions[c] = "-----"
#                     yellow_list = list(yellow_excluded_positions[c])
#                     yellow_list[ind] = c
#                     yellow_excluded_positions[c] = "".join(yellow_list)
#             elif i == "2":  # Green (correct)
#                 green_input += c

#         # Update excluded letters based on locked and yellow positions
#         excluded_letters = "".join(
#             letter
#             for letter in set(excluded_letters)
#             if letter not in locked_letters.replace("-", "") and letter not in yellow_excluded_positions
#         )
        
#         locked_letters = "".join(c1 if c1.isalpha() else c2 for c1, c2 in zip(locked_letters, green_input))

#         if len(locked_letters) == 5:
#             for i, l in enumerate(locked_letters):
#                 if l != "-":
#                     locked_positions[i] = l
#         if yellow_input != None:
#             for l in yellow_input:
#                 yellow_letters_list.append(l)

#         # Filter valid answers
#         for word in answers:
#             locked = True
#             unlocked = True
#             exclude = True
#             for key, val in locked_positions.items():
#                 if word[key] != val:
#                     locked = False
#                     break
#             if not locked:
#                 continue
#             for l in yellow_letters_list:
#                 if l not in word:
#                     unlocked = False
#                     break
#             if locked and unlocked:
#                 for l in excluded_letters:
#                     if l in word:
#                         exclude = False
#             if locked and unlocked and exclude:
#                 valid_answers.append(word)
        
#         # Sort the valid answers by entropy
#         valid_answers = sort_words_by_entropy(valid_answers, answers)
#         previous_guess = guess
#         guess = valid_answers[0]  # Make the next guess based on entropy
#         if guess == previous_guess:
#             print("Stuck on the same guess, checking logic!")
#             break  # Or handle the issue to break the loop


if __name__ == "__main__":
    valid_words, answers = load_words()
    print(solve_wordle("daddy", answers))
    # while True:
    #     main()
    