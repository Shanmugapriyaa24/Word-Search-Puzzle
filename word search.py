import csv
import os
import random

from flask import Flask, render_template, request

app = Flask(__name__)

def create_word_search(words, size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    for word in words:
        place_word(word, grid)
    fill_grid(grid)
    return grid

def place_word(word, grid):
    size = len(grid)
    directions = [
        (1, 0),  # right
        (0, 1),  # down
        (-1, 0), # left
        (0, -1), # up
        (1, 1),  # down-right
        (-1, 1), # down-left
        (-1, -1),# up-left
        (1, -1)  # up-right
    ]
    while True:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        dx, dy = random.choice(directions)
        end_x = x + (len(word) - 1) * dx
        end_y = y + (len(word) - 1) * dy
        if 0 <= end_x < size and 0 <= end_y < size:
            fits = True
            for i in range(len(word)):
                char = grid[x + i * dx][y + i * dy]
                if char != ' ' and char != word[i]:
                    fits = False
                    break
            if fits:
                for i in range(len(word)):
                    grid[x + i * dx][y + i * dy] = word[i]
                break

def fill_grid(grid):
    size = len(grid)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(letters)

def lowercase_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = grid[i][j].lower()

def read_words_from_csv(file_path):
    words = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            words.append(row[0].strip()) # Ensure no trailing spaces
    return words

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/puzzle', methods=['POST'])
def generate_puzzle():
    grid_size = int(request.form['grid_size'])
    num_words = int(request.form['num_words'])

    # Set the file path to your CSV file in the static directory
    static_folder_path = os.path.join(app.static_folder, '4000-most-common-english-words-csv.csv')
    words_to_find = read_words_from_csv(static_folder_path)

    filtered_words = [word for word in words_to_find if len(word) <= grid_size]
    selected_words = random.sample(filtered_words, min(num_words, len(filtered_words)))

    grid = create_word_search(selected_words, grid_size)
    lowercase_grid(grid)

    lowercase_selected_words = [word.lower() for word in selected_words]

    return render_template('puzzle.html', grid=grid, words=lowercase_selected_words)

if __name__ == '__main__':
    app.run(debug=True)
