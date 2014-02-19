import cgi
import re

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_month(month):
    for s in months:
        if s.upper() == month.upper():
            return s

def valid_day(day):
    if day and day.isdigit():
	day = int(day)
	if day > 0 and day < 31:
            return day

def valid_year(year):
    if year and year.isdigit():
	year = int(year)
        if year >= 1950 and year <= 2020:
	    return year

def rot13(to_cipher):
    a = ord('a') - 1
    z = ord('z')
    A = ord('A') - 1
    Z = ord('Z')
    ciphered = ''
    for c in to_cipher:
        if c.isalpha():
            if (ord(c) + 13) > z and c.islower():
                ciphered = ciphered + chr(a + ((ord(c) + 13) - z))
            elif (ord(c) + 13) > Z and c.isupper():
                ciphered = ciphered + chr(A + ((ord(c) + 13) - Z))
            else:
                ciphered = ciphered + chr(ord(c) + 13)
        else:
            ciphered = ciphered + c
    return ciphered

def escape_html(s):
    #for (i,o) in (("&","&amp;"),
    #                ("<","&lt;"),
    #                (">","&gt;"),
    #               ('"',"&quot;")):
    #    s = s.replace(i,o)
    return cgi.escape(s,True)

def valid_username(username):
    return username_re.match(username)

def valid_password(password):
    return password_re.match(password) 

def valid_check(password,pwcheck):
    return password == pwcheck

def valid_email(email):
    return email_re.match(email)
