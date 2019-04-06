class arabiziChecker:

    def __init__(self):
        self.arabizi_word_count = {}
        with open("configuration\elda_dict.txt") as f:
            for line in f:
                l=line.replace('\n','')
                self.arabizi_word_count[l] = 0

    def getDict(self):
        for word in self.arabizi_word_count.keys():
            self.arabizi_word_count[word] = 0
        return self.arabizi_word_count

    def checkTweet(self,tweet):
        d = self.getDict()
        splitToWords=tweet.split(' ')
        with open("configuration\output.txt", 'a') as file:
            for word in splitToWords:
                #print("word is: {}".format(word))
                #file.write("word = {}".format(word))
                #print(word)
                if word in d.keys():
                    d[word]+=1
                    print('arabizi word: {}'.format(word))
        #print(d)
        sum = 0
        for val in d.values():
            #print(val)
            sum = sum+val
        #print("sum of arabizi words = {}".format(sum))
        return sum > 2
