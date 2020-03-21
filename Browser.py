import requests
import numpy
import cv2
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://downdetector.com/status/'

class BrowserHandle(object):

	def __init__(self):
		self.prdctOrSrvc = str()

	def brwsr(self, productOrService: str, element_id: str):
		pOS = productOrService.replace(" ", "-")
		if element_id == 'chart-row':   # Graph
			status = requests.get(f'{base_url}{pOS}/').status_code
			if status != 404:
				self._driver_stuff(f'{base_url}{pOS}/', element_id)
			elif status == 404:
				return 404

		elif element_id == 'map':
			status = requests.get(f'{base_url}{pOS}/map/').status_code
			if status != 404:
				self._driver_stuff(f'{base_url}{pOS}/map/', element_id)
			elif status == 404:
				return 404

		elif element_id == 'indicators-card':
			status = requests.get(f'{base_url}{pOS}/').status_code
			if status != 404:
				self._driver_stuff(f'{base_url}{pOS}/', element_id)
			elif status == 404:
				return 404

	def _driver_stuff(self, url: str, element_id: str):
		chromedriver = 'E:\\Program Files (x86)\\ChromeDriver\\chromedriver.exe'
		driver = webdriver.Chrome(chromedriver)
		driver.get(url)
		delay = 10  # seconds

		try:
			WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, element_id)))

			time.sleep(1.5)  # This is used to wait for the ads to load to get a proper screenshot
			element = driver.find_element_by_id(element_id)

			location = element.location
			size = element.size
			nparr = numpy.frombuffer(driver.get_screenshot_as_png(), numpy.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

			left = location['x']
			top = location['y']
			right = location['x'] + size['width']
			bottom = location['y'] + size['height']

			# im = img[left:right, top:bottom]
			im = img[top:int(bottom), left:int(right)]
			cv2.imwrite('filename.png', im)
		except TimeoutException:
			return "Loading took too much time!"
