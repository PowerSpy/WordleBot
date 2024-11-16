# wordle_tester.py

import random
from wordlebot import load_words, solve_wordle
from tqdm import tqdm

def tester(sample_size=2315):
    # Load words and answers
    valid_words, answers = load_words()

    # Select a random sample of answers
    test_answers = random.sample(answers, sample_size)

    results = []
    total_guesses = 0
    max_guesses = 0
    min_guesses = float('inf')
    print(test_answers)

    # Initialize tqdm progress bar
    with tqdm(total=sample_size, desc="Testing Wordle Solver", unit="game") as pbar:
        for answer in test_answers:
            print(answer, "\n")
            guesses = solve_wordle(answer, answers)
            results.append((answer, guesses))
            total_guesses += guesses
            max_guesses = max(max_guesses, guesses)
            min_guesses = min(min_guesses, guesses)
            average_guesses = total_guesses / len(results)

            # Update progress bar with stats
            pbar.set_postfix({
                "avg_guesses": f"{average_guesses:.2f}",
                "max_guesses": max_guesses,
                "min_guesses": min_guesses
            })
            pbar.update(1)

    # Final statistics
    print("\nTesting Complete.")
    print(f"Average Guesses: {average_guesses:.2f}")
    print(f"Maximum Guesses: {max_guesses}")
    print(f"Minimum Guesses: {min_guesses}")

    # Save results to a file
    with open("test_results.txt", "w") as file:
        for answer, guesses in results:
            file.write(f"{answer}: {guesses} guesses\n")
        file.write(f"\nAverage Guesses: {average_guesses:.2f}\n")
        file.write(f"Maximum Guesses: {max_guesses}\n")
        file.write(f"Minimum Guesses: {min_guesses}\n")

if __name__ == "__main__":
    tester()
