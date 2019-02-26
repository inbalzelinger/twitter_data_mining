class arabiziChecker:

    def __init__(self):
        self.arabizi_word_count = {}
        with open("arabiziDict.txt") as f:
            for line in f:
                l=line.replace('\n','')
                self.arabizi_word_count[l] = 0

    def getDict(self):
       return self.arabizi_word_count

    def checkTweet(self,tweet):
        d=self.getDict()
        splitToWords=tweet.split(' ')
        for word in splitToWords:
            # print(word)
            if word in d.keys():
                d[word]+=1
        # print(d)
        sum=0
        for val in d.values():
            # print(val)
            sum=sum+val
        print("sum of arabizi words = {}".format(sum))
        return sum>0
