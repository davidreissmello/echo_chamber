import pandas as pd 

data = pd.read_csv('All_Gender_Location_Political_Echochambers_Subset__Friends__BrandID_FollowerID_FriendID.csv', 
                  sep = '\t', skiprows=10000000, nrows=1000)
data.columns = ['candidates', 'followers', 'followers1']

c_followers = pd.read_csv('Followers_Clinton_Trump.csv')

results = list()

clinton = 1339835893
trump = 25073877

CANDIDATES = [clinton, trump]

for candidate in CANDIDATES:
	opponent = [x for x in CANDIDATES if x != candidate][0]
	candidate_df = data[data['candidates'] == candidate]
	
	CANDIDATE_FOLLOWERS = set(c_followers[c_followers['brand_id'] == candidate].user_id.tolist())
	OPPONENT_FOLLOWERS = set(c_followers[c_followers['brand_id'] == opponent].user_id.tolist())

	for follower in candidate_df.followers.unique():
		candidate_follower_df = candidate_df[candidate_df['followers'] == follower]
		candidate_follower_followers1 = set(candidate_follower_df.followers1)
		
		followers1_that_follow_candidate = CANDIDATE_FOLLOWERS.intersection(candidate_follower_followers1)
		followers1_that_follow_opponent = OPPONENT_FOLLOWERS.intersection(candidate_follower_followers1)
		followers1_that_follow_candidate_opponent = followers_that_follow_candidate.intersection(followers_that_follow_opponent)
                
		try:
			results.append((candidate, 
							follower, 
							len(followers1_that_follow_candidate),  #number of followers1 that follow candidate
							len(candidate_follower_followers1), #number of followers follower has 
							len(followers1_that_follow_candidate)/len(candidate_follower_followers1), #echo-chambver
							len(CANDIDATE_FOLLOWERS), #number of followers candidate has  
							len(followers1_that_follow_candidate)/len(candidate_follower_followers1)/len(CANDIDATE_FOLLOWERS), #echo-chamber normalized
							len(followers1_that_follow_opponent), #followers that follow opponent 
							len(followers1_that_follow_candidate_opponent))) #followers that follow candidate and opponent 
		except:
			results.append((candidate, follower, count, len(candidate_followers1), 'error', n_followers, 'error',
					count_opponent, count_candidate_opponent))

echo = pd.DataFrame(results, columns = ['candidates', 
										'followers', 
                                        'followers1_that_follow_candidate', 
                                        'candidate_follower_followers1',
                                        'echo_chamber',
                                        'n_candidate_followers',
                                        'echo_chamber_normalized',
										'followers1_that_follow_opponent', 
										'followers1_that_follow_candidate_opponent'])

echo.to_csv('echo_computation2016.csv', index=False)