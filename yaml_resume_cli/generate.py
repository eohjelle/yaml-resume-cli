#!/usr/bin/env python3
import yaml
from pathlib import Path
import importlib.resources as pkg_res
from openai import OpenAI
import os
from pydantic import BaseModel

def process(resume, role):
    """Process the resume for the given role."""
    # Name and contact are not lists and are always relevant
    result = {k: resume[k] for k in ("name", "contact")}

    for section in resume:
        if section in ("name", "contact"):
            continue
        new_section = []
        for entry in resume[section]:
            if any(t in entry["tags"] for t in ["all", role]):
                new_section.append(entry)
        result[section] = new_section
    return result

# Helper class for the LLM response
class LLMResponse(BaseModel):
    explanation_of_changes: str
    yaml_resume: str

def refine_with_llm(resume, role, job_description):
    """Refine the resume with the job description using an LLM."""
    system_prompt = (
        "You are a resume assistant. "
        "Given a YAML resume and a job description, refine the resume to highlight the most relevant experience and skills for the job. "
        "Feel free to reorganize or rename the entries, and reorganize information between bullet points. "
        "But do not make up any new information, and try to limit the number of bullet points within each entry to 3. "
        "Preserve the original structure of the resume; do not make up any new sections. "
        "Return only valid YAML; put quotes around all items to avoid YAML errors related to special characters. "
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("Refining resume with LLM...")
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Resume: {resume}\nJob description: {job_description}"}
        ],
        text_format=LLMResponse
    )
    content = response.output_parsed
    if content is None:
        raise ValueError("Failed to get response from OpenAI.")
    print("Explanation: ", content.explanation_of_changes)
    try:
        yaml_content = yaml.safe_load(content.yaml_resume)
    except Exception as e:
        raise ValueError(f"OpenAI returned invalid YAML: {content}\n\nError: {e}")
    return yaml_content

def main(args):
    role = args.role
    job_path = args.job

    # Load master resume
    master_resume_text = pkg_res.read_text("yaml_resume_cli", "resume.yaml")
    master_resume = yaml.safe_load(master_resume_text)

    # Process the master resume
    processed_resume = process(master_resume, role)

    # If job description path is provided, refine the resume with the job description
    if job_path:
        refined_resume = refine_with_llm(processed_resume, role, Path(job_path).read_text())
        Path("original.resume.yaml").write_text(yaml.dump(processed_resume, sort_keys=False))
        Path("resume.yaml").write_text(yaml.dump(refined_resume, sort_keys=False))
    else:
        Path("resume.yaml").write_text(yaml.dump(processed_resume, sort_keys=False))