def operation(sentence):
    #Counting the total characters
    print(len(sentence))
    
    #counting the Total Words
    words=sentence.split()
    print(words)
    
    #Reverse the Sentence
    reverse=sentence[::-1]
    reversed=" ".join(words[::-1])
    print(f"The Reversed sentence is :{reverse}")
    print(f"The reveresed Correect is:{reversed}")
    
    #Checking Palindrome
    if sentence == reversed:
        print("This is a Palindrome Sentence")
    else:
        print("This is not a Palindrome Sentence")
    
    #finding The Frequency of each word
    freq={}
    for word in words:
        if word in freq:
            freq[word]+=1
        else:
            freq[word]=1
    
    print(freq) 
    
  
sentence=input("Enter the Sentence:")
print (sentence)
operation(sentence)

