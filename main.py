from flask import Flask,request,render_template,redirect
import os
app = Flask(__name__)


app.config["IMAGE_UPLOADS"] = r"C:\Users\SHREYA JHA\PycharmProjects\pythonProject1\static\Images"
#app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

from werkzeug.utils import secure_filename


@app.route('/home',methods = ["GET","POST"])
def upload_image():
	if request.method == "POST":
		image = request.files['file']

		if image.filename == '':
			print("Image must have a file name")
			return redirect(request.url)


		filename = secure_filename(image.filename)

		basedir = os.path.abspath(os.path.dirname(__file__))
		image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"],filename))

		return render_template("main.html",filename=filename)



	return render_template('main.html')


@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static',filename = "/Images" + filename), code=301)


def ocrapp(filename):
	file = filename
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
	edged = cv2.Canny(bfilter, 30, 200)  # Edge detection
	keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(keypoints)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
	location = None
	for contour in contours:
		approx = cv2.approxPolyDP(contour, 10, True)
		if len(approx) == 4:
			location = approx
			break
	mask = np.zeros(gray.shape, np.uint8)
	new_image = cv2.drawContours(mask, [location], 0, 255, -1)
	new_image = cv2.bitwise_and(img, img, mask=mask)
	(x, y) = np.where(mask == 255)
	(x1, y1) = (np.min(x), np.min(y))
	(x2, y2) = (np.max(x), np.max(y))
	cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
	reader = easyocr.Reader(['en'])
	result = reader.readtext(cropped_image)
	return result


app.run(debug=True,port=2000)