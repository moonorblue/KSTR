# KSTR

(optional) install virtualenv

    curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
    tar xvfz virtualenv-X.X.tar.gz
    cd virtualenv-X.X
    python virtualenv.py --system-site-packages myVE 

(optional) use virtualenv with pip

    myVE/bin/pip

(optional) use virtualenv local python

    myVE/bin/python 

use pip to install required library

    pip install -r pip-requirement.txt
    
    
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
*   expV6_ca_greedypruning_TopN.py expV6_fb_greedypruning_TopN.py

    >Experiment of greedy pruning (Top-N%) (Figure 8)
    
    >Use expV6_ca_parallel_skyline_avg_user_checkincount_p.csv, expV6_fb_parallel_skyline_avg_user_checkincount_p.csv to calculate the reconstruct-routes chosen ratio of skyline query
    
    >Use expV6_ca_parallel_skyline_user_checkincount_time_p.csv, expV6_fb_parallel_skyline_user_checkincount_time_p.csv to calculate the reconstruct time and total process time
*   expV7_ca_multi_0.1.py, expV7_fb_multi_0.1.py 

    >Experiment of goodness (Figure 10)
    
    >Use each csv file with different ranking methods to calculate the goodness of cover ratio,edit distance and consine similarity
*   expV8_ca_multi_0.1_KM.py, expV8_fb_multi_0.1_KM.py 

    >Experiment of goodness and prcoess time with keyword matching score
    
    >Use each csv file with different ranking methods to calculate the goodness of cover ratio,edit distance and consine similarity
*   expPerformance_ca_multi.py, expPerformance_ca_seq.py,
expPerformance_fb_multi.py, expPerformance_fb_seq.py

    >Experiment of sequential and multiprocess processing time (Figure 9)
    
    >Use output(process time) of code to draw Figure 9
    >> multiprocess include multi-scoring and multi-skyline search
*   expPerformance_ca_multi_test.py, expPerformance_fb_multi_test.py

    >Experiment of choosing multi-processes number by response time (process time)
    
    >The output shows the process time
*   expPerformance_ca_multi_n_performance.py, expPerformance_fb_multi_n_performance.py

    >Experiment of processing time by greedy pruning (Top-N%) with different covered routes amount
    
    >Use time csv to get the result of different covered routes amoun


##KSTR_demo
*   core/app.py

    >KSTR core with Flask framework (REST api), return multiple result chosed by KSTR
    
*   web/index.html

    >KSTR demo website built by Bootstrap with jQuery (HTML,Java Script)
    
    >OSM map plug-in by Leaflet
    
    >Routing information by Leaflet routing machine

##Package tutorial
*   use 'pg' to communicate with db in 140.113.86.128

        import pg
        conn_string = "host='***.***.***.***' dbname='*****' user='*****' password='****'"
        conn = pg.connect(conn_string)
        query = "SELECT a,b From c;"
        rows = conn.query(query).getresult() 
        for row in rows:
            a = row[0]
            b = row[1]
            print ' a = %s , b = %s' % ( a, b )
            
*   use 'psycopg2' to communicate with db in 140.113.86.128

        import psycopg2
        conn_string = "host='***.***.***.***' dbname='*****' user='*****' password='****'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        query = "SELECT a,b From c;"
        cur.execute(query)
        rows = [r for r in cur]
        for row in rows:
            a = row[0]
            b = row[1]
            print ' a = %s , b = %s' % ( a, b )

##Experiment tutorial
*   Make VX experiment directory (V=version)
        
        mkdir ~/exp
        mkdir ~/exp/VX
        mkdir ~/exp/VX/ca
        mkdir ~/exp/VX/fb

*   Change experiment data saving path in code

        
        with open('/home/moonorblue/exp/V8/fb/allScore/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_allScore:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')

            w.close()
        
        with open('/home/moonorblue/exp/V9/fb/allScore/expV9_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_allScore:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')

            w.close()

*   Copy dictionary data (POI information, socail relation ... etc) to local directory

        mkdir ~/socialINF
        mkdir ~/exp/materials
        cp /home/moonorblue/socialINF/* ~/socialINF
        cp /home/moonorblue/exp/materials ~/exp/materials


##Experiment csv file format

    original rid,cover routes,total time,skyline time,reconstruction time, reconstruct scoring time, original route scoring time

##Original route format extracted from  signle user

    {
      "route": {
        "0": [
          {
            "pid": "39834",
            "time": "1269455293.0"
          }
        ],
        "1": [
          {
            "pid": "41593",
            "time": "1269546020.0"
          },
          {
            "pid": "268",
            "time": "1269601699.0"
          }
        ],
        "15": [
          {
            "pid": "298",
            "time": "1270756911.0"
          },
          {
            "pid": "13120",
            "time": "1270811956.0"
          },
          {
            "pid": "295",
            "time": "1270833028.0"
          }
        ]
      },
      "uid": "790"
    }
    

##Route with scores, cateogries and metadata extracted from single user

    {
      "route": [
        [
          {
            "category": "Travel & Transport,Shop & Service,Hotel",
            "timeScore": 0.47236655274101524,
            "pid": "50163",
            "PATS": 1,
            "longitude": "-118.32827612555799",
            "time": "1296921889.0",
            "latitude": "33.34510138630335"
          },
          {
            "category": "Outdoors & Recreation,Athletics & Sports",
            "timeScore": 1,
            "pid": "50164",
            "PATS": 1,
            "longitude": "-118.32670211791992",
            "time": "1296931420.0",
            "latitude": "33.34268272115012"
          },
          {
            "category": "Travel & Transport,Shop & Service,Hotel",
            "timeScore": 1,
            "pid": "50163",
            "PATS": 1,
            "longitude": "-118.32827612555799",
            "time": "1296991625.0",
            "latitude": "33.34510138630335"
          },
          {
            "category": "Travel & Transport,Shop & Service,Hotel",
            "timeScore": 1,
            "pid": "50163",
            "PATS": 1,
            "longitude": "-118.32827612555799",
            "time": "1296991625.0",
            "latitude": "33.34510138630335"
          }
        ],
        [
          {
            "category": "Arts & Entertainment",
            "timeScore": 1,
            "pid": "50176",
            "PATS": 0.8713,
            "longitude": "-117.62486457824707",
            "time": "1281717335.0",
            "latitude": "33.42442134811548"
          },
          {
            "category": "Nightlife Spot,Food",
            "timeScore": 0.724277519974214,
            "pid": "8558",
            "PATS": 0.8411,
            "longitude": "-117.77154943759312",
            "time": "1281730491.0",
            "latitude": "33.529358800455434"
          },
          {
            "category": "Arts & Entertainment",
            "timeScore": 0.49810596371713456,
            "pid": "50176",
            "PATS": 0.8713,
            "longitude": "-117.62486457824707",
            "time": "1281785187.0",
            "latitude": "33.42442134811548"
          }
        ]
      ],
      "uid": "999"
    }

##Latex source files
* ICDM2015_cr.tex

    >main file, include other part of paper, edit these part inside with the corresponding .tex file
    
    >>1_introduction-v1.tex
    
    >>2_framework_v1.tex
    
    >>3_1_keyword.tex
    
    >>3_2_feature-v1.tex
    
    >>4_1_keyword.tex
    
    >>4_skyline_v1.tex
    
    >>5_experiment_yeo.tex
    
    >>5_experiment-v1.tex
