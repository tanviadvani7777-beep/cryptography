def playfair_cipher(plaintext, key):
    # Clean and prepare the plaintext
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    
    # Build the key matrix (5x5)
    key = key.upper().replace("J", "I")
    matrix = []
    for char in key:
        if char not in matrix and char.isalpha():
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # 'J' excluded
        if char not in matrix:
            matrix.append(char)
    matrix = [matrix[i*5:(i+1)*5] for i in range(5)]

    # Helper to find position of letter in matrix
    def find_position(letter):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == letter:
                    return i, j

    # Prepare plaintext digraphs
    i = 0
    pairs = []
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i+1] if i+1 < len(plaintext) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    if len(pairs[-1]) == 1:
        pairs[-1] += 'X'

    # Encrypt the pairs
    ciphertext = ""
    for pair in pairs:
        a, b = pair[0], pair[1]
        row1, col1 = find_position(a)
        row2, col2 = find_position(b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext

# Example usage
plaintext = "HELLO WORLD"
key = "example"
ciphertext = playfair_cipher(plaintext, key)

print("Plaintext:", plaintext)
print("Key:", key)
print("Ciphertext:", ciphertext)