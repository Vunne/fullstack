from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine

#Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<a href='restaurants/new'><h2>Create new restaurant</h1></a>"
				output += "</br>"
				for restaurant in restaurants:
					output += "%s</br>" % restaurant.name
					output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
					output += "</br>"
					output += "<a href='restaurants/%s/delete'>Delete</a>" % restaurant.id
					output += "</br></br>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Create new restaurant</br>"
				output += """<form method='POST' enctype='multipart/form-data' action='new'>
					<h2>Restaurant name</h2>
					<input name='newRestaurantName' type='text'>
					<input type='submit' value='submit'></form>"""
				output += "<a href='/restaurants'>List of restaurants</a>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "Edit restaurant</br>"
					output += """<form method='POST' enctype='multipart/form-data' action='edit'>
						<h2>Restaurant name</h2>
						<input name='newRestaurantName' type='text'>
						<input type='submit' value='submit'></form>"""
					output += "<a href='/restaurants'>List of restaurants</a>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "Delete restaurant</br>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
					output += "<input type='submit' value='delete'></form>"
					output += "<a href='/restaurants'>List of restaurants</a>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			# self.send_response(301)
			# self.end_headers()
			if self.path.endswith("/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					print 'ADDING RESTAURANT NAME: %s' % fields.get('newRestaurantName')
					newRestaurantName = fields.get('newRestaurantName')[0]
					
				newRestaurant = Restaurant(name = newRestaurantName)
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				return

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					print 'NEW RESTAURANT NAME: %s' % fields.get('newRestaurantName')[0]
				newRestaurantName = fields.get('newRestaurantName')[0]
				restaurantIDPath = self.path.split("/")[2]	
				
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				print 'RESTAURANT TO EDIT:', myRestaurantQuery.name
				if myRestaurantQuery != []:
					myRestaurantQuery.name = newRestaurantName
					session.add(myRestaurantQuery)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]				
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				print 'RESTAURANT TO DELETE: %s' % myRestaurantQuery.name
				if myRestaurantQuery != []:
					session.delete(myRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()