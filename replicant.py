# author: ahhh
# reddit replicant v0.2

import praw
import time, datetime
from optparse import OptionParser
import logging
import importlib
import random
import os


def bot_Login(config):
    r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Replicant",
			)
    print "Logged in as: " + config.username + " at " + str(datetime.datetime.now())
    return r


def comments_On_Comments(r, subreddit, filename, filterz, timing):
    print "loading your comments file"
    try:
        wordfile = open(filename, "r")
        wordbuf = wordfile.readlines()
        wordfile.close()
    except:
        "error loading your comments file"
    for comment in r.subreddit(subreddit).comments():
        body = comment.body.lower()
        print body
        if body.find(filterz) != -1:
            print "matched filter!"
            replo = random.choice(wordbuf)
            comment.reply(replo)
            print str(datetime.datetime.now()) + " posted comment " + replo
            print "sleeping for " + str(timing) + " sec"
            time.sleep(float(timing))


def comment_On_Top_10_Posts(r, subreddit, filename, timing):
    print "loading your comments file"
    try:
        wordfile = open(filename, "r")
        wordbuf = wordfile.readlines()
        wordfile.close()
    except:
        "error loading your comments file"
    for submission in r.subreddit(subreddit).new(limit=10):
        print(submission.title.lower())
        comment = random.choice(wordbuf)
        submission.reply(comment)
        print str(datetime.datetime.now()) + " posted comment " + comment
        print "sleeping for " + str(timing) + " sec"
        time.sleep(float(timing))


def upvote_Post_Filter(r, subreddit, filterz, timing):
    for submission in r.subreddit(subreddit).new(limit=10):
        print(submission.title.lower())
        if filterz in submission.title.lower():
            submission.upvote()
            print str(datetime.datetime.now()) + "upvoted " + submission.title.lower() + " post"
            print "sleeping for " + str(timing) + " sec"
            time.sleep(float(timing))


def downvote_User(r, redditorz, timing):
    # downvote all of a specific users posts
    for submission in r.redditor(redditorz).new(limit=10):
        print(submission.title.lower())
        submission.downvote()
        print str(datetime.datetime.now()) + " downvoted post " + submission.title.lower()
        print "sleeping for " + str(timing) + " sec"
        time.sleep(float(timing))


def upvote_User(r, redditorz, timing):
    # downvote all of a specific users posts
    for submission in r.redditor(redditorz).new(limit=10):
        print(submission.title.lower())
        submission.upvote()
        print str(datetime.datetime.now()) + " upvoted post " + submission.title.lower()
        print "sleeping for " + str(timing) + " sec"
        time.sleep(float(timing))


def troll_User(r, redditorz, filename, timing):
    #  comments on all of a users posts
    print "loading your comments file"
    try:
        wordfile = open(filename, "r")
        wordbuf = wordfile.readlines()
        wordfile.close()
    except:
        "error loading your comments file"
    for submission in r.redditor(redditorz).new(limit=10):
        print(submission.title.lower())
        comment = random.choice(wordbuf)
        submission.reply(comment)
        print str(datetime.datetime.now()) + " posted comment " + comment
        print "sleeping for " + str(timing) + " sec"
        time.sleep(float(timing))


# Main function with options for running script directly
def main():
    #Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                  action='store_const', dest='loglevel',
                  const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                  action='store_const', dest='loglevel',
                  const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                  action='store_const', dest='loglevel',
                  const=5, default=logging.INFO)

    # Option for user for basic auth
    optp.add_option("-c", "--config", dest="config",
                  help="the config file you want to use")

    optp.add_option("-w", "--words", dest="words",
                  help="the text file filled w/ comments you will use")

    optp.add_option("-r", "--redditor", dest="redditorz",
                  help="the redditor to troll")

    optp.add_option("-f", "--filter", dest="filterz",
                  help="the filter to search for")

    optp.add_option("-t", "--time", dest="timing",
                  help="the timing option, defaults to 1 min")

    opts, args = optp.parse_args()
    # Prompt if the user dosn't give a config
    if opts.config is None:
        opts.config = raw_input("what is the name of the config file your using? ")

    if opts.timing is None:
        opts.timing = 60

    # Our main code
    try:
        con = importlib.import_module(opts.config)
    except:
        print "error loading your config file"
        return 1
    r = bot_Login(con)
    subreddit = con.subreddit
    #upvote_User(r, "", opts.timing)
    #downvote_user(r, "", opts.timing)
    #upvote_Post_Filter(r, subreddit, "security", opts.timing)
    if opts.words is not None and opts.filterz is None and opts.redditorz is None:
        comment_On_Top_10_Posts(r, subreddit, opts.words, opts.timing)

    if opts.words is not None and opts.filterz is not None and opts.redditorz is None:
        comments_On_Comments(r, subreddit, opts.words, opts.filterz, opts.timing)

    if opts.words is not None and opts.filterz is None and opts.redditorz is not None:
        troll_User(r, opts.redditorz, opts.words, opts.timing)



if __name__ == '__main__':
    main()
