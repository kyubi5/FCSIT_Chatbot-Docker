# This files contains your custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List

import rasa.core.tracker_store
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict
from rasa_sdk.events import Restarted

class ActionSaveConversation(Action):

    def name(self) -> Text:
        return "action_save_conversation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
         
        conversation=tracker.events
        print(conversation)
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv','w') as file:
                file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
        chat_data=''
        for i in conversation:
            if i['event'] == 'user':
                chat_data+=i['parse_data']['intent']['name']+','+i['text']+','
                print('user: {}'.format(i['text']))
                if len(i['parse_data']['entities']) > 0:
                    chat_data+=i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+','
                    print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                          i['parse_data']['entities'][0]['value'])
                else:
                    chat_data+=",,"
            elif i['event'] == 'bot':
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data+=i['metadata']['utter_action']+','+i['text']+'\n'
                except KeyError:
                    pass
        else:
            with open('chats.csv','a') as file:
                file.write(chat_data)

        return []
    
class ActionCheckCourseEnroll(Action):

    def name(self) -> Text:
        return "action_course_enroll"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        programme = tracker.get_slot('programme_name')
        year = tracker.get_slot('student_year')

        programme = programme.lower()
        
        programme_templates = {
            "software engineering": "SE",
            "computational science": "CS",
            "network computing": "NC",
            "intelligent systems": "IS",
            "multimedia computing": "MC",

        }

        if programme in programme_templates:
            if year in ["1st", "2nd", "3rd", "4th"]:
                template = programme_templates[programme]
                dispatcher.utter_message(response=f"utter_{template}_{year}")
            else:
                dispatcher.utter_message("Sorry, please repeat your programme name and year of study")
        else:
            dispatcher.utter_message("Sorry, please repeat your programme name and year of study")

        return []
    
class ValidateCourseEnrollForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_course_enroll_form"

    @staticmethod
    def programme_db() -> List[Text]:
        """Database of programmes in the faculty"""

        return ["software engineering", "computational science", "intelligent systems", "multimedia computing", "network computing"]

    def validate_programme_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate programme value."""

        if slot_value.lower() in self.programme_db():
            # validation succeeded, set the value of the "programme_name" slot to value
            return {"programme_name": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"programme_name": None}
        
class ActionCheckCoursePrerequisite(Action):

    def name(self) -> Text:
        return "action_course_prerequisite"

    def run(self, dispatcher: CollectingDispatcher,
        
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_to_check = tracker.get_slot("course_name")

        course_prerequisites = {
            "data structure and algorithms": ["Introduction to Programming", "Discrete Mathematics"],
            "object oriented software development": ["Data Structure and Algorithms"],
            "java programming": ["Data Structure and Algorithms"],
            "human centered technology": ["Data Structure and Algorithms"],
            "industrial training": ["Data Structure and Algorithms, Ethics and Professionalism, Project Management","System Analysis and Design"],
            "advanced database management system": ["Database Concept and Design"],
            "final year project": ["Project Management"],
            "computer security": ["Communication and Computer Network"],
            "intelligent systems": ["Data Structure and Algorithms"],
            "computer graphics": ["Data Structure and Algorithms"],
            "distributed system": ["Operating System", "Communication and Computer Network"],
            "automata theory": ["Discrete Mathematics", "Data Structure and Algorithms"],
            "formal methods": ["Data Structure and Algorithms"],
            "software economics": ["Data Structure and Algorithms"],
            "software engineering lab": ["Object Oriented Software Development"],
            "software testing": ["Software Engineering Lab"],
            "software security engineering": ["Software Engineering Lab"],
            "software maintenance and configuration": ["System Analysis and Design", "Object Oriented Software Development"],
            "embedded system": ["Computer Architecture"],
            "internetworking technology lab": ["Communication and Computer Network"],
            "wireless and broadband network": ["Operating System", "Communication and Computer Network"],
            "network performance and simulation": ["Operating System"],
            
        }

        if course_to_check.lower() in course_prerequisites:
            prerequisites = course_prerequisites[course_to_check.lower()]
            dispatcher.utter_message(f"The prerequisites for {course_to_check} are: {', '.join(prerequisites)}")
        else:
            dispatcher.utter_message(f"The course: {course_to_check} has no prerequisites or is an invalid course name. Do refer to the guidebook for latest information")
        
        return []

class ActionCheckCourseFail(Action):

    def name(self) -> Text:
        return "action_course_fail"

    def run(self, dispatcher: CollectingDispatcher,
        
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_to_check = tracker.get_slot("course_name")
        cannot_enroll = []
        course_prerequisites = {
            "data structure and algorithms": ["Introduction to Programming", "Discrete Mathematics"],
            "object oriented software development": ["Data Structure and Algorithms"],
            "java programming": ["Data Structure and Algorithms"],
            "human centered technology": ["Data Structure and Algorithms"],
            "industrial training": ["Data Structure and Algorithms, Ethics and Professionalism, Project Management","System Analysis and Design"],
            "advanced database management system": ["Database Concept and Design"],
            "final year project": ["Project Management"],
            "computer security": ["Communication and Computer Network"],
            "intelligent systems": ["Data Structure and Algorithms"],
            "computer graphics": ["Data Structure and Algorithms"],
            "distributed system": ["Operating System", "Communication and Computer Network"],
            "automata theory": ["Discrete Mathematics", "Data Structure and Algorithms"],
            "formal methods": ["Data Structure and Algorithms"],
            "software economics": ["Data Structure and Algorithms"],
            "software engineering lab": ["Object Oriented Software Development"],
            "software testing": ["Software Engineering Lab"],
            "software security engineering": ["Software Engineering Lab"],
            "software maintenance and configuration": ["System Analysis and Design", "Object Oriented Software Development"],
            "embedded system": ["Computer Architecture"],
            "internetworking technology lab": ["Communication and Computer Network"],
            "wireless and broadband network": ["Operating System", "Communication and Computer Network"],
            "network performance and simulation": ["Operating System"],
            
        }

        if course_to_check.lower() in course_prerequisites:
            for course, prereq_list in course_prerequisites.items():
                if course != course_to_check.lower() and any(prereq.lower() == course_to_check.lower() for prereq in prereq_list):
                    cannot_enroll.append(course)
            if cannot_enroll:
                dispatcher.utter_message(f"You cannot enroll in the following courses if you failed {course_to_check}: {', '.join(cannot_enroll)}")
        else:
            dispatcher.utter_message(f"You can freely enroll in other courses as {course_to_check} is not a prerequisite of other courses.")


        return []
    

class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher,
        
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Chatbot logs and history successfully restarted.")
        return [Restarted()]