"""
Рендеринг страниц через Jinja2.
Простейшая обёртка для рендеринга шаблонов с контекстом.
"""

from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import os


def create_jinja_env(template_dir: str):
    """Создаёт и возвращает Environment Jinja2."""
    loader = FileSystemLoader(template_dir)
    env = Environment(loader=loader, autoescape=True)
    return env


def render_template(env: Environment, template_name: str, context: Dict[str, Any]) -> str:
    """Рендерит шаблон и возвращает строку HTML."""
    template = env.get_template(template_name)
    return template.render(**context)