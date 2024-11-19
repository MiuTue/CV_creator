from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import openai

app = Flask(__name__, template_folder='app/template')
UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openai.api_key = 'your-api-key-here'

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        job_title = request.form.get("job_title")
        contact = request.form.get("contact")
        email = request.form.get("email")
        address = request.form.get("address")
        personal_statement = request.form.get("personal_statement")
        skills = request.form.getlist("skills")
        experience = request.form.get("experience")
        education = request.form.get("education")
        photo = request.files.get("photo")

        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Save photo
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)

        # Render CV
        return render_template(
            "cv_format.html",
            name=name,
            job_title=job_title,
            contact=contact,
            email=email,
            address=address,
            personal_statement=personal_statement,
            skills=skills,
            experience=experience,
            education=education,
            photo=filename if photo else None,
        )
    return render_template("form.html")
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Pass the filename to the template
            return render_template('cv_format.html', photo=filename)
        
@app.route('/api/virtual_therapist', methods=['POST'])
def virtual_therapist():
    data = request.json
    user_input = data['input']
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Bạn là một nhà tư vấn và hướng dẫn làm cv cũng như là profile xin việc, đưa ra lời khuyên hữu ích. Hãy trả lời một cách tự nhiên, dễ hiểu như một người bạn bằng ngôn ngữ nói không có phải liệt kê và bằng tiếng Việt."},
            {"role": "user", "content": user_input}
        ]
    )
    
    # Access the content of the response correctly
    reply = response.choices[0].message.content
    
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
