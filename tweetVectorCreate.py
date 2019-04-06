class tweetVector:

    def createWordsCountVector(self,tweet):
        wordsContDict={}
        splitToWords=tweet.split(' ')
        for word in splitToWords:
            if word in wordsContDict.keys():
                wordsContDict[word] += 1
            wordsContDict[word] = 1
        return wordsContDict

