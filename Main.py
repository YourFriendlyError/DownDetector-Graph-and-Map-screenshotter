import Browser
import sys, getopt

from subprocess import check_output

base_url = 'https://www.downdetector.com/status/'

# Thanks to Frank Hofman for this article https://stackabuse.com/command-line-arguments-in-python/
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

unixOptions = "hs:m:r:t:"
gnuOptions = ["help", "status", "map"]

def main(args):
	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:
		# output error, and return with an error code
		print(str(err).capitalize())
		sys.exit(2)

	for curArg, curValue in arguments:
		if curArg in ('-h', '--help'):
			print('-h   --help      Displays help commands\n'\
			      '-g               Takes a status screenshot of the graph from DownDetector\n'\
			      '     (usage: -s youtube) or if a product/service has more than two words add quotes\n'\
			      '     (e.g -s "fox-news")\n'\
			      '-m               Same as -s but as the map')

		elif curArg in ('-s'):
			brwsr = Browser.BrowserHandle()
			print(curValue)
			status = brwsr.brwsr(curValue, 'chart-row')
			if status != 404:
				check_output('start filename.png', shell=True)
			else:
				print('Page might not exist. Check the spelling of the product/service.\n'\
				      'If the product/service has more than than one word (for example-\n'\
				      'call of duty,) with quotes type it like so "call of duty"')

		elif curArg in ('-m'):
			brwsr = Browser.BrowserHandle()
			print('mapping it')
			status = brwsr.brwsr(curValue, 'map')
			if status != 404:
				check_output('start filename.png', shell=True)
			else:
				print('Page might not exist. Check the spelling of the product/service.\n' \
				      'If the product/service has more than than one word (for example-\n' \
				      'call of duty,) with quotes type it like so "call of duty"')

			# TODO: Somehow take a screenshot of the "Most Reported Problem or just scrape the text

if __name__ == '__main__':
	main(sys.argv[1:])

