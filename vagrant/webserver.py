from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are your sure you want to delete "
                    output += myRestaurantQuery.name
                    output += " ?</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    # output += "<input name='restaurantID' type='text' placeholder = '%s' >" % myRestaurantQuery.id
                    output += "<input type= 'submit' value='Delete'>"
                    output += "</form>"
                    self.wfile.write(bytearray(output, 'utf8'))
                    print(output)
                    return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'> " % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type= 'submit' value='Rename'>"
                    output += "</form>"
                    self.wfile.write(bytearray(output, 'utf8'))
                    print(output)
                    return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<br><br><a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                for restaurant in restaurants:
                    output += "<br>" + restaurant.name + " <a href = '/restaurants/" + str(
                        restaurant.id) + "/edit'>Edit</a> <a href = '/restaurants/" + str(restaurant.id) + "/delete'>Delete</a></br>"
                output += "</body></html>"
                self.wfile.write(bytearray(output, 'utf8'))
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Make a new restaurant"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input " \
                          "name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'> </form> "
                output += "</body></html>"
                self.wfile.write(bytearray(output, 'utf8'))
                print(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you 
                like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form> '''
                output += "</body></html>"
                self.wfile.write(bytearray(output, 'utf8'))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola <a href = '/hello'>Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you 
                like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form> '''
                output += "</body></html>"
                self.wfile.write(bytearray(output, 'utf8'))
                print(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')[0].decode('utf-8')

                # Create new Restaurant class
                newRestaurant = Restaurant(name=messagecontent)
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')[0].decode('utf-8')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    assert isinstance(messagecontent, object)
                    myRestaurantQuery.name = messagecontent
                    print(myRestaurantQuery.name)
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                # messagecontent = fields.get('restaurantID')[0].decode('utf-8')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    # assert isinstance(messagecontent, object)
                    # myRestaurantQuery.name = messagecontent
                    # print(myRestaurantQuery.name)
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers['Content-type'])
            # if ctype == 'multipart/form-data':
            #     pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')[0].decode('utf-8')
            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me
            # to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form> '''
            # output += "</body></html>"
            # self.wfile.write(output.encode('utf8'))
            # print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
