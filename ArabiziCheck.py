class arabiziChecker:

    def __init__(self):
        self.arabizi_word_count = {}
        with open("configuration\elda_dict.txt", encoding='UTF-8') as f:
            for line in f:
                l=line.replace('\n','')
                self.arabizi_word_count[l] = 0

    def getDict(self):
        for word in self.arabizi_word_count.keys():
            self.arabizi_word_count[word] = 0
        return self.arabizi_word_count

    def checkTweet(self,tweet):
        d = self.getDict()
        if "" in d.keys():
            d.__delitem__("")
        splitToWords=tweet.split(' ')
        with open("configuration\output.txt", 'a') as file:
            for word in splitToWords:
                #print("word is: {}".format(word))
                #file.write("word = {}".format(word))
                #print(word)
                if word in d.keys():
                    print('the word is: {}'.format(word))
                    d[word]+=1
        #print(d)
        sum = 0
        for val in d.values():
            #print(val)
            sum = sum+val
        #print("sum of arabizi words = {}".format(sum))
        return sum > 2
