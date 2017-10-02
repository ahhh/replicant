# replicant
social media bots

v0.3 is a reddit comment / vote bot

example of how to automate the reddit bot on a server w/ a cron file:

45 \*/2 * * * python /opt/replicant/replicant.py -c config -w /opt/replicant/comments.txt -t 600 -f the
51 \*/2 * * * python /opt/replicant/replicant.py -c config2 -w /opt/replicant/comments.txt -t 600 -f is
22 \*/4 * * * python /opt/replicant/replicant.py -c config4 -w /opt/replicant/comments.txt -t 3000
12 \*/2 * * * python /opt/replicant/replicant.py -c config5 -w /opt/replicant/comments.txt -t 3000

15 \*/3 * * * python /opt/replicant/replicant.py -c config -w /opt/replicant/comments.txt -t 30000
16 4 * * * python /opt/replicant/replicant.py -c config -w /opt/replicant/comments.txt -t 30000 -r some_example_user_2 

25 \*/8 * * * python /opt/replicant/upvote.py -t 5 -f the -c config
0 \*/8 * * * python /opt/replicant/upvote.py -t 5 -f is -c config2
42 \*/8 * * * python /opt/replicant/upvote.py -t 5 -f security -c config3

42 2 * * * python /opt/replicant/upvote.py -t 5 -r some_example_user_1 -c config
42 5 * * * python /opt/replicant/upvote.py -t 5 -r some_example_user_2  -c config2
42 10 * * * python /opt/replicant/upvote.py -t 5 -r some_example_user_3  -c config
