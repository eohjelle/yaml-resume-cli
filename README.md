# YAML Resume CLI

A command-line interface for generating and rendering your resume from YAML format.

This is not so much a package as a simple template for streamlining the process of anything having to do with resumes:

- Keep a single "master resume" with all your information in a YAML file.
- Generate resumes for different roles from the master resume using a single command.
- Use an LLM to further refine a role-specific resume for specific job descriptions. Manually go over all changes made.
- Render the resume to any format using customizable templates.

See my [blog post](https://eohjelle.com/posts/yaml-resume/) for more information.

## Example workflow

You found a job application for a woodworking position that you want to apply for. So you create a new folder called `woodworking-job-application` somewhere on your system. Inside this folder you create a file called `job-description.txt` where you paste a copy of the job description. Then you run

```zsh
resume generate --role woodworking --job job-description.txt
```

The above command creates two files in the `woodworking-job-application` folder:

- `original.resume.yaml`, your "original" woodworking resume, and
- `resume.yaml`, a refined version of the "original" created with the help of an LLM using the job description.

(You can choose to not pass the optional `--job` parameter if you don't want to use the LLM feature, in which case the `resume generate` command will only generate the "original" resume as `resume.yaml`.)

You can then look over the resume. I recommend using a diff to compare the "original" and "refined" resumes. Since the refined version is made by an LLM it's important to make sure that all the details are factually correct.

Once you're happy with `resume.yaml`, run the command

```zsh
resume render --role woodworking
```

to render the resume using your pre-made templates.

## Technical setup and usage

After cloning the repository, run

```zsh
pip install -e .
```

to make the `resume generate` and `resume render` commands available.
Keep an eye on the output from pip; you may have to add a certain location to PATH to make it work.

If you want to use the LLM feature by passing the `--job` parameter to `resume generate`, make sure to set `OPENAI_API_KEY`.

Modify the "master resume" `yaml_resume_cli/resume.yaml` and jinja2 templates located in `yaml_resume_cli/templates` according to your needs.
