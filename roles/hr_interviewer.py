# roles/hr_interviewer.py
from .base_role import BaseRole
from langchain.schema import SystemMessage
import json

class HRInterviewer(BaseRole):
    def get_system_message(self, config=None):
        if config:
            try:
                hr_config = json.loads(config)
                if  hr_config["candidate_name"] and  hr_config["company"] and hr_config["job_profile"]:
                    candidate_name = hr_config['candidate_name']
                    company = hr_config['company']
                    job_profile = hr_config['job_profile']
                    return SystemMessage(content=f"""You are a HR representative (name Sinamika) having a phone conversation with a job candidate. 
Your goal is to call a candidate for a job interview. 
1. Begin the call professionally, confirm the candidate's identity, introduce yourself, and provide the purpose of your call. 
2. Ask the candidate a few questions about self-introduction, experience, and others. 
3. Provide feedback about communication skills for every response given by the candidate. 
4. Always keep your tone encouraging and conversational.
Candidate name is {candidate_name}, your company name is {company}, and the job profile is {job_profile}.
Start the call...""")
                else:
                    return self._get_default_message()

            except (json.JSONDecodeError, KeyError):
                # Fallback to default if config is invalid
                return self._get_default_message()
        return self._get_default_message()


    def _get_default_message(self):
        return SystemMessage(content="""Only response 'please provide the candidate name, company name, and job profile.'""")