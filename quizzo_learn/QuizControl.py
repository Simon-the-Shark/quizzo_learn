# coding=utf-8
"""
quizzo_learn QuizControl
controls queue of questions
"""

from random import sample


class QuizControl(object):
    def __init__(self, dicts_of_questions, practice=True):
        self.dict_of_questions, self.reversed_dict_of_questions = dicts_of_questions
        self.practice = practice

        if self.practice:
            quiz_window.practice = True
            self.start_endless_quiz()
        elif not self.practice:
            quiz_window.practice = False
            self.max_points = len(self.dict_of_questions) + len(self.reversed_dict_of_questions)
            self.current_points = 0
            self.start_test()

    def mix_questions_queue(self):
        keys_list = self.dict_of_questions.keys()
        reversed_keys_list = self.reversed_dict_of_questions.keys()
        mixed_keys_list = sample(keys_list, len(keys_list))
        mixed_reversed_keys_list = sample(reversed_keys_list, len(reversed_keys_list))

        queue = []
        while len(mixed_keys_list) > 0:
            if len(mixed_keys_list) == 1 or len(queue) == 0:
                added = mixed_keys_list.pop(0)
                queue.append(added)
            elif not self.dict_of_questions[mixed_keys_list[0]] == queue[len(queue) - 1]:
                added = mixed_keys_list.pop(0)
                queue.append(added)
            else:
                added = mixed_keys_list.pop()
                queue.append(added)

            if not mixed_reversed_keys_list[0] == self.dict_of_questions[added]:
                queue.append(mixed_reversed_keys_list.pop(0))
            elif len(mixed_reversed_keys_list) == 1:
                queue.append(mixed_reversed_keys_list.pop(0))
            else:
                queue.append(mixed_reversed_keys_list.pop())
                thing_to_flip = mixed_reversed_keys_list.pop(0)
                mixed_reversed_keys_list.append(thing_to_flip)

        return queue

    def start_test(self):
        self.queue = self.mix_questions_queue()
        self.next_question()

    def start_endless_quiz(self):
        self.queue = self.mix_questions_queue()
        self.next_endless_question()

    def next_question(self):
        if len(self.queue) > 0:
            quiz_window.set_question(self.queue.pop(0))
            quiz_window.init_ui()
        else:
            self.end_test()

    def next_endless_question(self):
        if len(self.queue) > 0:
            quiz_window.set_question(self.queue.pop(0))
            quiz_window.init_ui()
        else:
            self.queue = self.mix_questions_queue()
            self.next_endless_question()

    def check(self, question, answer):
        if question in self.dict_of_questions:
            if self.dict_of_questions[question] == answer:
                return [True, ""]
            else:
                good_answer = self.dict_of_questions[question]
                return [False, good_answer]
        if question in self.reversed_dict_of_questions:
            if self.reversed_dict_of_questions[question] == answer:
                return [True, ""]
            else:
                good_answer = self.reversed_dict_of_questions[question]
                return [False, good_answer]

    def end_test(self):
        rating_window.init_ui(self.current_points, self.max_points)

    @staticmethod
    def give_globals(quiz_w, rating_w):
        global quiz_window, rating_window
        quiz_window = quiz_w
        rating_window = rating_w
