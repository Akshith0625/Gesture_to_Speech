def classify_isl_letter(left, right):
    """
    Classifies the ISL letter based on given left and right hand landmarks.
    'left' and 'right' are lists of hand landmarks obtained from MediaPipe.
    """
    if not left and not right:
        return None  # No hands detected

    # Define classification conditions
    def is_a():
        return (
            left and right and  # Check if both hands are present
            left[4].x > left[3].x and  # Left thumb extended
            all(left[i].y > left[i - 2].y for i in (8, 12, 16, 20)) and  # Left fingers curled
            right[4].x < right[3].x and  # Right thumb extended
            all(right[i].y > right[i - 2].y for i in (8, 12, 16, 20))  # Right fingers curled
        )

    def is_b():
        return (
            left and right and  # Check if both hands are present
            left[4].y < left[3].y and  # Thumb tucked in
            all(left[i].y < left[i - 2].y for i in (8, 12, 16, 20)) and  # All fingers extended
            right[4].y < right[3].y and  # Right-hand thumb tucked
            all(right[i].y < right[i - 2].y for i in (8, 12, 16, 20))  # Right-hand fingers extended
        )

    def is_c():
        return (
            left and  # Check if left hand is present
            left[4].x > left[3].x and  # Thumb extended
            left[8].x > left[6].x and  # Index finger curved
            left[12].x > left[10].x and  # Middle finger curved
            left[16].x > left[14].x and  # Ring finger curved
            left[20].x > left[18].x  # Pinky curved
        )

    def is_d():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and  # Index finger extended
            all(left[i].y > left[i - 2].y for i in (12, 16, 20)) and  # Other fingers curled
            left[4].y > left[3].y  # Thumb tucked in
        )

    def is_e():
        return (
            left and right and  # Check if both hands are present
            left[4].y > left[3].y and  # Thumb tucked
            all(left[i].y > left[i - 2].y for i in (8, 12, 16, 20)) and  # All fingers curled
            right[4].y > right[3].y and
            all(right[i].y > right[i - 2].y for i in (8, 12, 16, 20))  # Right-hand curled
        )

    def is_f():
        return (
            left and  # Check if left hand is present
            left[4].x < left[8].x and  # Thumb touching index finger
            left[12].y > left[10].y and  # Middle finger down
            left[16].y > left[14].y and  # Ring finger down
            left[20].y > left[18].y and  # Pinky down
            left[8].y < left[6].y  # Index finger extended
        )

    def is_g():
        return (
            left and  # Check if left hand is present
            left[4].x > left[3].x and  # Thumb extended
            left[8].x > left[6].x and  # Index finger extended
            all(left[i].y > left[i - 2].y for i in (12, 16, 20))  # Other fingers curled
        )

    def is_h():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and  # Index & Middle fingers extended
            all(left[i].y > left[i - 2].y for i in (16, 20))  # Other fingers curled
        )

    def is_i():
        return (
            left and  # Check if left hand is present
            left[20].y < left[18].y and  # Pinky extended
            all(left[i].y > left[i - 2].y for i in (8, 12, 16))  # Other fingers curled
        )

    def is_j():
        return (
            is_i() and  # Pinky extended
            left[20].x > left[18].x  # Pinky moving in an arc
        )

    def is_k():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and  # Index & Middle fingers extended
            left[4].x > left[3].x  # Thumb extended
        )

    def is_l():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and  # Index finger extended
            left[4].x > left[3].x and  # Thumb extended
            all(left[i].y > left[i - 2].y for i in (12, 16, 20))  # Other fingers curled
        )

    def is_m():
        return (
            left and  # Check if left hand is present
            all(left[i].y < left[4].y for i in (8, 12, 16)) and  # Three fingers touching palm
            left[20].y > left[18].y  # Pinky slightly extended
        )

    def is_n():
        return (
            left and  # Check if left hand is present
            all(left[i].y < left[4].y for i in (8, 12)) and  # Two fingers touching palm
            left[16].y > left[14].y and left[20].y > left[18].y  # Ring & Pinky extended
        )

    def is_o():
        return (
            left and  # Check if left hand is present
            left[4].x > left[3].x and  # Thumb extended
            left[8].x > left[6].x and  # Index finger curved
            left[12].x > left[10].x and  # Middle finger curved
            left[16].x > left[14].x and  # Ring finger curved
            left[20].x > left[18].x  # Pinky curved
        )

    def is_p():
        return (
            is_k() and left[8].y > left[6].y  # Index finger bent down
        )

    def is_q():
        return (
            is_g() and left[8].y > left[6].y  # Index finger bent down
        )

    def is_r():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and  # Index & Middle fingers extended
            left[8].x < left[12].x  # Fingers crossed
        )

    def is_s():
        return (
            is_a() and left[4].y > left[3].y  # Thumb across fist
        )

    def is_t():
        return (
            is_s() and left[4].y < left[8].y  # Thumb between index and middle finger
        )

    def is_u():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and  # Index & Middle fingers extended
            left[8].x > left[12].x  # Fingers not crossed
        )

    def is_v():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and  # Index & Middle fingers extended
            left[16].y > left[14].y and left[20].y > left[18].y  # Ring & Pinky curled
        )

    def is_w():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and left[12].y < left[10].y and left[16].y < left[14].y and  # Index, Middle & Ring fingers extended
            left[20].y > left[18].y  # Pinky curled
        )

    def is_x():
        return (
            left and  # Check if left hand is present
            left[8].y < left[6].y and  # Index finger extended
            left[12].y > left[10].y and left[16].y > left[14].y and left[20].y > left[18].y  # Other fingers curled
        )

    def is_y():
        return (
            left and  # Check if left hand is present
            left[4].x > left[3].x and  # Thumb extended
            left[20].y < left[18].y and  # Pinky extended
            all(left[i].y > left[i - 2].y for i in (8, 12, 16))  # Other fingers curled
        )

    def is_z():
        return (
            is_i() and  # Pinky extended
            left[20].x < left[18].x  # Pinky moving in a zigzag
        )

    letter_conditions = {
        "A": is_a, "B": is_b, "C": is_c, "D": is_d, "E": is_e, "F": is_f,
        "G": is_g, "H": is_h, "I": is_i, "J": is_j, "K": is_k, "L": is_l,
        "M": is_m, "N": is_n, "O": is_o, "P": is_p, "Q": is_q, "R": is_r,
        "S": is_s, "T": is_t, "U": is_u, "V": is_v, "W": is_w, "X": is_x,
        "Y": is_y, "Z": is_z
    }

    for letter, condition in letter_conditions.items():
        if condition():
            return letter

    return None  # No matching letter found