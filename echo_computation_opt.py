#!/apps/anaconda3/bin/python3

import pandas as pd 

test = pd.read_csv('./Subset_359040__Brand_Follower_Friend.csv',  engine='c', sep='\t',header=None)
test.columns = ['candidates', 'followers', 'followers1']
c_followers = pd.read_csv('follower_ids.csv', sep='\t', names=['candidate', 'follower'])

opponents = pd.read_csv('opponents.csv')

results = list()

for candidate in test.candidates.unique():
	tmp_candidate = test[test['candidates'] == candidate]
	candidate_followers = set(c_followers[c_followers['candidate'] == candidate].follower.tolist())
	n_followers = len(candidate_followers)

	candidate_opponent = opponents[opponents['candidates'] == candidate].opponent.tolist() + [None]
	candidate_opponent = candidate_opponent[0]

	opponent_followers = set(c_followers[c_followers['candidate'] == candidate_opponent].follower.tolist())

	for follower in tmp_candidate.followers.unique():
		tmp_candidate_follower = tmp_candidate[tmp_candidate['followers'] == follower]
		candidate_followers1 = set(tmp_candidate_follower.followers1)
		
		followers_that_follow_candidate = candidate_followers.intersection(candidate_followers1)
		count = len(candidate_followers.intersection(candidate_followers1))

		followers_that_follow_opponent = opponent_followers.intersection(candidate_followers1)
		count_opponent = len(followers_that_follow_opponent)
		
		followers_that_follow_candidate_opponent = followers_that_follow_candidate.intersection(followers_that_follow_opponent)
		count_candidate_opponent = len(followers_that_follow_candidate_opponent)
		
		
                
		try:
			results.append((candidate, 
					follower, 
					count, 
					len(candidate_followers1),
					count/len(candidate_followers1), 
					n_followers, 
					count/len(candidate_followers1)/n_followers,
					count_opponent,
					count_candidate_opponent))
		except:
			results.append((candidate, follower, count, len(candidate_followers1), 'error', n_followers, 'error',
					count_opponent, count_candidate_opponent))

echo = pd.DataFrame(results, columns = ['candidates', 
					'followers', 
                                        'f_of_f_candidate_followers', 
                                        'n_f_of_f',
                                        'ratio',
                                        'n_candidate_followers',
                                        'ratio_normalized',
					'opponent_followers', 
					'candidate_and_opponent_followers'])

echo.to_csv('echo_computation3.csv', index=False)
