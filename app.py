from flask import Flask, render_template, request, flash, redirect, url_for

import re
import smtplib
import dns.resolver


app= Flask(__name__)


@app.route('/',methods=["GET","POST"])
def index():
	fromAddress = 'sagu7065@gmail.com'

	regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

	if request.method == "POST":
		mail= request.form['mail']

		if not mail:
			flash('Please enter the email address')

			return redirect(url_for("index"))

		match = re.match(regex, mail)
		if match == None:
			print('Bad Syntax')
			raise ValueError('Bad Syntax')

		# Get domain for DNS lookup
		splitAddress = mail.split('@')
		domain = str(splitAddress[1])
		print('Domain:', domain)

		# MX record lookup
		records = dns.resolver.query(domain, 'MX')
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)


		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
		server.mail(fromAddress)
		code, message = server.rcpt(str(mail))
		server.quit()

		#print(code)
		#print(message)

		# Assume SMTP response 250 is success

		if code == 250:
			print('Success')
		else:
			print('Bad')

		return render_template('index.html', email= code)

	return render_template('index.html')


if __name__ == "__main__":
	app.run(debug=True)