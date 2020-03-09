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


def main():

    # Checking if the supplied json file exists
    if os.path.exists(args.i):
        
        with open(args.i, 'r') as read_file:
            data = json.load(read_file)

            # Here's the json data structure that Bitwarden provides 
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
            names = []

            for element in data['items']:

                # Type 1 is a password entry, Type 2 would be a secure note
                # Generated on mobile is a remnant from LastPass, can skip those
                # Backblaze entry has two urls, TODO: handle that
                if element['type'] == 1 and element['name'] != 'Generated Password on Mobile Device': 

                    # element is a nested dictionary object
                    # This line get's the values for the 'login' key
                    # Then, it gets the values for the username key
                    # Finally, it appends the username to the list created above
                    usernames.append(element.get('login', {}).get('username'))

                    # Do the same for passwords
                    passwords.append(element.get('login', {}).get('password'))

                    # .get('uris') returns a list containing a dictionary
                    # This handles that as well as the NoneType error that is thrown
                    try:
                        for item in element.get('login', {}).get('uris'):
                            urls.append(item['uri'])

                    except TypeError:
                        urls.append('None')
                        continue
                        
                    names.append(element['name'])

            # Debugging print, two newlines for readability 
            #print(f'{usernames}\n\n {passwords}\n\n {urls}\n\n {names}\n\n') 

            # Start the csv writing process. 
            fields = ['name', 'username', 'password', 'url']
            # Zipping the rows to write them as columns
            rows = zip(names, usernames, passwords, urls)

            # This works, however, it gets out of order
            # This is due to an entry having more than one url saved 
            # TODO: fix this 
            # This was towards the end of my list, 
            # so I edited the last few by hand 
            with open(args.o, 'w') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(fields)
                for row in rows:
                    writer.writerow(row)

    else:
        print(f'Supplied input file {args.i} does not exist or we might not have permission to see it. Please try again.')
        sys.exit(1)


if __name__ == '__main__':

    # Handle ^C without throwing an exception
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
        
