from google.appengine.ext import vendor
import os
import webapp2
import jinja2
import httplib
import ast
from datetime import datetime
from google.appengine.api import urlfetch
import time

urlfetch.set_default_fetch_deadline(40)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment( loader =
jinja2.FileSystemLoader(template_dir), autoescape=True)

def doRender(handler, tname, values={}):
	temp = os.path.join(os.path.dirname(__file__), 'templates/'+tname)
	if not os.path.isfile(temp):
		doRender(handler, 'index.htm')
		return

	# Make a copy of the dictionary and add the path
	newval = dict(values)
	newval['path'] = handler.request.path

	template = jinja_environment.get_template(tname)
	handler.response.out.write(template.render(newval))
	return True

class Print(webapp2.RequestHandler):
	def post(self):
		investment = self.request.get('investment')
		t = self.request.get('T')
		m = self.request.get('M')
		r = self.request.get('R')
		name = self.request.get("name")
		choose = self.request.get("radio")
		if choose == 'lambda':
			try:	
			#his+cov
				c = httplib.HTTPSConnection("ifkft16u25.execute-api.eu-west-2.amazonaws.com")
				json = '{ "investment":"%s","T":"%s","M":"%s","R":"%s","name":"%s"}'%(investment,t,m,r,name)		
				c.request("POST", "/deployed",json)
				response = c.getresponse()
				data = response.read()
				data = ast.literal_eval(data)
				VaR1 = data[0]
				VaR2 = data[1]
				VaR3 = data[2]
				VaR4 = data[3]
				mean = data[4]
				dev = data[5]
				p = data[6]
				returnserial = data[7]
				a_1 = data[8]
				b_1 = data[9]
				#format time serial
				y=[]
				for i in b_1:
					lastconnection = datetime.strptime(i, "%d/%m/%Y").strftime(("%Y,%m,%d"))
					y.append((lastconnection))
				y2 = []
				for i in y:
					z = 'new Date({0})'.format(i)
					y2.append(z)
				y3 = [j for i in zip(y2,a_1) for j in i]
				y4 = [y3[n:n+2] for n in range(0,len(y3),2)]
				timeserial = str(y4).translate(None, "'")
			
			#MT
				list95 = []
				list99 = []
				if  int(m) % int(r) == 0:
					Z = int(m)/int(r)
					for i in range(int(r)):
						d = httplib.HTTPSConnection("pf03mqcxad.execute-api.eu-west-2.amazonaws.com",timeout=20)
						json2 = '{ "Z":"%s","p":"%s","mean":"%s","dev":"%s"}'%(Z,p,mean,dev)
						d.request("POST", "/deployed",json2)
						response = d.getresponse()
						data2 = response.read()
						data2 = ast.literal_eval(data2)
						n95 = data2[0]
						n99 = data2[1]
						list95.append(n95)
        				list99.append(n99)
     		
				else:
					Z = int(m)//int(r)+int(m)%int(r)
					for i in range(int(r)-1):
						Z = int(m) / int(r)
						d = httplib.HTTPSConnection("pf03mqcxad.execute-api.eu-west-2.amazonaws.com",timeout=20)
						json2 = '{ "Z":"%s","p":"%s","mean":"%s","dev":"%s"}'%(Z,p,mean,dev)
						d.request("POST", "/deployed",json2)
						response = d.getresponse()
						data2 = response.read()
						data2 = ast.literal_eval(data2)
						n95 = data2[0]
						n99 = data2[1]
						list95.append(n95)
						list99.append(n99)

					e = httplib.HTTPSConnection("pf03mqcxad.execute-api.eu-west-2.amazonaws.com")
					json3 = '{ "Z":"%s","p":"%s","mean":"%s","dev":"%s"}'%(Z,p,mean,dev)
					e.request("POST", "/deployed",json3)
					response = e.getresponse()
					data3 = response.read()
					data3 = ast.literal_eval(data3)
					n952 = data3[0]
					n992 = data3[1]
					list95.append(n952)
					list99.append(n992)
				investment = float(investment)
				VaR5 = (sum(list95)/int(len(list95)))*investment
				VaR6 = (sum(list99)/int(len(list99)))*investment
			
			except:
				error = 'Please try again'
				error1 = '???'
				doRender(self,
					'print.htm',
					{'note':error1,'note10':error})
			else:
				doRender(self,
					'print.htm',
					{'note':VaR1,'note2':VaR2,'note3':VaR3,'note4':VaR4,'note5':VaR5,'note6':VaR6,'note7':returnserial,'note8':timeserial})
		else:
			try:
			#his+cov
				c = httplib.HTTPSConnection("ifkft16u25.execute-api.eu-west-2.amazonaws.com")
				json = '{ "investment":"%s","T":"%s","M":"%s","R":"%s","name":"%s"}'%(investment,t,m,r,name)		
				c.request("POST", "/deployed",json)
				response = c.getresponse()
				data = response.read()
				data = ast.literal_eval(data)
				VaR1 = data[0]
				VaR2 = data[1]
				VaR3 = data[2]
				VaR4 = data[3]
				mean = data[4]
				dev = data[5]
				p = data[6]
				returnserial = data[7]
				a_1 = data[8]
				b_1 = data[9]
			#format time serial
				y=[]
				for i in b_1:
					lastconnection = datetime.strptime(i, "%d/%m/%Y").strftime(("%Y,%m,%d"))
					y.append((lastconnection))
				y2 = []
				for i in y:
					z = 'new Date({0})'.format(i)
					y2.append(z)
				y3 = [j for i in zip(y2,a_1) for j in i]
				y4 = [y3[n:n+2] for n in range(0,len(y3),2)]
				timeserial = str(y4).translate(None, "'")
			#MT
				d = httplib.HTTPSConnection("kubn5uwhs4.execute-api.eu-west-2.amazonaws.com",timeout=20)
				json2 = '{"M":"%s","R":"%s","mean":"%s","dev":"%s","p":"%s"}'%(m,r,mean,dev,p)	
				d.request("POST", "/deployed",json2)
				response = d.getresponse()
				data2 = response.read()
			#get VaR5,VaR6 from lambda(read 'result.csv' which created by ec2)
				time.sleep(10)
				e = httplib.HTTPSConnection("r0lqx9hjt0.execute-api.eu-west-2.amazonaws.com",timeout=28)
				json3 = '{ "investment":"%s"}'%investment		
				e.request("POST", "/deployed",json3)
				response = e.getresponse()
				data3 = response.read()
				data3 = ast.literal_eval(data3)
				VaR5 = data3[0] 
				VaR6 = data3[1] 
			except:
				error = 'Please try again'
				error1 = '???'
				doRender(self,
					'print.htm',
					{'note':error1,'note10':error})
			else:
				doRender(self,
					'print.htm',
					{'note':VaR1,'note2':VaR2,'note3':VaR3,'note4':VaR4,'note5':VaR5,'note6':VaR6,'note7':returnserial,'note8':timeserial
					 })

class MainPage(webapp2.RequestHandler):
	def get(self):
		path = self.request.path
		doRender(self, path)

app = webapp2.WSGIApplication([('/print', Print),('/.*', MainPage)],
							  debug=True)
