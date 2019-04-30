#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               00598949                                                    #
#                               mkhan8@unh.newhaven.edu                                     #
#############################################################################################

# Importing system module
import sys

# Function Definitions


# Function to read text from file
def get_text(filename=""):

    if not filename:
        filename = input("Please enter name of data file(s): ")

    # Got encoding idea from:
    # http://stackoverflow.com/questions/10971033/backporting-python-3-openencoding-utf-8-to-python-2
    file = open(filename, "r", encoding="utf8")
    # Read the whole text at once
    text = file.read()
    # Close the file
    file.close()

    return text


# Function to filter letters from text and return it
def clean_text(read_text):

    for letter in read_text:
        letter = letter.lower()
        # Return letter based on their ASCII values
        if 97 <= ord(letter) <= 122:
            yield letter


# Function to store Letter Frequency Statistics imported from wikipedia
def wiki_stats():

    temp_list = []
    wiki_position = {}

    # Imported letter frequency from https://en.wikipedia.org/wiki/Letter_frequency
    wiki_frequency = {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228,
                      'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025,
                      'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987,
                      's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
                      'y': 1.974, 'z': 0.074}

    # Letter frequency dictionary
    for keys, values in wiki_frequency.items():
        temp_list.append((values, keys))
        temp_list.sort(reverse=True)

    # List of index values for letters
    for index in range(len(temp_list)):
        wiki_position[temp_list[index][1]] = index

    return wiki_frequency, temp_list, wiki_position


# Function to get a dictionary of letters A-Z
def get_dictionary(read_text):

    letters = {}

    for letter in clean_text(read_text):
        if letter in letters:
            temp = letters.get(letter)
#            print (temp)
            # If letter is already present in dictionary increment count
            letters[letter] = temp + 1
        else:
            # If letter is not present in dictionary add it as key with value 1
            letters[letter] = 1

    return letters


# Function to calculate the letter frequency
def get_percentage(letter_dictionary):

    total_letters = 0
    for letter in letter_dictionary:
        total_letters += letter_dictionary.get(letter)

#    print(total_letters)

    for letter in letter_dictionary:
        temp = letter_dictionary.get(letter)
        # To calculate the letter frequency by dividing letter count by total letters
        letter_dictionary[letter] = round((temp/total_letters)*100, 3)

    return letter_dictionary


# Function to calculate the Letter Frequency Deviation for a file
def print_difference(letter_percentage, wiki_frequency, filename):

    total_error = 0

    print("__________Frequency Comparison___________\n\n", "Book Table       -        Wiki Table\n")

    for letter in letter_percentage:
        if letter in letter_percentage:
            print(" -> ", letter.upper(), " : %.3f" % letter_percentage[letter], "  |  ", letter.upper(),
                  " : %.3f" % wiki_frequency[letter])

    for letter in letter_percentage:
        if letter in letter_percentage:
            # print(letter_percentage[letter] - wiki_frequency[letter])
            total_error += abs(letter_percentage[letter] - wiki_frequency[letter])

    print("\nThe total Frequency Deviation Error for [", filename, "] is: ", round(total_error, 3))
    return round(total_error, 3)


# Function to rank books by Frequency Deviation and Changes in Letter Position
def rank_books(error, filename, temp_list, switch):

    # To sort a list in ascending order
    if switch == 1:
        temp_list.append((error, filename))
        temp_list.sort(reverse=False)
    # To sort a list in descending order
    elif switch == 2:
        temp_list.append((error, filename))
        temp_list.sort(reverse=True)
    else:
        print("\n\n#################### RANK #########################")
        if switch == 3:
            print("\n Ranking by Deviation (Lesser to Greater): ")
        elif switch == 4:
            print("\n Ranking by Changes in Letter Position (Higher to Lower): ")

        for x in range(0, len(temp_list)):
            try:
                print("\n", x+1, ". ",  temp_list[x][1], " : ", temp_list[x][0], end="")
            except IndexError:
                print("          ", end="")

    return temp_list


# Function to sort and compare the letter frequency; Calculate the changes letter position
def sort_compare(letter_percentage, wiki_sort, wiki_position, filename):

    temp_list = []
    letter_position = {}
    temp_pos = {}
    total_position_error = 0

    for keys, values in letter_percentage.items():
        temp_list.append((values, keys))
        temp_list.sort(reverse=True)

    print("\n_____________Sorted table_____________\n\n", "Book Frequency  -  Wiki Frequency\n")

    for x in range(0, len(wiki_sort)):
        try:
            print(" -> ", (temp_list[x][1]).upper(), " :  %.3f" % temp_list[x][0], " - ", (wiki_sort[x][1]).upper(),
                  " :  %.3f" % wiki_sort[x][0], end="\n")
        except IndexError:
            print(" -> ", "?  :  %.3f" % 0.000, " - ", (wiki_sort[x][1]).upper(),
                  " :  %.3f" % wiki_sort[x][0], end="\n")

#    print(wiki_position)

    for index in range(len(temp_list)):
        temp_pos[temp_list[index][1]] = index

#    print(temp_pos)

    # Calculate the position error
    for letter in letter_percentage:
        temp = temp_pos.get(letter)
        temp2 = wiki_position.get(letter)
        letter_position[letter] = temp - temp2
        total_position_error += abs(temp - temp2)

#    print(letter_position)
    print("\n___________Letter Positions___________")

    for letter in letter_percentage:
        print("\n -> Letter", letter.upper(), " is at ", letter_position[letter], " position.", end="")

    print("\n\n The total letter position error for [", filename, "] is: ", total_position_error, end="\n")

    return temp_list, letter_position, total_position_error


# Function to group the letters using the letter table
def letter_grouping(table):

    letter_list = []

    for letter in table:
        letter_list.append(letter[1])

    letter_tuple = tuple(letter_list)

    # Group containing letters from 1:6
    one_six = letter_tuple[0:6]
    # Group containing letters from 7:12
    seven_twelve = letter_tuple[6:12]
    # Group containing letters from 13:19
    thirteen_nineteen = letter_tuple[12:19]
    # Group containing letters from 19:26
    twenty_twenty_six = letter_tuple[19:26]

#    print("\n\nGroup 1: ", one_six, end="\n")
#    print("Group 2: ", seven_twelve, end="\n")
#    print("Group 3: ", thirteen_nineteen, end="\n")
#    print("Group 4: ", twenty_twenty_six, end="\n")

    return one_six, seven_twelve, thirteen_nineteen, twenty_twenty_six


# Function to calculate the occurrence of letters in a group; Set Intersection
def letter_prominence(one, two, three, four):

    omnipresent_one = set(one[0])
    omnipresent_two = set(two[0])
    omnipresent_three = set(three[0])
    omnipresent_four = set(four[0])

    for group in range(1, len(one)):
        omnipresent_one = omnipresent_one.intersection(one[group])

    for group in range(1, len(two)):
        omnipresent_two = omnipresent_two.intersection(two[group])

    for group in range(1, len(three)):
        omnipresent_three = omnipresent_three.intersection(three[group])

    for group in range(1, len(four)):
        omnipresent_four = omnipresent_four.intersection(four[group])

    print("\n\n___________Letter Prominence___________\n")
    print(" -> Letters in Group 1: ", omnipresent_one, end="\n")
    print(" -> Letters in Group 2: ", omnipresent_two, end="\n")
    print(" -> Letters in Group 3: ", omnipresent_three, end="\n")
    print(" -> Letters in Group 4: ", omnipresent_four, end="\n")

    return omnipresent_one, omnipresent_two, omnipresent_three, omnipresent_four


# Function to calculate the consistency of occurrence of letters across all books
def letter_consistency(list1, list2, list3, list4):

    first_set = set(list1[0]) | set(list2[0])
    second_set = set(list3[0]) | set(list2[0])

    for book in range(len(list1)):
        first_set = first_set & (set(list1[book]) | set(list2[book]))

    for book in range(len(list1)):
        second_set = second_set & (set(list3[book]) | set(list4[book]))

    print("\n______Letter Occurrence Consistency______\n")
    print("Letters in the First Half: ", first_set, end="\n")
    print("Letters in the Second Half: ", second_set, end="\n")

#############################################################################################

# Main Program

# List to store the deviation error by the name of the file
rank_deviation = []
# List to store the position error by the name of the file
rank_position = []

# Lists to store the groupings of letters in a book by group
group_one = []
group_two = []
group_three = []
group_four = []

# Command line argument to take names of files as input
files = sys.argv[1:]

# Loop to process each file
for file in files:
    print("\n", "##########################", file, "############################", "\n")

    # Read Text
    text = get_text(file)
#    print(text)

    # Get letter dictionary
    letter_dict = get_dictionary(text)
#    print(letter_dict)

    # Get the letter frequency
    letter_dict_percentage = get_percentage(letter_dict)
#    print(letter_dict_percentage)

    # Get the wikipedia statistics
    wiki_freq, wiki_sorted, wiki_pos = wiki_stats()
#    print(wiki_freq)

    # Get the deviation error
    deviation_error = print_difference(letter_dict_percentage, wiki_freq, file)
#    print("\nError: ", deviation_error, "\n")

    # Gets a sorted list of books by closest to farthest deviation from error
    rank_deviation = rank_books(deviation_error, file, rank_deviation, 1)
#    print(rank_deviation)

    # Sort, Compare and Find Letter Positions
    sorted_table, position, position_error = sort_compare(letter_dict_percentage, wiki_sorted, wiki_pos, file)
#    print(sorted_table)

    # Gets a sorted list of books based on the position error
    rank_position = rank_books(position_error, file, rank_position, 1)
#    print("\n", rank_position)

    # Get the list of grouped letters
    group_1, group_2, group_3, group_4 = letter_grouping(sorted_table)
    group_one.append(group_1)
    group_two.append(group_2)
    group_three.append(group_3)
    group_four.append(group_4)

# Print the rank by deviation
rank_deviation = rank_books(0, " ", rank_deviation, 3)

# Print the rank by position
rank_position = rank_books(0, " ", rank_position, 4)

# Get the set set intersection of the groups
first, second, third, fourth = letter_prominence(group_one, group_two, group_three, group_four)

# Get the set union of the first 2 and last 2 groups
letter_consistency(group_one, group_two, group_three, group_four)

print("\n############################ Program Completed ############################")

#############################################################################################
#                                       End of Program                                      #
#############################################################################################
