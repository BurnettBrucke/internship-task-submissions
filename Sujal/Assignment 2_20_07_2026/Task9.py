class TopTen:
    def __init__(self):
        self.num=1
    def __iter__(self):
        return self
    def __next__(self):
        if self.num<=10:
            val=self.num
            self.num+=1
            return val
        else:
            raise StopIteration

def even():
    n=1
    while n<=50:
        if(n%2==0):
            yield n
        n+=1
        

num=even()
for i in num:
    print(i)


values=TopTen()
for i in values:
    print(i)


