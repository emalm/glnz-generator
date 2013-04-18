# Timing and performance

Effects of row caching: negligible improvement in performance

- maybe 5% gain? see logs

Effects of generating at the row level, pruning out bad rows first:

- performance drag at small sizes, weights
- vast performance gains at larger sizes, weights
- WAY faster to generate submatrix first, then generate row and compare, especially with caching
    - 3x3: factor of 5
    - 4x4: factor of 5 for 1 to 12

Average time to generate a matrix, with row pruning?
- length 2:
    - 0.16 ms/matrix for 1 to 20
    - 1.32 ms/matrix for 1 to 101
    - 3.78 ms/matrix for 1 to 200
- length 3:
    - 0.22 ms/matrix for 1 to 17
- length 4:
    - 0.63 ms/matrix for 1 to 