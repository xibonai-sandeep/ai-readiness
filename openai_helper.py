import os
from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_questions(industry, size, country):
    prompt = f"""Generate 15 questions for an AI readiness assessment for a {size} company in the {industry} industry located in {country}. 
    The questions should cover the following areas:
    1. AI Strategy and Leadership
    2. Data Infrastructure and Management
    3. AI/ML Capabilities and Talent
    4. Ethical AI and Governance
    5. AI Integration and Innovation

    For each question, provide:
    1. A clear, concise question text that is specific to the company's size, industry, and location
    2. A brief explanation of why this question is important in the context of AI readiness
    3. The type of question (scale, multiple-choice, or open-ended)
    4. The impact level of this question (high, medium, or low) on overall AI readiness
    5. For multiple-choice questions, provide 4-5 options that reflect varying levels of AI maturity

    Guidelines for creating questions:
    - Tailor questions to the specific industry, considering unique challenges and opportunities
    - Adjust the complexity based on the company size (e.g., more sophisticated for larger companies)
    - Consider regional factors that might influence AI adoption in the given country
    - Include a mix of technical and non-technical questions to assess overall organizational readiness
    - Ensure questions are actionable and provide insights for improvement

    Format the output as a JSON string with a list of question objects, each containing the following fields:
    - question_text
    - explanation
    - type
    - impact_level
    - options (for multiple-choice questions only)

    Example structure:
    [
      {{
        "question_text": "...",
        "explanation": "...",
        "type": "scale|multiple-choice|open-ended",
        "impact_level": "high|medium|low",
        "options": ["...", "...", "...", "..."] // Only for multiple-choice
      }},
      // ... more questions ...
    ]"""

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")

        # Print the raw content for debugging
        print("Raw OpenAI response:")
        print(content)

        # Remove any markdown formatting if present
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            questions_data = json.loads(content)
            # Check if the response is a dictionary with a 'questions' key
            if isinstance(questions_data, dict) and 'questions' in questions_data:
                questions = questions_data['questions']
            # Check if the response is already a list of questions
            elif isinstance(questions_data, list):
                questions = questions_data
            else:
                raise ValueError("Unexpected JSON structure")

            # Normalize the question structure and validate question types
            normalized_questions = []
            for q in questions:
                question_text = q.get("question", q.get("question_text", ""))
                if not question_text:
                    continue  # Skip questions without text

                question_type = q.get("type", "").lower()
                if question_type not in ["scale", "multiple-choice", "open-ended"]:
                    question_type = "open-ended"  # Default to open-ended if type is invalid

                normalized_q = {
                    "question_text": question_text,
                    "explanation": q.get("explanation", q.get("importance", "")),
                    "type": question_type,
                    "impact_level": q.get("impact_level", ""),
                    "options": q.get("options", []) if question_type == "multiple-choice" else []
                }
                normalized_questions.append(normalized_q)

            return normalized_questions
        except json.JSONDecodeError as json_error:
            print(f"JSON decoding error: {str(json_error)}")
            raise ValueError(f"Invalid JSON response from OpenAI: {str(json_error)}")
    except Exception as e:
        print(f"Error in generate_questions: {str(e)}")
        raise Exception(f"Error generating questions: {str(e)}")

def generate_recommendations(answers, company_info):
    prompt = f"""Based on the following AI readiness assessment answers for a {company_info['size']} company in the {company_info['industry']} industry located in {company_info['country']}, provide 5 detailed recommendations to improve their AI readiness:

    Assessment Answers:
    {answers}

    For each recommendation, include:
    1. Action: A specific action the company should take
    2. Rationale: Why this action is important
    3. Benefits: The potential benefits of implementing this recommendation
    4. Challenges: Potential challenges or obstacles in implementing this recommendation
    5. Example: A brief example or case study of a company that successfully implemented a similar action
    6. Timeline: An estimated timeline for implementation (e.g., short-term, medium-term, long-term)
    7. Key Performance Indicators: 2-3 KPIs to measure the success of this recommendation

    Format the output as a JSON string with a list of recommendation objects."""

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")

        # Print the raw content for debugging
        print("Raw OpenAI response:")
        print(content)

        # Remove any markdown formatting if present
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            recommendations = json.loads(content)
            return recommendations
        except json.JSONDecodeError as json_error:
            print(f"JSON decoding error: {str(json_error)}")
            raise ValueError(f"Invalid JSON response from OpenAI: {str(json_error)}")
    except Exception as e:
        print(f"Error in generate_recommendations: {str(e)}")
        raise Exception(f"Error generating recommendations: {str(e)}")


def generate_ai_readiness_score(answers, company_info):
    prompt = f"""Based on the following AI readiness assessment answers for a {company_info['size']} company in the {company_info['industry']} industry located in {company_info['country']}, provide:
    1. An overall AI readiness score on a scale of 0-100
    2. A detailed explanation of the score, including key factors that influenced it
    3. Scores for each of the 5 focus areas (AI Strategy and Leadership, Data Infrastructure and Management, AI/ML Capabilities and Talent, Ethical AI and Governance, AI Integration and Innovation) on a scale of 0-100
    4. Key strengths and areas for improvement, with actionable insights for each
    5. A projected AI readiness score in 12 months if the company implements the recommended improvements
    6. Potential risks and opportunities based on the current AI readiness level
    7. Relevant specific examples of AI use cases based on the organization's current AI readiness scores, and compare them with ideal scenarios
    8. Insights on developing stronger AI policies, strategies, and frameworks based on the assessment results
    9. Recommendations for future AI readiness assessment, including potential areas for improvement and actionable steps

    Assessment Answers:
    {answers}

    Consider industry-specific factors, company size, and country-specific regulations when analyzing the AI readiness.
    Provide deep, critical analysis of the user's scores and rich insights for improving AI readiness.
    Include specific recommendations for developing stronger AI policies, strategies, and frameworks.
    Provide detailed comparisons between current AI use cases and ideal scenarios based on the readiness scores.

    Format the output as a JSON string with keys for 'overall_score', 'explanation', 'area_scores', 'strengths', 'improvement_areas', 'projected_score', 'risks', 'opportunities', 'ai_use_cases', 'policy_strategy_insights', and 'recommendations for future'."""

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500,
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")

        # Print the raw content for debugging
        print("Raw OpenAI response:")
        print(content)

        # Remove any markdown formatting if present
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            ai_readiness_result = json.loads(content)
            return ai_readiness_result
        except json.JSONDecodeError as json_error:
            print(f"JSON decoding error: {str(json_error)}")
            raise ValueError(f"Invalid JSON response from OpenAI: {str(json_error)}")
    except Exception as e:
        print(f"Error in generate_ai_readiness_score: {str(e)}")
        raise Exception(f"Error generating AI readiness score: {str(e)}")
