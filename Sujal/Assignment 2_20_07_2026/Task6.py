def is_prime(number:int) ->bool:
    if number<=1:
        return False
    for i in range(2,number):
        if number%i==0:
            return False
        else:
            return True
        
def fact(number:int) ->int:
    if number==0 or number ==1:
        return 1
    return number *fact(number-1)

def is_even(number:int) ->bool:
    if number%2==0:
        print("Number is Prime")
    else:
        print("Number is odd")

def largest(number:list[int])->int:
    return max(number)

def average(number:list[int]) ->int:
    count=len(number)
    summ=sum(number)
    
    return summ/count

#driver Code
print(is_prime(5))
print(fact(5))
print(is_even(19))
print(largest([10,20,9,5,35]))
print(average([10,20,9,5,35]))
