def chess():
    # https://acmp.ru/index.asp?main=task&id_task=6 I don't know why, but it took me a long time.
    print("Checking the correctness of the knight's move. Example: C7-D5")

    try:
        start_pos, final_pos = input().split('-')
        start_letter, start_num = start_pos[0], int(start_pos[1])
        final_letter, final_num = final_pos[0], int(final_pos[1])
        letter_dic = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

        let = abs(letter_dic[start_letter] - letter_dic[final_letter])
        num = abs(start_num - final_num)

        if not (1 <= start_num <= 8 and 1 <= final_num <= 8):
            print('ERROR')
        elif (let == 2 and num == 1) or (let == 1 and num == 2):
            print('YES')
        else:
            print('NO')

    except:
        print('ERROR')




def len_of_segment():
    # https://acmp.ru/index.asp?main=task&id_task=529 It's a fun maths problem
    print('A segment is given the coordinates of its endpoints. It is required to calculate the length of this segment.')

    x1, y1, x2, y2 = map(int, input().split())
    a = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    print(int(a) if int(a) == a else round(a, 5))




def air_conditioner():
    # https://acmp.ru/index.asp?main=task&id_task=854 I just like my solution
    print('You enter the room temperature you want. Then one of the four operating modes (freeze, heat, auto, fan)')

    room, cond = map(int, input().split())
    d = {
        'freeze': min(room, cond),
        'heat': max(room, cond),
        'auto': cond,
        'fan': room
    }
    print(d[input()])




def main():
    print('Here are my solutions from acmp.ru. Reference to functions by index or name. '
          'In case of incorrect input, the program closes')

    function_dictionary = {
        'chess': chess,
        'length of segment': len_of_segment,
        'air conditioner': air_conditioner
    }

    for index, function_name in enumerate(function_dictionary):
        print(f"{function_name}({index + 1}); ", end='')
    choice_main = input('\n')

    while True:  # If you want the programme not to close after an incorrect input, remove break everywhere.
        if choice_main.isdigit():  # If references to the index
            if 0 < int(choice_main) <= len(function_dictionary):  # Checking index correctness
                func_name = list(function_dictionary.keys())[int(choice_main) - 1]
                func_to_call = function_dictionary.get(func_name)
                if func_to_call:
                    func_to_call()
                else:
                    print('incorrect input')
                    break
            else:
                print('incorrect input')
                break

        elif choice_main in function_dictionary:
            function_dictionary[choice_main]()

        else:
            break

        choice_main = input()


main()
