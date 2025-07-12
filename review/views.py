import os
import markdown
from django.shortcuts import render
from .forms import ResumeReviewForm
from .utils import extract_resume_text
from dotenv import load_dotenv
from openai import OpenAI
from django.utils.safestring import mark_safe
from .embedding_utils import get_embedding, cosine_similarity

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def review_resume(request):
    feedback = None

    if request.method == "POST":
        form = ResumeReviewForm(request.POST, request.FILES)

        if form.is_valid():
            resume_file = form.cleaned_data["resume"]
            job_description = form.cleaned_data["job_description"]

            resume_text = extract_resume_text(resume_file)
            resume_embedding = get_embedding(resume_text)
            job_embedding = get_embedding(job_description)
            similarity_score = cosine_similarity(resume_embedding, job_embedding)

            prompt = f"""
            You are a helpful resume reviewer. Here's how to analyze resumes against job descriptions.

            Example:
            Resume:
            - Experience: Google SWE intern, Python, C++, ML
            Job:
            - Looking for: Python, ML, leadership

            Output:
            ✅ Strengths: Strong ML background, Google intern.
            ⚠️ Gaps: No leadership shown.
            💡 Suggestions: Add leadership experience or impact bullet points.

            Now analyze the following:

            Resume:
            {resume_text}

            Job Description:
            {job_description}
            """


            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )

            feedback = response.choices[0].message.content
            feedback_html = markdown.markdown(feedback, extensions=['extra', 'nl2br'])
            feedback = mark_safe(feedback_html)

    else:
        form = ResumeReviewForm()

    return render(request, "review/form.html", {"form": form, "feedback": feedback, "similarity_score": similarity_score * 100})
