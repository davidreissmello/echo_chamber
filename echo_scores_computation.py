#!/apps/anaconda3/bin/python3

import pandas as pd

test = pd.read_csv('./Subset_359040__Brand_Follower_Friend.csv',  engine='c', sep='\t',header=None)
test.columns = ['candidates', 'followers', 'followers1']

results = list()

for candidate in test.candidates.unique():
        tmp_candidate = test[test['candidates'] == candidate]
        candidate_followers = set(tmp_candidate.followers.unique())
        n_followers = len(candidate_followers)

        for follower in tmp_candidate.followers.unique():
                tmp_candidate_follower = tmp_candidate[tmp_candidate['followers'] == follower]
                candidate_followers1 = set(tmp_candidate_follower.followers1)
                count = len(candidate_followers.intersection(candidate_followers1))

                results.append((candidate,
                                follower,
                                count,
                                len(candidate_followers1),
                                count/len(candidate_followers1),
                                n_followers,
                                count/len(candidate_followers1)/n_followers))


echo = pd.DataFrame(results, columns = ['candidates',
                                        'followers',
                                        'f_of_f_candidate_followers',
                                        'n_f_of_f',
                                        'ratio',
                                        'n_candidate_followers',
                                        'ratio_normalized'])

echo.to_csv('echo_computation1.csv', index=False)
