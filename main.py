import sys, requests, json
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qgui 






class WeatherApp(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.city_label= qtw.QLabel("Enter a City: ", self )
        self.city_input= qtw.QLineEdit(self)
        self. get_weather_btn= qtw.QPushButton("Get Weather", self)
        self.temperature_label= qtw.QLabel(self)
        self.description_label= qtw.QLabel( self)
        self.image_label= qtw.QLabel(self)
        self.setWindowIcon(qgui.QIcon('weatherLogo.png')) 
        self.initUI() 

    def initUI(self):
        self.setWindowTitle("My Weather App")
        self.setGeometry(1500, 500, 400, 600)

        layout= qtw.QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_btn)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.image_label, alignment=qtc.Qt.AlignCenter)
        layout.addWidget(self.description_label)
        
        pixmap= qgui.QPixmap("weatherLogo.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.setLayout(layout)

        self.city_label.setAlignment(qtc.Qt.AlignCenter)
        self.city_input.setAlignment(qtc.Qt.AlignCenter)  
        self.temperature_label.setAlignment(qtc.Qt.AlignCenter) 
        self.description_label.setAlignment(qtc.Qt.AlignCenter)
        #self.image_label.setAlignment(qtc.Qt.AlignCenter)

        self.city_label.setObjectName("city_label") 
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.image_label.setObjectName("image_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                    font-family: CALIBRI, sans-serif;
                    font-size: 30px;
                    font-weight: bold;   
            }             
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_btn {
                font-weight: bold;   
                font-size: 50px;   

            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#description_label {
                font-size: 50px;
                font-style: italic;
            }
            QLabel#image_label {
                max-width: 100px;
                max-height: 100px;
            }
                
        """)

        self. get_weather_btn.clicked.connect(self.get_weather)
          
    def get_weather(self):

            api_key= "Your API key here" 
            city= self.city_input.text()
            url= f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

            try: 
           
                response= requests.get(url)
                response.raise_for_status()
                data= response.json()
                if data.get("cod") == 200:
                    self.display_weather(data)

            except requests.exceptions.HTTPError as http_error :
                    match response.status_code:
                        case 400:   
                           self.display_error("\nBad Request: The server could not understand the request.\n")
                        case 401:
                            self.display_error("\nUnauthorized: Access is denied due to invalid credentials.\n")
                        case 403:
                            self.display_error("\nForbidden: Access is denied.\n")
                        case 404:
                            self.display_error("\nNot Found: City submitted not found.\n")
                        case 500:
                            self.display_error("\nInternal Server Error: The server encountered an error.\n")
                        case 503:   
                            self.display_error("\nService Unavailable: The server is currently unavailable.\n")
                        case 504:
                                self.display_error("\nGateway Timeout: The server did not receive a timely response.\n")
                        case _:
                            self.display_error(f"\nHTTP Error occured: {http_error}\n")

            except requests.exceptions.ConnectionError:
                    self.display_error("\nConnection Error: Failed to connect to the server. \nPlease check your internet connection.\n")
            except requests.exceptions.Timeout:
                    self.display_error("\nTimeout Error: The request timed out. \nPlease try again later.\n")
            except requests.exceptions.TooManyRedirects:
                    self.display_error("\nToo Many Redirects: The request was redirected too many times. \nPlease check the URL.\n")

            except requests.exceptions.RequestException as req_error:
                    self.display_error(f"\nAn error occurred while making the request: {req_error}\n")
                

     
    def display_error(self, error_message):

            self.description_label.setStyleSheet("color: red; font-size: 30px;")
            self.description_label.setText(error_message)
            self.image_label.clear()      
            self.temperature_label.clear()    
     

    def display_weather(self, weather_data):
        
            self.update_image(weather_data["weather"][0]["id"])
            tem_kelvin= weather_data["main"]["temp"]
            tem_fahrenheit= (tem_kelvin - 273.15) * 9/5 + 32
            tem_celsius= tem_kelvin - 273.15 
            self.temperature_label.setText(f"{tem_fahrenheit:.1f} °F / {tem_celsius:.1f} °C")
            self.temperature_label.setStyleSheet("color: green; font-size: 50px;")
            self.description_label.setText(weather_data["weather"][0]["description"])
            self.description_label.setStyleSheet("color: auto; font-size: 50px;")

    
    def update_image(self, weather_code):
           
            if weather_code >= 200 and weather_code < 240:
                pixmap= qgui.QPixmap("storm.png")    
                self.image_label.setPixmap(pixmap)

            elif weather_code >= 300 and weather_code < 502:
                pixmap= qgui.QPixmap("light_rain.png")    
                self.image_label.setPixmap(pixmap)
            
            elif weather_code > 800 and weather_code <= 805:
                pixmap= qgui.QPixmap("cloudy.png")    
                self.image_label.setPixmap(pixmap)

            elif weather_code == 800:
                pixmap= qgui.QPixmap("clear.png")    
                self.image_label.setPixmap(pixmap)

            elif weather_code >= 502 and weather_code < 535:
                pixmap= qgui.QPixmap("rain.png")    
                self.image_label.setPixmap(pixmap)

            elif weather_code >= 600 and weather_code < 625:
                pixmap= qgui.QPixmap("snowy.png")    
                self.image_label.setPixmap(pixmap)

            elif weather_code >= 701 and weather_code < 781:
                pixmap= qgui.QPixmap("bad_weather.png")    
                self.image_label.setPixmap(pixmap)


     
    
        
  
    


       




if __name__ == "__main__":

    app= qtw.QApplication(sys.argv) 
    weatherWidget= WeatherApp() 
    weatherWidget.show()
    sys.exit(app.exec_()) 