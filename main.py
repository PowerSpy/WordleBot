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
        file.write(a)
def fill_guesses(g):
    with open("good_guesses.txt", "w") as file:
        file.write(g)
def main():
    while True:
        letters = []
        let_dic = {}
        user = input("Enter Locked Values (green): ")
        user_guess = input("Enter string of letters (yellow): ")
        if user == "exit":
            break
        elif user == "_____" and user_guess == None:
            fill_answers(answers)
            fill_guesses(valid_words)
        if len(user) == 5:
            for i, l in enumerate(user):
                if l != "_":
                    let_dic[(i+1)] = l
        if user_guess != None:
            for l in user_guess:
                letters.append(l)
        print(letters, let_dic)
main()