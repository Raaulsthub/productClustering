#                       TERM WEIGHT SIMILARITY CLUSTERING
#                       by RaaulstHub


import term_weight_similarity as tws

minimum_similarity = 1.25


# main function -> transform list of products into a list of clusters
def clusterize(product_list):
    product_clusters = []  # cluster list starts blank
    for product in product_list:  # iterates all products in the list
        if not product_clusters:  # if the cluster list in empty, the list's 1st element generates a cluster
            product_clusters.append([product])
        most_similar = None  # variable dedicated to store the existing cluster that is most similar to the product
        similarity = 0  # similarity to be beaten by cluster starts at zero
        for product_cluster in product_clusters:  # iterates the list of clusters
            # if it finds a cluster that's more similar than the best occurrence, it becomes the most similar
            if tws.cluster_similarity(product_cluster, product) > similarity:
                most_similar = product_cluster
                similarity = tws.cluster_similarity(product_cluster, product)

        # if the best case's similarity is not greater than the parameter, a new cluster is created for the product
        if similarity < minimum_similarity:
            product_clusters.append([product])
        # if the best case's similarity is greater or equal the parameter, the product is appended to the cluster
        else:
            most_similar.append(product)
        # product is removed from the list (it's now in the clusters list)
        product_list.remove(product)

    return product_clusters
