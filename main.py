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
def main():
    while True:
        letters = []
        let_dic = {}
        valids = []
        guesses = []
        user = input("Enter Locked Values (green): ")
        user_guess = input("Enter string of letters (yellow): ")
        excluded = input("Enter string of excluded words (gray): ")
        if user == "exit":
            break
        elif user == "_____" and user_guess == None and excluded == None:
            fill_answers(answers)
            fill_guesses(valid_words)
        if len(user) == 5:
            for i, l in enumerate(user):
                if l != "_":
                    let_dic[i] = l
        if user_guess != None:
            for l in user_guess:
                letters.append(l)
        print(letters, let_dic)
        for word in valid_words:
            locked = True
            unlocked = True
            exclude = True
            for key, val in let_dic.items():
                if word[key] != val:
                    locked = False
                    break
            if locked == False:
                continue
            else:
                for l in letters:
                    if l not in word:
                        unlocked = False
                        break
            if locked and unlocked:
                for l in excluded:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                valids.append(word)
        fill_guesses(valids)
        for word in answers:
            locked = True
            unlocked = True
            exclude = True
            for key, val in let_dic.items():
                if word[key] != val:
                    locked = False
                    break
            if locked == False:
                continue
            else:
                for l in letters:
                    if l not in word:
                        unlocked = False
                        break
            if locked and unlocked:
                for l in excluded:
                    if l in word:
                        exclude = False
            if locked and unlocked and exclude:
                guesses.append(word)
        fill_answers(guesses)
                        


main()