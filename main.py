#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:ufuncts.escape_html(//www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import ufuncts

welcome = """
<h1>Welcome %(username)s!</h1>
"""

signup_form ="""
<h1>Signup</h1>
<form method="post">
<div>
    <label>Username<input type="text" name="username" value="%(username)s"></label><span>%(error_u)s</span>
</div>
<div>
    <label>Password<input type="password" name="password" ></label><span>%(error_pw)s</span>
</div>
<div>
    <label>Verify password<input type="password" name="verify" ></label><span>%(error_check)s</span>
</div>
<div>
    <label>Email<input type="text" name="email" value="%(email)s"></label><span>%(error_email)s</span>
</div>
<div>
    <input type="submit">
</div>
</form>
"""

form_rot13 = """
<form method="post">
<h1>Enter some text to ROT13</h1>
    <br>
    <textarea name="text">%(cipher)s</textarea>
    <br>
    <input type="submit">
</form>
"""

form = """
<form method="post">
	What is your birthday?
	<br>
	<label> Month
		<input type="text" name="month" value="%(month)s">
	</label>
	<label> Day
		<input type="text" name="day" value="%(day)s">
	</label>
	<label> Year
		<input type="text" name="year" value="%(year)s">
        </label>
        <div style="color: red">%(error)s</div>
	<br>
	<br>
	<input type="submit">
</form>
"""
class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error":error,
                                        "month":ufuncts.escape_html(month),
                                        "day":ufuncts.escape_html(day),
                                        "year":ufuncts.escape_html(year)})
    def get(self):
        self.write_form()
    def post(self):
	user_day = (self.request.get('day'))
	user_year =(self.request.get('year'))
	user_month = (self.request.get('month'))

        month = ufuncts.valid_month(user_month)
        day = ufuncts.valid_day(user_day)
        year = ufuncts.valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend",user_month,user_day,user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
	self.response.out.write("Thanks! That's a totally valid day!")

class Rot13(webapp2.RequestHandler):
    def write_form(self,cipher=''):
        self.response.out.write(form_rot13 % {"cipher":cipher})
    def get(self):
        self.write_form()
    def post(self):
        cipher_text = (self.request.get('text'))
        ciphered_text = ufuncts.rot13(cipher_text)
        ciphered_text = ufuncts.escape_html(ciphered_text)
        self.write_form(ciphered_text)

class Signup(webapp2.RequestHandler):
    def write_form(self,username='',password='',verify='',email=''):
        error_u = ''
        error_pw = ''
        error_check = ''
        error_email = ''
        success = True
        if(not ufuncts.valid_username(username)):
            success = False
            error_u = "That's not a valid username!"
        if(not ufuncts.valid_password(password)):
            success = False
            error_pw = "That's not a valid password!"
        if(not ufuncts.valid_check(password,verify)):
            success = False
            error_check = "These passwords do not match"
        if(not ufuncts.valid_email(email) and not email == ''):
            success = False
            error_email = "That's not a valid email address!"
        if(success):
            self.redirect("/welcome?username=%(username)s" % {'username':username})
        self.response.out.write(signup_form % {'error_u':error_u,'error_pw':error_pw,'error_check':error_check,'error_email':error_email,'username':username,'email':email})

    def get(self):
        self.response.out.write(signup_form % {'error_u':'','error_pw':'','error_check':'','error_email':'','username':'','email':''})
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
       #self.response.out.write(welcome % {'username':username})
        self.write_form(username,password,verify,email)

class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(welcome % {'username':self.request.get('username')})

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/thanks',ThanksHandler),
                               ('/rot13',Rot13),
                               ('/signup',Signup),
                               ('/welcome',Welcome)],debug=True)
