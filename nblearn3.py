import re
import math
def main():
    list_of_reviews = []
    no_of_reviews = 0
    general_dict = {}
    pos_truthful = {}
    pos_deceptive = {}
    neg_truthful = {}
    neg_deceptive = {}
    dict={}
    with open("train-text.txt","r") as file:
        for line in file:
            list_of_reviews.append(line)
            no_of_reviews += 1
    with open("train-labels.txt", 'r') as labels_file:
        for line in labels_file:
            label_terms = line.split()
            dict[label_terms.pop(0)] = label_terms

    length_of_DP = 0
    length_of_TP = 0
    length_of_DN = 0
    length_of_TN = 0
    no_of_TP = 0
    no_of_DP = 0
    no_of_TN = 0
    no_of_DN = 0

    for review in list_of_reviews:
        TP_flag = 0
        DP_flag = 0
        TN_flag = 0
        DN_flag = 0
        terms = re.split(r'[ ,;.!]', review)
        # terms = review.split()
        key = terms.pop(0)
        list_of_labels = dict[key]
        if list_of_labels[0].lower().strip() == "truthful" and list_of_labels[1].lower().strip() == "positive":
            no_of_TP += 1
            TP_flag = 1
        elif list_of_labels[0].lower().strip() == "deceptive" and list_of_labels[1].lower().strip() == "positive":
            no_of_DP += 1
            DP_flag = 1
        elif list_of_labels[0].lower().strip() == "truthful" and list_of_labels[1].lower().strip() == "negative":
            no_of_TN += 1
            TN_flag = 1
        elif list_of_labels[0].lower().strip() == "deceptive" and list_of_labels[1].lower().strip() == "negative":
            no_of_DN += 1
            DN_flag = 1
        for term in terms:
            # print(term.lower())
            term = term.lower()
            if re.match(r'[a-zA-Z]', term):
                if TP_flag == 1:
                    length_of_TP+=1
                    if term in general_dict.keys():
                        temp = general_dict[term]
                        temp[0] += 1
                    else:
                        general_dict[term] = [1,0,0,0]

                    # if term in pos_truthful.keys():
                    #     pos_truthful[term] += 1
                    # else:
                    #     pos_truthful[term] = 1
                elif DP_flag == 1:
                    length_of_DP += 1
                    if term in general_dict.keys():
                        temp = general_dict[term]
                        temp[1] += 1
                    else:
                        general_dict[term] = [0,1,0,0]
                    # if term in pos_deceptive.keys():
                    #     pos_deceptive[term] += 1
                    # else:
                    #     pos_deceptive[term] = 1
                elif TN_flag == 1:
                    length_of_TN += 1
                    if term in general_dict.keys():
                        temp = general_dict[term]
                        temp[2] += 1
                    else:
                        general_dict[term] = [ 0, 0, 1, 0]

                    # if term in neg_truthful.keys():
                    #     neg_truthful[term] += 1
                    # else:
                    #     neg_truthful[term] = 1
                elif DN_flag == 1:
                    length_of_DN += 1
                    if term in general_dict.keys():
                        temp = general_dict[term]
                        temp[3] += 1
                    else:
                        general_dict[term] = [0,0,0,1]
                    # if term in neg_deceptive.keys():
                    #     neg_deceptive[term] += 1
                    # else:
                    #     neg_deceptive[term] = 1

        # Smoothing
    # length_of_PD = pos_deceptive.__len__()
    # length_of_PT = pos_truthful.__len__()
    # length_of_ND = neg_deceptive.__len__()
    # length_of_NT = neg_truthful.__len__()
    no_of_terms = general_dict.__len__()
    output = open("nbmodel.txt", 'w')
    for key in general_dict.keys():
        temp_TP = (general_dict[key][0] + 1 ) / (length_of_TP + no_of_terms)
        temp_DP = (general_dict[key][1] + 1 ) / (length_of_DP + no_of_terms)
        temp_TN = (general_dict[key][2] + 1 ) / (length_of_TN + no_of_terms)
        temp_DN = (general_dict[key][3] + 1 ) / (length_of_DN + no_of_terms)
        general_dict[key] = [math.log(temp_TP), math.log(temp_DP), math.log(temp_TN), math.log(temp_DN)]
        # general_dict[key] = [temp_TP, temp_DP, temp_TN, temp_DN]
        # print(terms)
    output.write(str(general_dict))
    output.close()

    output = open("prior_probabilities.txt",'w')
    output.write("Truthful Positive\tDeceptive Positive\tTruthful Negative\tDeceptive Negative\n")
    output.write(str(math.log(no_of_TP / no_of_reviews)) + "\t")
    # output.write(str(no_of_TP / no_of_reviews) + "\t")
    output.write(str(math.log(no_of_DP / no_of_reviews)) + "\t")
    # output.write(str(no_of_DP / no_of_reviews) + "\t")
    output.write(str(math.log(no_of_TN / no_of_reviews)) + "\t")
    # output.write(str(no_of_TN / no_of_reviews) + "\t")
    output.write(str(math.log(no_of_DN / no_of_reviews)))
    # output.write(str(no_of_DN / no_of_reviews))
    output.close()

main()