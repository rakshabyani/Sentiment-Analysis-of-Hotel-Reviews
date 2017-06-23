import ast
import re
import math
def main():
    list_of_test_reviews = []
    with open("nbmodel.txt",'r') as file:
        model = file.read()

    dict = ast.literal_eval(model)
    # print(dict)
    with open("test-text.txt",'r') as file:
        for line in file:
            list_of_test_reviews.append(line)

    # list_of_test_reviews = ["1 DIRTY POOL"]

    with open("prior_probabilities.txt",'r') as file:
        # no_of_reviews = int(file.readline())
        heading = file.readline()
        priors = file.readline().split()
        TP_prior = float(priors[0])
        DP_prior = float(priors[1])
        TN_prior = float(priors[2])
        DN_prior = float(priors[3])

    output = open("nboutput.txt", 'w')
    for review in list_of_test_reviews:
        terms = re.split(r'[ ,;.!]', review)
        PTP = TP_prior
        PDP = DP_prior
        PTN = TN_prior
        PDN = DN_prior
        # terms = review.split()
        key = terms.pop(0)
        for term in terms:
            term = term.lower()
            if term in dict.keys():
                probabilities = dict[term]
            PTP += probabilities[0]
            PDP += probabilities[1]
            PTN += probabilities[2]
            PDN += probabilities[3]
        max_no = max(PTP, PDP, PTN, PDN)
        if PTP == max_no:
            output.write(key + " truthful positive")
            output.write("\n")
        elif PDP == max_no:
            output.write(key + " deceptive positive")
            output.write("\n")
        elif PTN == max_no:
            output.write(key + " truthful negative")
            output.write("\n")
        else:
            output.write(key + " deceptive negative")
            output.write("\n")

    output.close()
main()