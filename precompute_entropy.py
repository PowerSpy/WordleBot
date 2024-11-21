import math
from wordlebot import load_words, get_feedback
import random

# Example get_feedback function (replace with your actual implementation)
# def get_feedback(guess, answer):
#     """Returns a feedback pattern for a guess against the answer."""
#     feedback = []
#     for i in range(len(guess)):
#         if guess[i] == answer[i]:
#             feedback.append("2")
#         elif guess[i] in answer:
#             feedback.append("1")
#         else:
#             feedback.append("0")
#     return ''.join(feedback)

# Precompute feedback patterns for all guesses
def precompute_feedback_patterns(guesses, answers):
    feedback_dict = {}
    for guess in guesses:
        feedback_dict[guess] = {}
        for answer in answers:
            feedback = get_feedback(guess, answer)
            if feedback not in feedback_dict[guess]:
                feedback_dict[guess][feedback] = []
            feedback_dict[guess][feedback].append(answer)
    return feedback_dict

# Calculate average information (entropy) for a guess
def calculate_average_information(guess, feedback_dict, total_answers):
    total_info = 0
    feedback_patterns = feedback_dict[guess]
    for pattern, subset in feedback_patterns.items():
        subset_size = len(subset)
        probability = subset_size / total_answers
        if probability > 0:  # Avoid log(0)
            total_info += probability * (-math.log(probability, 2))
    try:
        return total_info
    except:
        return None

# Recursive entropy calculation for subsequent guesses
def recursive_entropy_calculation(guesses, answers, feedback_dict):
    if len(answers) <= 1:
        return 0  # No more information to gain
    total_answers = len(answers)
    best_guess = None
    max_entropy = -1
    for guess in guesses:
        feedback_patterns = feedback_dict[guess]
        avg_info = calculate_average_information(guess, feedback_dict, total_answers)
        if avg_info > max_entropy:
            max_entropy = avg_info
            best_guess = guess
    return best_guess, max_entropy

def sort_guesses_by_entropy(guesses, answers, feedback_dict):
    """
    Sorts a list of guesses by their entropy values in descending order.

    Parameters:
        guesses (list): The list of guesses to sort.
        answers (list): The list of possible answers.
        feedback_dict (dict): Precomputed feedback patterns for guesses and answers.

    Returns:
        list: A list of tuples containing guesses and their corresponding entropy, sorted by entropy.
    """
    total_answers = len(answers)
    entropy_list = []

    for guess in guesses:
        avg_info = calculate_average_information(guess, feedback_dict, total_answers)
        entropy_list.append((guess, avg_info))

    # Sort the list by entropy (second element in tuple) in descending order
    sorted_entropy_list = sorted(entropy_list, key=lambda x: x[1], reverse=True)
    return sorted_entropy_list


def solve_wordle(answer, answers, initial_guess = "crane", prints = True):
    guess = initial_guess
    guesses = [guess]
    guess_count = 0
    while True:
        feedback_dict = precompute_feedback_patterns(guesses, answers)
        best_guesses = sort_guesses_by_entropy(guesses, answers, feedback_dict)
        guess = best_guesses[0][0]
        if prints:
            print(guess)
        info = get_feedback(guess, answer)
        guess_count += 1
        if info == "22222":
            if prints:
                print(f"Solved with {guess_count} guesses")
            return guess_count
        guesses = feedback_dict[guess][info]
        answers = feedback_dict[guess][info]
def main(answers, initial_guess = "tares"):
    guess = initial_guess
    print(guess)
    guesses = [guess]
    guess_count = 0
    while True:
        
        feedback_dict = precompute_feedback_patterns(guesses, answers)
        best_guesses = sort_guesses_by_entropy(guesses, answers, feedback_dict)
        guess = best_guesses[0][0]
        print("Try..." + guess)
        while True:
            info = input("Input info: ")
            if info == "exit":
                return
            elif len(info) == 5:
                break
            else:
                print("Error try again!")
            
        guess_count += 1
        if info == "22222":
            print(f"Solved with {guess_count} guesses")
            return
        guesses = feedback_dict[guess][info]
        answers = feedback_dict[guess][info]


if __name__ == "__main__":
    # Example usage
    answers = load_words()[1]
    # guess = "tares"
    # guesses = [guess]
    # feedback_dict = precompute_feedback_patterns(guesses, answers)

    # # Calculate for the first guess
    # best_guesses = sort_guesses_by_entropy(guesses, answers, feedback_dict)
    # print(f"Best first guess: {best_guesses}")

    # info = get_feedback("tares", "tardy")

    # guesses = feedback_dict[best_guesses[0][0]][info]
    # answers = feedback_dict[best_guesses[0][0]][info]
    # print(guesses, answers)

    # feedback_dict = precompute_feedback_patterns(answers, answers)

    # best_guesses = sort_guesses_by_entropy(answers, answers, feedback_dict)

    # print(f"Best first guess: {best_guesses}")
    # print(solve_wordle("alert", answers))
    # print(get_feedback("beset","exist"))
    # while True:
        first_guess = input("Start guess: ")
        if len(first_guess) != 5:
            first_guess = "crane"
        main(answers, first_guess)
    # solve_wordle("watch", answers, "stare")
