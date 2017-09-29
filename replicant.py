# author: ahhh
# reddit replicant v0.1

import praw
import time
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
    print "Logged in as: " + config.username
    return r


def comments_on_Comments(r, subreddit, filename, filterz):
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
            print "posted comment " + replo
            print "sleeping 1 min"
            time.sleep(60)   # Sleep for 1 minute


def comment_On_Top10_Posts(r, subreddit, filename):
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
        print "posted comment " + comment
        print "sleeping 1 min"
        time.sleep(60)   # Sleep for 1 minute


def upvote_Post_Filter(r, subreddit, filterz):
    for submission in r.subreddit(subreddit).new(limit=10):
        print(submission.title.lower())
        if filterz in submission.title.lower():
            submission.upvote()
            print "upvoted " + filterz + " post"
            time.sleep(60)   # Sleep for 1 minute
            print "sleeping 1 min"


def downvote_User(r, redditorz):
    # downvote all of a specific users posts
    for submission in r.redditor(redditorz).new(limit=10):
        print(submission.title.lower())
        print submission.downvote()
        print "downvoted post!"
        print "sleeping 1 min"
        time.sleep(60)   # Sleep for 1 minute


def upvote_User(r, redditorz):
    # downvote all of a specific users posts
    for submission in r.redditor(redditorz).new(limit=10):
        print(submission.title.lower())
        print submission.upvote()
        print "upvoted post!"
        print "sleeping 1 min"
        time.sleep(60)   # Sleep for 1 minute


def troll_User(r, redditorz, filename):
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
        print "posted comment " + comment
        print "sleeping 1 min"
        time.sleep(60)   # Sleep for 1 minute


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

    opts, args = optp.parse_args()
    # Prompt if the user dosn't give a config
    if opts.config is None:
        opts.config = raw_input("what is the name of the config file your using? ")

    # Our main code
    try:
        con = importlib.import_module(opts.config)
    except:
        print "error loading your config file"
        return 1
    r = bot_Login(con)
    subreddit = con.subreddit
    #upvote_User(r, "ge_reed_richards")
    #downvote_user(r, "ge_reed_richards")
    #upvote_Post_Filter(r, subreddit, "security")
    if opts.words is not None and opts.filterz is None and opts.redditorz is None:
        comment_On_Top10_Posts(r, subreddit, opts.words)

    if opts.words is not None and opts.filterz is not None and opts.redditorz is None:
        comments_on_Comments(r, subreddit, opts.words, opts.filterz)

    if opts.words is not None and opts.filterz is None and opts.redditorz is not None:
        troll_User(r, opts.redditorz, opts.words)


if __name__ == '__main__':
    main()


