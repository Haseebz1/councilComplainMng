from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dummy database for storing complaints
complaints_db = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    user_complaint = request.json.get('complaint')
    if not user_complaint:
        return jsonify({'error': 'Complaint is required!'}), 400

    try:
        # Use AI to categorize the complaint
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Categorize the following complaint: {user_complaint}",
            max_tokens=50
        )
        category = response.choices[0].text.strip()

        # Save the complaint with category in dummy database
        complaint_entry = {
            'complaint': user_complaint,
            'category': category
        }
        complaints_db.append(complaint_entry)

        return jsonify({'message': 'Complaint submitted successfully!', 'category': category})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/complaints', methods=['GET'])
def get_complaints():
    return jsonify({'complaints': complaints_db})

if __name__ == '__main__':
    app.run(debug=True)
