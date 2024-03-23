import textwrap

from edsl.prompts.QuestionInstructionsBase import QuestionInstuctionsBase


class Image(QuestionInstuctionsBase):
    """Image question type."""

    question_type = "image"
    model = "gpt-4-vision-preview"
    default_instructions = textwrap.dedent(
        """\
        Using the input images respond to this question {{question_text}}.
        {% if sub_type == "checkbox" %}
            The options are
            {% for option in question_options %}
            {{ loop.index0 }}: {{ option }}
            {% endfor %}
            Return a valid JSON formatted like this, selecting only the number of the option:
            {"answer": [<put comma-separated list of answer codes here>], "comment": "<put explanation here>"}
        {% else %}
            Return a valid JSON formatted like this:
            {"answer": "<put free text answer here>"}
        {% endif %}
        """
    )
