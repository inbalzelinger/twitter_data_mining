class arabiziChecker:

    def __init__(self):
        self.arabizi_word_count = {}
        #with open("ArabiziDict.txt") as f:
        with open("arabicDict.txt",encoding='utf-8') as f:
            for line in f:
                l=line.replace('\n','')
                self.arabizi_word_count[l] = 0

    def getDict(self):
       return self.arabizi_word_count

    def checkTweet(self,tweet):
        for k in self.arabizi_word_count.keys():
            self.arabizi_word_count[k]=0
        #d=self.getDict()
        splitToWords=tweet.split(' ')
        for word in splitToWords:
            if word in self.arabizi_word_count.keys():
                self.arabizi_word_count[word]+=1
        for k in self.arabizi_word_count.keys():
            if self.arabizi_word_count[k]>0:
                print(self.arabizi_word_count[k], k)
        count=0
        for val in self.arabizi_word_count.values():
            count=count+val
        return count>1
