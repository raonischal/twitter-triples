import sys, subprocess

class extract_entities:
    def __init__(self):
        self.ark_path = "ark-tweet-nlp-0.3.2/"
        return

    def tag_tweets(self, file_name):
        output = subprocess.Popen([self.ark_path + "runTagger.sh", file_name], stdout = subprocess.PIPE).communicate()
        result = output[0].split("\n")
        result = result[:-1]
        for line in result:
            parts = line.split('\t')
            tokens = parts[0].split()
            print tokens
            tags = parts[1].split()
            print tags
            pairs = ["%s/%s" % (tok, tag) for tok,tag in zip(tokens,tags)]
            print pairs
        return

    def get_named_entities(self, file_name):
        return


if __name__ == "__main__":
    entityExtractor = extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
