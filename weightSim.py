#                                TERM WEIGHT SIMILARITY
#                                by RaaulstHub
#
# This algorithm aims to precisely compare and get the similarity between
# two brazilian supermarket invoice product descriptions

import stringdist as sd
import pylcs

# minimum similarity to be considered 'similar' in similarity count
edit_distance_minimum_similarity = 0.8
lcs_minimum_similarity = 0.8


# Calculates Term Weight Similarity between two products description strings
def tws_similarity(prod1, prod2):
    sim = 0  # similarity starts at zero
    prod1_list = prod1.split(' ')  # separating first product's terms in a list (tokenizing by the character ' ')
    prod2_list = prod2.split(' ')  # separating second product's terms in a list (tokenizing by the character ' ')

    if prod1_list[0] == prod2_list[0]:  # tests if the first terms from both products (most important) are equal
        print(f"Added 1.5 because two first terms are equal")
        sim += 1.5

    elif (min(len(prod1_list[0]),
              len(prod2_list[0])) >= 3):  # terms have len > than 3 (avoids edit_d and LCS inconsistency)
        # tests levenshtein similarity between the first terms
        if (1 - (sd.levenshtein(prod1_list[0], prod2_list[0])) / min(len(prod1_list[0]), len(
                prod2_list[0]))) > edit_distance_minimum_similarity:
            print("Added 1.25 because first terms have edit distance similarity")
            sim += 1.25
        # tests if there is a big Longuest Common Subsequence similarity between the first terms
        elif (pylcs.lcs_string_length(prod1_list[0], prod2_list[0]) / min(len(prod1_list[0]), len(prod2_list[0]))) > lcs_minimum_similarity:
            print("Added 1.25 because first terms have LCS similarity")
            sim += 1.25
    # pops the first terms out of the product and sends the remaining terms to less weight evaluation
    prod1_list.pop(0)
    prod2_list.pop(0)
    sim += second_evaluation(prod1_list, prod2_list)
    return sim


# Less significative similarity evaluation (smaller weights)
def second_evaluation(prod1_list, prod2_list):
    print(prod1_list)
    print(prod2_list)
    sim = 0
    for i in prod1_list:
        for j in prod2_list:
            if i == j:  # found equal tokens
                if len(i) > 5:  # has considerable length
                    print("Added 0.25 because there are equal terms with len > 5")
                    sim += 0.25
                else:  # does not have considerable length
                    print("Added 0.1 because there are equal terms with len < 5")
                    print(f'{i} === {j}')
                    sim += 0.1
            elif min(len(i), len(j)) > 5:  # found considerable length word
                if (1 - (sd.levenshtein(i, j)) / max(len(i), len(j))) > 0.8:  # check if there's levenshtein similarity
                    print("Added 0.15 because there are levenshtein similar terms with len > 5")
                    sim += 0.15
                elif (pylcs.lcs_string_length(i, j) / max(len(i), len(j))) > 0.8:  # check if there's lcs similarity
                    print("Added 0.15 because there are lcs similar terms with len > 5")
                    sim += 0.15
    return sim


# Calculates average similarity between a product and a cluster
def cluster_similarity(cluster, product):
    similarity = 0  # score starts at zero
    for i in cluster:
        if str(i) != 'nan':
            similarity += tws_similarity(i, product)  # calculate similarity between product and cluster product
    return similarity / len(cluster)  # calculates average
