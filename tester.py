import random
from wordlebot import load_words, solve_wordle
from tqdm import tqdm
import precompute_entropy

def tester(sample_size=2315, starting_words=None):
    # Load words and answers
    valid_words, answers = load_words()
    len(answers)

    # Default starting words if none provided
    if starting_words is None:
        starting_words = ["crane"]

    # Select a random sample of answers
    test_answers = random.sample(answers, sample_size)
    print(len(test_answers))

    # Open the file for appending results
    with open("comparison_results.txt", "w") as file:
        file.write("Starting_word, Answer : WordleBot, Precompute Entropy\n")

    # Initialize tqdm progress bar
    with tqdm(total=sample_size * len(starting_words), desc="Testing Wordle Solver", unit="game") as pbar:
        for starting_word in starting_words:
            print(f"\nTesting with starting word: {starting_word}")
            
            # Initialize per-word statistics
            wordlebot_total_guesses = 0
            wordlebot_max = 0
            wordlebot_total = 0

            precompute_total_guesses = 0
            precompute_max = 0
            precompute_total = 0

            results = []

            for answer in test_answers:
                print("Answer, Starting:", answer, starting_word)
                # Solve using wordlebot.solve_wordle
                # wordlebot_guesses = solve_wordle(answer, test_answers, starting_word, prints = False)
                wordlebot_guesses = 10
                wordlebot_total_guesses += wordlebot_guesses
                wordlebot_max = max(wordlebot_guesses, wordlebot_max)
                wordlebot_total += 1

                # Solve using precompute_entropy.solve_wordle
                precompute_guesses = precompute_entropy.solve_wordle(answer, test_answers, starting_word, prints = False)
                precompute_total_guesses += precompute_guesses
                precompute_max = max(precompute_guesses, precompute_max)
                precompute_total += 1

                # Store the results
                results.append((starting_word, answer, wordlebot_guesses, precompute_guesses))

                # Update progress bar
                pbar.update(1)

            # Calculate per-word averages and save results
            wordlebot_avg = wordlebot_total_guesses / wordlebot_total if wordlebot_total else 0
            precompute_avg = precompute_total_guesses / precompute_total if precompute_total else 0

            with open("comparison_results.txt", "a") as file:
                file.write(f"\nResults for Starting Word: {starting_word}\n")
                for starting_word, answer, wordlebot_guesses, precompute_guesses in results:
                    file.write(f"{starting_word}, {answer} : {wordlebot_guesses}, {precompute_guesses}\n")
                file.write(f"WordleBot -> Average Guesses: {wordlebot_avg:.2f}, Max Guesses: {wordlebot_max}\n")
                file.write(f"PrecomputeEntropy -> Average Guesses: {precompute_avg:.2f}, Max Guesses: {precompute_max}\n")

            print(f"\nResults for {starting_word} saved.")

    print("\nComparison Complete. Results saved to 'comparison_results.txt'.")


if __name__ == "__main__":
    
    tester(2315, ["slant", "trace", "carte", "salet", "crate"])
