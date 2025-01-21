# chat_manager.py
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from roles.hr_interviewer import HRInterviewer
from roles.english_teacher import EnglishTeacher
from roles.jd_interviewer import JDInterviewer
from dotenv import load_dotenv

class ChatManager:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.chat_histories = {}
        self.roles = {
            'hr_interviewer': HRInterviewer(),
            'english_teacher': EnglishTeacher(),
            'jd_interviewer': JDInterviewer()
        }
    
        
    def get_response(self, session_id, role, user_text, config=None):
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = {
                'messages': [self.roles[role].get_system_message(config)]
            }

        # Add user message to chat history
        self.chat_histories[session_id]['messages'].append(
            HumanMessage(content=user_text)
        )
        
        # Get AI response
        result = self.model.invoke(self.chat_histories[session_id]['messages'])
        response = result.content if result and hasattr(result, 'content') else "I apologize, but I couldn't generate a response."
        
        # Add AI response to chat history
        self.chat_histories[session_id]['messages'].append(
            AIMessage(content=response)
        )
        
        return response