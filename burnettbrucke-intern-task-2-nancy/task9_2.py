def even_numbers(limit=50):
    """Yield even numbers from 1 up to `limit` (inclusive)."""
    for num in range(1, limit + 1):
        if num % 2 == 0:
            yield num   # pause here, hand back `num`, resume on next call
 
 
print("Generator Output (even numbers 1 to 50):")
for num in even_numbers(50):
    print(num, end=" ")
    print("\n")
 