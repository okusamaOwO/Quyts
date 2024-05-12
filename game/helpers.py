import json


def convert_questions_to_json(questions):
    questions_json = []
    for question in questions:
        question_json = {
            "question": question.text,
            "answers": [question.answer1, question.answer2, question.answer3, question.answer4],
            "correct_answer": question.correct_answer
        }
        questions_json.append(question_json)
    return json.dumps(questions_json)
