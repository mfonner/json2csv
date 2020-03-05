#!/usr/bin/env python3

import sys
import json
import csv
import argparse
import os

# Gathering args
parser = argparse.ArgumentParser(
        description='A script to convert a given json file to csv.')

parser.add_argument('-i', 
        help='json file to be converted. Note this will not overwrite the given file.')

parser.add_argument('-o',
        help='Output file to write as a csv.')

args = parser.parse_args()


def json_print(obj):
    
    # Prints json neatly
    print(json.dumps(obj, indent=4, sort_keys=True))


def main():

    # Checking if the supplied json file exists
    if os.path.exists(args.i):
        
        with open(args.i, 'r') as read_file:
            data = json.load(read_file)

            # TODO: Filter through the data for:
            '''
	        "login": {
        	    "uris": [
          	    {
            	        "match": null,
            	        "uri": "URL HERE"
          	    }
                ],
            "username": "VALUE",
            "password": "VALUE"
            '''
          
            # Initializing empty lists before looping through json file
            usernames = []
            passwords = []
            urls = []
            for element in data['items']:

                # element is a nested dictionary object
                # This line get's the values for the 'login' key
                # Then, it gets the values for the username key
                # Finally, it appends the username to the list created above
                usernames.append(element.get('login', {}).get('username'))

                # Do the same for passwords
                passwords.append(element.get('login', {}).get('password'))

                # TODO: Get URLs
                # It appears that .get('uris') returns a list
                # Need to find a way to get the 'uri' value from that
                print(element.get('login', {}).get('uris', {}).get('uri'))


    else:
        print(f'Supplied input file {args.i} does not exist or we might not have permission to see it. Please try again.')
        sys.exit(1)


if __name__ == '__main__':

    # Handle ^C without throwing an exception
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
        
