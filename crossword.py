import random

# Grid setup
GRID_SIZE = 15
EMPTY = '.'

# Expanded Kiswahili dictionary (uppercase for consistency)
dictionary = {
    "MAMA", "BABA", "MTOTO", "SHULE", "KITI",
    "MEZA", "CHAKULA", "NYUMBA", "SAMAKI", "MBWA",
    "SOKO", "GARI", "NDIZI", "NGUO", "MWALIMU",
    "KITU", "MKATE", "KUNDA", "MSICHANA", "MVULA",
    "MBWA", "NGOMA", "SOMA", "KAZI", "PENDE", "NDOTO",
    "MAJI", "MOTO", "MKONO", "SIMBA", "PEPE", "KUNDA"
}

# Words to place (uppercase)
words = [
    "MAMA", "BABA", "MTOTO", "SHULE", "KITI",
    "MEZA", "CHAKULA", "NYUMBA", "SAMAKI", "MBWA",
    "SOKO", "GARI", "NDIZI", "NGUO", "MWALIMU"
]

DIRECTIONS = {
    'H': (0, 1),   # Horizontal
    'V': (1, 0),   # Vertical
}

def create_grid():
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def print_grid(grid):
    for row in grid:
        print(" ".join(row))

def get_word_in_direction(grid, r, c, dr, dc):
    """Get full word in the (dr, dc) direction that includes (r, c)."""
    start_r, start_c = r, c
    # Move backwards to start of word
    while 0 <= start_r - dr < GRID_SIZE and 0 <= start_c - dc < GRID_SIZE and grid[start_r - dr][start_c - dc] != EMPTY:
        start_r -= dr
        start_c -= dc
    
    letters = []
    rr, cc = start_r, start_c
    while 0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE and grid[rr][cc] != EMPTY:
        letters.append(grid[rr][cc])
        rr += dr
        cc += dc
    return "".join(letters)

def is_valid_word(word, dictionary):
    return word in dictionary

def can_place(grid, word, row, col, direction, dictionary):
    dr, dc = DIRECTIONS[direction]
    # Check bounds and conflicts
    for i, letter in enumerate(word):
        r = row + i * dr
        c = col + i * dc
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
            return False
        current = grid[r][c]
        if current != EMPTY and current != letter:
            return False
    
    # Simulate placing the word temporarily
    temp_grid = [list(row) for row in grid]
    for i, letter in enumerate(word):
        r = row + i * dr
        c = col + i * dc
        temp_grid[r][c] = letter
    
    # Determine perpendicular direction for checking intersections
    if direction == 'H':
        perp_dr, perp_dc = 1, 0  # vertical words cross horizontal
    else:
        perp_dr, perp_dc = 0, 1  # horizontal words cross vertical
    
    # Check all intersecting words formed
    for i in range(len(word)):
        r = row + i * dr
        c = col + i * dc
        formed_word = get_word_in_direction(temp_grid, r, c, perp_dr, perp_dc)
        if len(formed_word) > 1 and not is_valid_word(formed_word, dictionary):
            return False
    
    # Also check the word itself is valid (important for first placement)
    if not is_valid_word(word, dictionary):
        return False

    return True

def place_word(grid, word, row, col, direction):
    dr, dc = DIRECTIONS[direction]
    for i, letter in enumerate(word):
        r = row + i * dr
        c = col + i * dc
        grid[r][c] = letter

def find_overlap(grid, word, dictionary):
    best_options = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            for direction in DIRECTIONS:
                dr, dc = DIRECTIONS[direction]
                for i, letter in enumerate(word):
                    rr = r - i * dr
                    cc = c - i * dc
                    if not (0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE):
                        continue
                    if can_place(grid, word, rr, cc, direction, dictionary):
                        # Count overlaps
                        overlap_count = 0
                        for j, l in enumerate(word):
                            rj = rr + j * dr
                            cj = cc + j * dc
                            if grid[rj][cj] == l:
                                overlap_count += 1
                        if overlap_count > 0:
                            best_options.append((overlap_count, rr, cc, direction))
    if best_options:
        best_options.sort(reverse=True)
        _, rr, cc, direction = best_options[0]
        return rr, cc, direction
    return None

def place_anywhere(grid, word, dictionary):
    positions = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            for direction in DIRECTIONS:
                if can_place(grid, word, r, c, direction, dictionary):
                    positions.append((r, c, direction))
    if positions:
        return random.choice(positions)
    return None

def generate_crossword(word_list, dictionary):
    grid = create_grid()
    placed = []

    random.shuffle(word_list)
    first_word = word_list[0].upper()

    # Try placing first word at center
    direction = random.choice(['H', 'V'])
    start_r = GRID_SIZE // 2
    start_c = (GRID_SIZE - len(first_word)) // 2 if direction == 'H' else GRID_SIZE // 2

    if can_place(grid, first_word, start_r, start_c, direction, dictionary):
        place_word(grid, first_word, start_r, start_c, direction)
        placed.append(first_word)
    else:
        print(f"⚠️ Could not place first word: {first_word}")

    # Place remaining words
    for word in word_list[1:]:
        word = word.upper()
        pos = find_overlap(grid, word, dictionary)
        if not pos:
            pos = place_anywhere(grid, word, dictionary)
        if pos:
            place_word(grid, word, *pos)
            placed.append(word)
        else:
            print(f"⚠️ Skipped word (no valid placement): {word}")

    return grid, placed

# --- Main Program ---
print("🧩 Kiswahili Crossword Generator (Valid words horizontally and vertically)\n")
grid, placed_words = generate_crossword(words, dictionary)
print_grid(grid)
print("\n✅ Words placed:", ", ".join(placed_words))
