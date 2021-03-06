import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, f1_score
from tpot_metrics import balanced_accuracy_score
from sklearn.pipeline import make_pipeline
import itertools

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t').sample(frac=1., replace=False, random_state=42)

for (n_neighbors, weights) in itertools.product(list(range(1, 26)) + [50, 100],
                                                ['uniform', 'distance']):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            KNeighborsClassifier(n_neighbors=n_neighbors,
                                                 weights=weights))
        # 10-fold CV score for the pipeline
        cv_predictions = cross_val_predict(estimator=clf, X=features, y=labels, cv=10)
        accuracy = accuracy_score(labels, cv_predictions)
        macro_f1 = f1_score(labels, cv_predictions, average='macro')
        balanced_accuracy = balanced_accuracy_score(labels, cv_predictions)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'n_neighbors={},'.format(n_neighbors)
    param_string += 'weights={}'.format(weights)

    out_text = '\t'.join([dataset.split('/')[-1][:-7],
                          'KNeighborsClassifier',
                          param_string,
                          str(accuracy),
                          str(macro_f1),
                          str(balanced_accuracy)])

    print(out_text)
    sys.stdout.flush()
