def Transform_A_to_B(A_coordinates):
    X = A_coordinates[0] + 23.33
    Y = A_coordinates[1] + 1433.77
    Z = A_coordinates[2] + 57.35 
    W = -A_coordinates[3] if A_coordinates[3] is not None else None
    P = -A_coordinates[4] if A_coordinates[4] is not None else None
    R = -A_coordinates[5] if A_coordinates[5] is not None else None
    result = [X, Y, Z, W, P, R]
    return result

A_coordinates = [567, -528, 151, 90, 30, 0]
result = Transform_A_to_B(A_coordinates)
print(result)