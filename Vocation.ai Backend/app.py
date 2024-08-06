from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import os
import re
import json
import traceback
import logging
import ast
import re

app = Flask(__name__)

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    api_key = "YOUR_API_KEY"

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

chat_history = []
student_memory = {
    "strengths": [],
    "weaknesses": [],
    "topics_covered": [],
    "learning_style": []
}

@app.route('/')
def home():
    return render_template('TutorAI.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')

        global chat_history
        chat_history.append(f"Student: {user_message}")
        
        system_prompt = """
            System Prompt removed to avoid plagiarism
        """
        
        conversation_history = "\n".join(chat_history)
        full_prompt = f"{system_prompt}\n{conversation_history}\n\nTeacher:"
        
        response = model.generate_content(full_prompt)
        print(response)
        
        memory_match = re.search(r'\[STUDENT_MEMORY\](.*?)\[/STUDENT_MEMORY\]', response.text, re.DOTALL)
        if memory_match:
            memory_data = eval(memory_match.group(1))
            for key in student_memory:
                student_memory[key].extend(memory_data.get(key, []))
                student_memory[key] = list(set(student_memory[key]))
        
        quiz_match = re.search(r'\[QUIZ\](.*?)\[/QUIZ\]', response.text, re.DOTALL)
        if quiz_match:
            quiz_data = json.loads(quiz_match.group(1))
            return jsonify({
                "message": "Prompt removed to avoid plagiarism",
                "quiz_data": quiz_data
            })
        
        cleaned_response = re.sub(r'\[STUDENT_MEMORY\].*?\[/STUDENT_MEMORY\]', '', response.text, flags=re.DOTALL)

        chat_history.append(f"Teacher: {cleaned_response}")
        return jsonify({
            "message": cleaned_response.strip(),
            "student_memory": student_memory
        })
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/quiz')
def quiz():
    return render_template('QuizAI.html')

@app.route('/job_ai')
def job_ai():
    return render_template('JobAI.html')

job_ai_chat_history = []

@app.route('/resume_generator')
def resume_generator():
    return render_template('resume_generator.html')

@app.route('/api/autofill', methods=['POST'])
def autofill():
    data = request.json
    field = data['field']
    content = data['content']

    prompt = f"System Prompt removed to avoid plagiarism"
    
    response = model.generate_content(prompt)
    autofilled_content = response.text.strip()

    return jsonify({"autofilled_content": autofilled_content})

@app.route('/api/job_ai_chat', methods=['POST'])
def job_ai_chat():
    global job_ai_chat_history
    try:
        data = request.json
        user_message = data.get('message')

        job_ai_chat_history.append(f"User: {user_message}")

        if "resume" in user_message.lower():
            return jsonify({"message": "Sure, I can help you generate a resume. Please click <a href='/resume_generator'>here</a> to use our Resume Generator AI"})
        if "interview" in user_message.lower():
            return jsonify({"message": "Sure, I can help you generate your interview. Please click <a href='/interview_ai'>here</a> to try our Interview AI"})

        system_prompt = """
            System Prompt removed to avoid plagiarism
        """

        conversation_history = "\n".join(job_ai_chat_history[-10:])
        full_prompt = f"{system_prompt}\n\nConversation history:\n{conversation_history}\n\nJob AI:"

        response = model.generate_content(full_prompt)
        ai_response = response.text.strip()
        
        job_ai_chat_history.append(f"Job AI: {ai_response}")
        
        return jsonify({"message": ai_response})
    except Exception as e:
        app.logger.error(f"Error in job_ai_chat endpoint: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/interview_ai')
def interview_ai():
    return render_template('interview_ai.html')

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/generate_questions', methods=['POST'])
def generate_questions():
    try:
        data = request.json
        job_title = data.get('jobTitle')
        job_description = data.get('jobDescription')

        if not job_title or not job_description:
            return jsonify({"error": "Job title and description are required"}), 400

        prompt = f"""
        System Prompt removed to avoid plagiarism
        """

        try:
            response = model.generate_content(prompt)
            logging.debug(f"Model response: {response.text}")

            cleaned_response = re.sub(r'```python\n|```\n?', '', response.text).strip()
            logging.debug(f"Cleaned response: {cleaned_response}")

            questions = ast.literal_eval(cleaned_response)
            
            if not isinstance(questions, list) or len(questions) != 3:
                raise ValueError("Invalid response format from model")

            return jsonify({"questions": questions})
        except (SyntaxError, ValueError) as e:
            logging.error(f"Failed to parse model response: {cleaned_response}")
            logging.error(f"Error: {str(e)}")
            return jsonify({"error": "Failed to parse model response"}), 500

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/grade_answer', methods=['POST'])
def grade_answer():
    try:
        data = request.json
        question = data.get('question')
        answer = data.get('answer')

        if not question or not answer:
            return jsonify({"error": "Question and answer are required"}), 400

        prompt = f"""
            System Prompt removed to avoid plagiarism
        """

        response = model.generate_content(prompt)
        logging.debug(f"Model response: {response.text}")

        cleaned_response = re.sub(r'```json\n|```', '', response.text).strip()

        try:
            result = json.loads(cleaned_response)
            if not isinstance(result, dict) or 'score' not in result or 'feedback' not in result:
                raise ValueError("Invalid response format from model")

            result['score'] = 1 if result['score'] == 1 else 0

            return jsonify(result)
        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Failed to parse model response: {cleaned_response}")
            logging.error(f"Error: {str(e)}")
            return jsonify({"error": "Failed to parse model response"}), 500

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/api/clear_context', methods=['POST'])
def clear_context():
    global chat_history, student_memory
    chat_history = []
    student_memory = {
        "strengths": [],
        "weaknesses": [],
        "topics_covered": [],
        "learning_style": []
    }
    return jsonify({"message": "Chat context cleared successfully"})

@app.route('/api/clear_context_jobai', methods=['POST'])
def clear1_context():
    global job_ai_chat_history, student_memory
    job_ai_chat_history = []
    return jsonify({"message": "Chat context cleared successfully"})

if __name__ == '__main__':
    app.run(debug=True)