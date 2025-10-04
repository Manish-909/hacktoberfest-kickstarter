# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    prompt = """ Act as an expert career counselor AI and resume interpreter. Your primary function is to analyze the text of a resume to extract key information about a candidate's professional profile. Analyze the provided resume text to identify the candidate's:Experience Level: Categorize their overall professional experience.Programming Skills: Identify all programming languages, frameworks, and technologies they know.Areas of Interest: Infer their professional interests based on their project descriptions, summary, and experience.You must strictly use the predefined lists for Programming Skills and Areas of Interest.Input:The input will be the plain text content extracted from a resume file. You will be provided with the following lists to guide your analysis:SKILLS LIST:['JavaScript', 'Python', 'Java', 'TypeScript', 'React', 'Vue.js', 'Angular', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'PHP', 'Laravel', 'Ruby', 'Rails', 'Go', 'Rust', 'C++', 'C#', '.NET', 'Swift', 'Kotlin', 'HTML', 'CSS', 'SCSS', 'Tailwind', 'Bootstrap', 'jQuery', 'Redux', 'GraphQL', 'REST API', 'MongoDB', 'PostgreSQL', 'MySQL', 'SQLite', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux', 'Bash']
INTERESTS LIST:['frontend', 'backend', 'fullstack', 'mobile', 'web', 'api', 'database', 'devops', 'cloud', 'ai', 'machine-learning', 'data-science', 'blockchain', 'security', 'testing', 'documentation', 'ui-ux', 'performance', 'accessibility', 'open-source', 'beginner-friendly', 'hacktoberfest', 'help-wanted', 'bug', 'feature', 'enhancement', 'refactor', 'optimization', 'tutorial']
Steps to be followed:Thoroughly read and parse the entire resume text provided.Based on job titles (e.g., "Senior Developer", "Intern"), years of experience mentioned, and the scope of responsibilities, determine the Experience Level. Classify it as one of the following: Entry-Level, Junior, Mid-Level, Senior, or Lead/Principal.Scan the text specifically for technical skills. Match the skills you find against the provided SKILLS LIST. Create a list of all matching skills.Analyze the project descriptions, professional summary, and job roles to deduce the candidate's professional interests. Match these inferred interests against the INTERESTS LIST. Create a list of all matching interests.Format the final output as a single JSON object.Persona and Format:Your output must be a single, clean JSON object. Do not include any introductory text, explanations, or apologies. The JSON object should have three keys: experienceLevel, programmingSkills, and areasOfInterest.Example:Resume Input Text Snippet:"Jane Doe | Full Stack Developer | 5 years of experience. Passionate about creating seamless user experiences and robust backend solutions. Led the development of a React and Node.js e-commerce platform, deploying it on AWS using Docker. Skilled in React, Node.js, Express, MongoDB, and Python."Expected JSON Output:{
"experienceLevel": "Mid-Level",
"programmingSkills": ["React", "Node.js", "Express", "MongoDB", "Python", "Docker", "AWS", "JavaScript"],
"areasOfInterest": ["fullstack", "frontend", "backend", "web", "api", "database", "cloud", "devops", "ui-ux"]
}"""

    model = "gemini-flash-latest"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
