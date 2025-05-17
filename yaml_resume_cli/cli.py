import argparse
from .generate import main as generate_main
from .render import main as render_main

def main():
    parser = argparse.ArgumentParser(prog="resume")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate role‑filtered (and optionally LLM‑refined) YAML")
    gen.add_argument("--role",    required=True)
    gen.add_argument("--job",     help="Path to job description (optional)")
    gen.set_defaults(func=generate_main)

    ren = sub.add_parser("render", help="Render resume YAML to a format")
    ren.add_argument("--role", required=True)
    ren.add_argument("--source", default="resume.yaml", help="Path to reviewed resume YAML")
    ren.add_argument("--format", help="Format to render to")
    ren.add_argument("--out-dir", default=".", help="Output directory")
    ren.set_defaults(func=render_main)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
