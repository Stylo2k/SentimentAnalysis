# get the following args from the command line:
# -c, --classifier, the classifier(s) to use
# -t, --text, the text to classify
# -f, --file, the file to classify
# -co, --compare, the file to compare
# -u, --url, the url of the sentiment analysis server
# -h, --help, the help message


import argparse
import requests, sys, json

def parse_args():
    parser = argparse.ArgumentParser(description='Sentiment Analysis')
    parser.add_argument('-c', '--classifier', type=str, help='the classifier(s) to use')
    parser.add_argument('-t', '--text', type=str, help='the text to classify')
    parser.add_argument('-f', '--file', type=str, help='the file to classify')
    parser.add_argument('-co', '--compare', type=str, help='the file to compare')
    parser.add_argument('-u', '--url', type=str, help='the url of the sentiment analysis server')
    args = parser.parse_args()
    return args


def do_request(url, data):
    response = requests.post(url, json=data)
    return response.json()

def main():
    args = parse_args()
    if not args.url:
        print("Url not provided: taking http://127.0.0.1:8000", file=sys.stderr)
        url = "http://127.0.0.1:8000"
    else:
        url = args.url
    data = {}
    if args.classifier:
        # check whether it is a list
        if ',' in args.classifier:
            url += '/multiple'
            data['classifiers'] = args.classifier.split(',')
        else:
            data['classifier'] = args.classifier
    if args.text:
        data['text'] = [args.text]
    if args.file:
        # read the file and put it in data['text']
        f = open(args.file, "r")
        data['text'] = f.read()
    if args.compare:
        # add /compare to the url
        url += '/compare'
    
    print(json.dumps(do_request(url, data), indent=4, sort_keys=True))
    



if __name__ == '__main__':
    main()