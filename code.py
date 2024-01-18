import time
import smbus2
from gpiozero import MCP3008, DigitalInputDevice, RGBLED
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import PCF8591 as ADC

GPIO.setmode(GPIO.BCM)

bus = smbus2.SMBus(1)

# Configuration du convertisseur analogique-numérique PCF8591
PCF8591_I2C_ADDR = 0x48

# Configurations des broches
PIN_VIBRATION = 17  # Broche numérique pour le capteur de vibration
RGB_LED_PINS = {'rouge': 18, 'vert': 27, 'bleu': 22}  # Broches GPIO pour la LED RVB
GPIO.setup(PIN_VIBRATION, GPIO.IN)

# Initialisation des périphériques
led_rgb = RGBLED(red=RGB_LED_PINS['rouge'], green=RGB_LED_PINS['vert'], blue=RGB_LED_PINS['bleu'])

# Initialisation de l'écran LCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)  # Utiliser la bonne adresse I2C

# Fonction de détection de vibration
def detecter_vibration(channel):
	print("Vibration détectée !")
	afficher_sur_lcd("\nVibration détectée !")
	time.sleep(1)

# Fonction pour lire le capteur de son
def lire_capteur_son():
 	# Lire la valeur analogique du capteur de son à l'aide du PCF8591
	with smbus2.SMBus(1) as bus:
    	bus.write_byte(PCF8591_I2C_ADDR, 0)  # En supposant que le capteur de son est connecté à la voie 0
    	time.sleep(0.1)  # Laisser un peu de temps pour la conversion
    	return bus.read_byte(PCF8591_I2C_ADDR)

# Fonction pour afficher un message sur l'écran LCD
def afficher_sur_lcd(message):
	lcd.clear()
	lcd.write_string(message)
	time.sleep(1)
	lcd.clear()

# Fonction pour mettre à jour la couleur de la LED RVB
def mettre_a_jour_led_rgb(couleur):
	led_rgb.color = couleur



# Ajouter un détecteur d'événements pour la broche de vibration
GPIO.add_event_detect(PIN_VIBRATION, GPIO.RISING, callback=detecter_vibration)

def main():
	try:
    	while True:
        	niveau_son = lire_capteur_son()
        	message_lcd = f"NiveauSonore:{niveau_son}"
        	afficher_sur_lcd(message_lcd)

        	if niveau_son >= 100:
            	mettre_a_jour_led_rgb((1, 0, 1))  # vert pour des niveaux sonores normaux
            	afficher_sur_lcd(f"NiveauSonore:{niveau_son}")
            	print(niveau_son)
#         	elif 50 < niveau_son < 120:
#             	mettre_a_jour_led_rgb((0, 0.75, 1))  # Orange pour un son un peu élevé
#             	afficher_sur_lcd(f"Niveau sonore: \n {niveau_son}")
#             	print(niveau_son)
        	else:
            	mettre_a_jour_led_rgb((0, 1, 1))
            	afficher_sur_lcd(f"Niveau Sonore:{niveau_son}")  # rouge pour un son élevé
            	print(niveau_son)
except KeyboardInterrupt:
    	print("Programme terminé par l'utilisateur.")
	finally:
    	GPIO.remove_event_detect(PIN_VIBRATION)
    	GPIO.cleanup()

if __name__ == "__main__":
	main()
