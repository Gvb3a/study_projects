import os  # To clean cmd
from faker import Faker  # To generate the word

hangman = (''' ------
 |    |
 |
 |
 |
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |
 |
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |    |
 |
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |   /|
 |
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |   /|\\
 |
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |   /|\\
 |   /
 |
 |
----------''',
           ''' ------
 |    |
 |    O
 |   /|\\
 |   / \\
 |
 |
----------'''
           )

loss = win = streak = 0


def generate_word():
    word = Faker().word()
    while len(word) < 7:
        word = Faker().word()
    return word


def main():

    print('Welcome to Hangman!')

    word = generate_word()  # Call function generate_word

    max_wrong_guesses = len(hangman)
    wrong_guesses = 0
    dashes = '-' * len(word)
    used = []
    k = 0
    guess = 'None123'

    while wrong_guesses < max_wrong_guesses:

        if guess in word:
            print(f'The letter \'{guess}\' is in the word')
            new = ''
            for i in range(len(word)):
                if guess == word[i]:
                    new += guess
                else:
                    new += dashes[i]
            dashes = new
        elif k != 0:
            print('Wrong guess. The letters \'{}\' are not in the word'.format(guess))
            wrong_guesses += 1

        if dashes == word or wrong_guesses == max_wrong_guesses:
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        print(hangman[wrong_guesses])
        print('Word:', dashes)
        print('Number of errors {} out of {}'.format(wrong_guesses, max_wrong_guesses))
        print('Used letters:', used)
        guess = input('Enter a letter: ')

        while guess in used:
            print('you\'ve already guessed', guess)
            guess = input('Enter a letter: ')
        while len(guess) > 1:
            print('It\'s not a letter.')
            guess = input('Enter a letter: ')

        used.append(guess)
        k += 1
        os.system('cls' if os.name == 'nt' else 'clear')

    if wrong_guesses == max_wrong_guesses:
        print(hangman[max_wrong_guesses - 1])
        print('Word:', word)
        print('You\'re hanged')
        return 0
    else:
        print(hangman[wrong_guesses])
        print('You guessed the word!')
        print('The target word is \'{}\'.'.format(word))
        return 1


while True:
    win_or_loss = main()
    if win_or_loss == 1:
        win += 1
        streak += 1
    else:
        loss += 1
        streak = 0
    win_rate = (win / (win + loss)) * 100 if (win + loss) != 0 else 100
    print(f'Number of wins: {win}. Number of losses: {loss}. Streak: {streak}. Win rate: {win_rate:.2f}%')
    choose = input('Do you want to play again? ').lower()
    if choose not in ['yes', 'y', '1', 'true', 'Yes']:
        break
