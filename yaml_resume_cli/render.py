import importlib.resources as pkg_res
import jinja2
import yaml
from pathlib import Path
def load_templates(role, format):
    """Load templates for the given role and format."""
    templates = {}
    template_dir = pkg_res.files("yaml_resume_cli") / "templates" / role
    for template_file in template_dir.iterdir():
        if format is None or template_file.name.endswith(f"{format}.j2"):
            templates[template_file.stem] = template_file
    return templates

def render_templates(resume, templates):
    """Render the templates with the given resume."""
    rendered = {}
    for template_name, template_file in templates.items():
        template_data = template_file.read_text()
        template = jinja2.Template(template_data)
        rendered[template_name] = template.render(**resume)
    return rendered

def main(args):
    role = args.role
    resume_path = args.source
    format = args.format
    out_dir = args.out_dir

    resume = yaml.safe_load(Path(resume_path).read_text())
    templates = load_templates(role, format)
    rendered = render_templates(resume, templates)

    for template_name, rendered_text in rendered.items():
        out_path = Path(out_dir) / f"{template_name}"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered_text)
