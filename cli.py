#!/usr/bin/env python

from config import consumer_key, consumer_secret, access_token_key, access_token_secret
# from config import project_id

import json
import requests
import twitter

import google.auth
from google.cloud import datastore


api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
)

credentials, project_id = google.auth.default()


def display_user(user):
    """Output the information about a user."""
    output = """User: @%s
Created: %s
Name: %s
Bio: %s
Location: %s

Statuses: %s
Favorites: %s
Followers: %s
Friends: %s
"""
    values = (
        user['screen_name'],
        user['created_at'],
        user['name'],
        user['description'],
        user['location'],
        user['statuses_count'],
        user['favourites_count'],
        user['followers_count'],
        user['friends_count'],
    )
    print(output % values)
    # print(json.dumps(user, indent=2, sort_keys=True))


def get_entities(kind):
    """Return a list of entities from datastore."""
    client = datastore.Client(project_id)
    query = client.query(kind=kind)
    return list(query.fetch())


def get_followers():
    """Return a list of followers."""


def get_friends(user):
    """Return a list of friends."""
    client = datastore.Client(project_id)
    friends = []
    for user in api.GetFriends(user):
        user = user.AsDict()
        uid = user['id']
        key = client.key('Friend', uid)
        entity = datastore.Entity(key)
        entity['screen_name'] = user['screen_name']
        for k in user:
            if k in [
                'status',
            ]:
                continue
            entity[k] = user[k]
        friends.append(entity)
    return friends

def update_friends(user):
    """Update friends in datastore."""
    client = datastore.Client(project_id)

    print('Getting friends from Twitter API...')
    twitter_friends = get_friends(user)
    print('Received %s friends from Twitter API.' % (len(twitter_friends)))

    print('Getting friends from Datastore...')
    datastore_friends = get_entities('Friend')
    print('Received %s friends from Datastore.' % (len(datastore_friends)))

    print('Updating friends...')
    # find friends to delete
    batch = client.batch()
    batch.begin()
    for friend in datastore_friends:
        if friend not in twitter_friends:
            print('Delete %s' % (friend.key))
            batch.delete(friend.key)
        if len(batch.mutations) >= 500:
            batch.commit()
            batch = client.batch()
            batch.begin()
    batch.commit()

    # find friends to add
    batch = client.batch()
    batch.begin()
    for friend in twitter_friends:
        if friend not in datastore_friends:
            print('Add %s' % (friend.key))
            batch.put(friend)
        if len(batch.mutations) >= 500:
            batch.commit()
            batch = client.batch()
            batch.begin()
    batch.commit()

def main():
    """Main function."""
    ratelimit = api.InitializeRateLimit()
    print(dir(api))
    user = api.VerifyCredentials()
    display_user(user.AsDict())
    try:
        update_friends(user)
    except twitter.error.TwitterError as e:
        print(e)


if __name__ == "__main__":
    main()
