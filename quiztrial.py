from flask import Flask, redirect, url_for, render_template, request, flash
from testdata import *
import random

app =Flask(__name__)
app.config['SECRET_KEY'] = 'testplatform'


#random list of numbers to access data
def shuffle():
 randomlist = []
 for i in range(0,10):
  n = random.randint(0,29)
  if not n in randomlist:
      randomlist.append(n)
      if len(randomlist) == 3:
          break
 return (randomlist)

#load questions and answers into dictionary
def select_questions(chapter_questions_name,chapter_answers_name, randomlist): 
 quiz = []
 for item in randomlist:  
  new_question = (chapter_questions_name[item])
  new_answer = (chapter_answers_name[item])
  quiz.append({'question':new_question, 'answer':new_answer}) 
 return(quiz)

#call all together for data
def prepare_exam(chapter_number_questions, chapter_number_answers):
 order = shuffle()
 quiz_addition = select_questions(chapter_number_questions, chapter_number_answers, order)
 return (quiz_addition)


def final_test():
    final_questions = []
    for i in range(len(chapters)):
        set_of_questions = prepare_exam (chapters[i]['questions'], chapters[i]['answers'])
        for i in range(len(set_of_questions)):
            new_question = set_of_questions[i]['question']
            new_answer = set_of_questions[i]['answer']
            final_questions.append({'question':new_question, 'answer':new_answer})    
    return (final_questions)

question_number = 0
#final = final_test()

@app.route('/', methods = ['POST', 'GET'])
def welcome():
    index = 0
    student_score = 0
    final = final_test()
    number_of_questions = len(final)
    return render_template('welcome.html', questions = final, index = index, student_score = student_score
                           ,total_questions = number_of_questions)

@app.route('/question', methods = ['POST', 'GET'])
def question():
    if request.method == 'POST':
        index_returned = request.form['index_value']
        index = int(index_returned)
        total_returned = request.form["total_questions"]
        total_questions = int(total_returned)
        score_returned = request.form['student_score']
        score = int(score_returned)

        temp = request.form['questions']
        final = list(eval(temp))
        print(index, ' : ', total_questions)
        if index == total_questions:
            print('display final')
            return render_template('final.html', index_value = index, student_score = score)
    return render_template('question.html', questions = final, index_value = index, student_score = score
                           ,total_questions = total_questions)

@app.route('/question/answer', methods = ['POST', 'GET'])
def answer():
    if request.method == 'POST':
        question_returned = request.form['original_question']
        answer_question = request.form['original_answer']
        student_answer = request.form['RadioA']
        index_value = request.form['index_value']
        index = int(index_value)
        student_score = request.form['student_score']
        score = int(student_score)
        total_returned = request.form["total_questions"]
        total_questions = int(total_returned)
        temp = request.form['questions']
        final = list(eval(temp))
        if student_answer == 'e':
            flash('ANSWER IS REQUIRED!!! USE THE BACK BUTTON TO ANSWER QUESTION.')
        else:
            if student_answer == answer_question:
                score += 1
                flash('CORRECT ANSWER')
            else:
                flash('INCORRECT ANSWER')
        return render_template('answer.html', question = question_returned, student = student_answer, correct = answer_question,
                                   student_score = score, index = index, total_questions = total_questions, questions = final)
    
    
@app.route('/final')
def final():
    return render_template('final.html')




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80, debug=True)




