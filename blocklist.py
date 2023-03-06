'''
bloklist.py

This file just contain the blocklist of the JWT Tokens. It will be imported by app
and the logout resource so that token can be added to the blocklist when the user logs out.
'''

BLOCKLIST=set()

