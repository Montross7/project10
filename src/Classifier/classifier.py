import numpy as np
np.random.seed(0)

from sklearn.ensemble import RandomForestClassifier

def make_feature_vector(authorID, papaerID):
    pass

def computeMAP(forest):
    fValid = open("data/Valid.csv", 'r')
    fValidSol = open("data/ValidSolution.csv", 'r')
    # read out the first headline from each database, and then ignore
    fValid.readline();
    fValidSol.readline();

    N, MAP = 0, 0; 

    while 1:
        ValidLine = fValid.readline()
        ValidSolLine = fValidSol.readline()
        if not ValidLine: break
        
        N+=1
        v = ValidLine.replace(',', ' ').strip('\n').split(' ')[:-1]
        vs = ValidSolLine.replace(',', ' ').strip('\n').split(' ')[:-1]

        # cast types of attributes from strings to integers
        v = [int(v[i]) for i in range(len(v))]
        vs = [int(vs[i]) for i in range(1,len(vs))]

        # if denominator of AveP formula is 0, just set AveP to 0 and continue on
        if len(v)==1 or len(vs)==0:
            continue
      
        # construct feature matrix of size [n_samples X n_features
        # and then run it with random_forest to produces probabilities
        X = [make_feature_vector(v[0],v[i]) for i in range(1, len(v))]
        Y = forest.predict_proba(X)

        # combine the output probabilities with original paperlist as tuples,
        # and then sort them from higher probabilities to lower
        tuples = [(v[i+1], Y[i]) for i in range(len(Y))]
        sorted(tuples, key=lambda x: x[1], reverse=True)

        k = 1
        AveP = 0.
        for i in range(len(tuples)):
            if tuples[i][0] in vs:
                Avep += float(k)/i
                k+=1
        Avep /= min(len(tuples), len(vs))
        MAP += Avep

    return MAP

if __name__ == "__main__":
    # initialize random_forest classifier with given parameters (parameter tuning needed)
    forest = RandomForestClassifier(n_estimators=10)

    # X is a feature matrix of size [n_samples, n_features]
    # Y is a output matrix of size [n_samples, n_outputs]
    X = [], Y = []

    # have the classifier learn from inputs and outputs, say X and Y
    forest.fit(X, Y)

    # after having finished learning, examine the accuracy of classifier using MAP metric
    computeMAP(forest)
