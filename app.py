from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import pdfkit
import os
import mimetypes

app = Flask(__name__)
CORS(app) 

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    convert_to_pdf = request.args.get('convertToPDF')
    isFile = request.args.get('file')
    
    if isFile:
        isFile = int(isFile)
    else:
        isFile = 0

    if isFile:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            }
            response = requests.get(url, headers=headers, stream=True)
            print(response)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the file extension
                file_extension = os.path.splitext(url)[1]
                filename = "downloaded_file" + file_extension
                with open(filename, 'wb') as file:
                    file.write(response.content)
                
                mime_type = mimetypes.guess_type(url)[0]
                response = send_file(filename, mimetype=mime_type, as_attachment=True)
            
            else:
                response = 'Unable to fetch the file', 500
            
            os.remove(filename)

            return response

        except Exception as e:
            return str(e), 500

    else:    
    # Convert convertToPDF parameter to integer
        if convert_to_pdf:
            convert_to_pdf = int(convert_to_pdf)
        else:
            convert_to_pdf = 0
        
        if convert_to_pdf == 1:
            # Convert URL to PDF and save as 'output.pdf'
            pdfkit.from_url(url, 'output.pdf')

            # Send the generated PDF as file
            response = send_file('output.pdf', mimetype='application/pdf')
            os.remove('output.pdf')
            return response
        else:
            response = requests.get(url)
            return response.content

if __name__ == '__main__':
    app.run(port=5000)
