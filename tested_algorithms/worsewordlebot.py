import json
import math
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


from tqdm import tqdm

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



def process_guess(guess, answers, feedback_cache):
    """
    This function processes a single starting word against all answers
    and updates the feedback_cache dictionary.
    """
    # Initialize the inner progress bar for each guess
    with tqdm(total=len(answers), desc=f"Processing {guess}", leave=False) as inner_bar:
        for answer in answers:
            feedback = get_feedback(guess, answer)  # Calculate feedback
            # Convert tuple keys to string (e.g., ("crane", "yellow") -> "crane-yellow")
            key = f"{guess}-{feedback}"
            excluded_letters = ""
            locked_positions = {}
            locked_letters = "-----"
            yellow_excluded_positions = {}  # Store the positions where yellow letters cannot be
            guessed_word = guess
            guesses = 0
            sorted_valid_answers = answers

            yellow_letters_list = []
            valid_guesses = []
            valid_answers = []

            yellow_input = ""
            green_input = ""

            # Process feedback info
            info = get_feedback(guessed_word, answer)
            guesses += 1
            if guessed_word == answer:
                return guesses
            try:
                sorted_valid_answers.remove(guessed_word)
            except:
                pass
            for ind, (c, i) in enumerate(zip(guessed_word, info)):
                if i == "0":
                    excluded_letters += c
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
                elif i == "2":
                    green_input += c

            # Update locked_letters and excluded_letters
            locked_letters = "".join(c1 if c1.isalpha() else c2 for c1, c2 in zip(locked_letters, green_input))
            excluded_letters = "".join(
                letter
                for letter in set(excluded_letters)
                if letter not in locked_letters.replace("-", "") and letter not in yellow_excluded_positions
            )

            # Set locked positions
            if len(locked_letters) == 5:
                for i, l in enumerate(locked_letters):
                    if l != "-":
                        locked_positions[i] = l

            # Filter possible valid answers based on yellow and excluded letters
            valid_answers = []
            yellow_letters_list = list(yellow_input)
            for word in answers:
                if all(word[k] == v for k, v in locked_positions.items()) and all(l in word for l in yellow_letters_list):
                    if all(e not in word for e in excluded_letters):
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
            feedback_cache[key] = guessed_word  # Cache feedback for this guess-answer pair

            inner_bar.update(1)  # Update the inner progress bar for each answer

    return feedback_cache

def generate_feedback_cache(starting_words, answers):
    feedback_cache = {}

    # Initialize the outer tqdm progress bar with time estimate
    with tqdm(total=len(starting_words), desc="Processing guesses and answers") as outer_bar:
        with ThreadPoolExecutor() as executor:
            futures = []
            for guess in starting_words:
                futures.append(executor.submit(process_guess, guess, answers, feedback_cache))
            
            for future in futures:
                future.result()  # Wait for all threads to finish
                outer_bar.update(1)  # Update the outer progress bar with each completed task

    # Save the cache to a file after processing
    with open("feedback_cache.json", "w") as file:
        json.dump(feedback_cache, file)




def solve_wordle(answer, answers, initial_guess = "crane", cache_file="feedback_cache.json"):
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}
    excluded_letters = ""
    locked_positions = {}
    locked_letters = "-----"
    yellow_excluded_positions = {}  # Store the positions where yellow letters cannot be
    guessed_word = initial_guess
    guesses = 0
    sorted_valid_answers = answers
    while True:
        yellow_letters_list = []
        # valid_guesses = []
        valid_answers = []

        yellow_input = ""
        green_input = ""

        # (ex: 02001, 0 = gray, 1 = yellow, 2 = green)
        info = get_feedback(guessed_word, answer)
        guesses += 1
        print(guessed_word)
        # print(info)
        if guessed_word == answer:
            return guesses
        try:
            sorted_valid_answers.remove(guessed_word)
        except:
            pass
        cache_key = f"{guessed_word}-{info}"
        print(sorted_valid_answers)
        if cache_key in cache:
            guessed_word = cache[cache_key]
            continue
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
        print(sorted_valid_answers)
        sorted_valid_answers = sort_words_by_entropy(valid_answers, answers)
        guessed_word = sorted_valid_answers[0]



if __name__ == "__main__":
    valid_words, answers = load_words()
    # print(solve_wordle("tramp", answers, "crane"))
    while True:
        main()
    