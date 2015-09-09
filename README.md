# KSTR

##KSTR_algorithm
*   RouteExtration.py 

    > Extract routes from original dataset
*   PATS.py

    > Process PATS score
*   SocialINF_Pre_CheckinCount.py 

    >Preprocess of social influence score, calculate checkin counts
*   SocialINF_Pre_FollowFriendCount_CA.py, SocialINF_Pre_FollowFriendCount_FB.py

    >Preprocess of social influence score, calculate following friends counts

*   SocialINF.py

    >Process social influence score
*   TimeDistribution_Pre.py
  
    >Preprocess of time score
*   TimeDistribution.py

    >Process time score and save with routes
*   ConbineOfflineScore.py
    
    >Add all POI scores with routes
*   InsertToDB

    >Insert all routes data into PostgreSQL database
*   expV6_ca_1000.py expV6_fb_1000.py

    >Experiment of greedy pruning (Top-N%) (Figure 8)
*   expV7_ca_multi_0.1.py, expV7_fb_multi_0.1.py 

    >Experiment of goodness and prcoess time (Figure 10)
*   expV8_ca_multi_0.1_KM.py, expV8_fb_multi_0.1_KM.py 

    >Experiment of goodness and prcoess time with keyword matching score
*   expPerformance_ca_multi.py, expPerformance_ca_seq.py,
expPerformance_fb_multi.py, expPerformance_fb_seq.py

    >Experiment of sequential and multiprocess processing time (Figure 9)
    >> multiprocess include multi-scoring and multi-skyline search
*   expPerformance_ca_multi_test.py, expPerformance_fb_multi_test.py

    >Experiment of choosing multi-processes number by response time
*   expPerformance_ca_multi_n_performance.py, expPerformance_fb_multi_n_performance.py

    >Experiment of processing time by greedy pruning (Top-N%) with different covered routes amount



##KSTR_demo
*   core/app.py

    >KSTR core with Flask framework (REST api), return multiple result chosed by KSTR
    
*   web/index.html

    >KSTR demo website built by Bootstrap with jQuery (HTML,Java Script)
    
    >OSM map plug-in by Leaflet
    
    >Routing information by Leaflet routing machine
