import random
import textwrap
from typing import Any, Union
from edsl.questions import Question
from edsl.questions.descriptors import IntegerDescriptor, QuestionOptionsDescriptor
from edsl.scenarios import Scenario
from edsl.utilities import random_string


class QuestionBudget(Question):
    """
    QuestionBudget is a question where the user is asked to allocate a budget among options.
    - `budget_sum` is the total amount of the budget, and should be a positive integer.
    - `question_options` is a list of strings

    For an example, run `QuestionBudget.example()`
    """

    question_type = "budget"

    default_instructions = textwrap.dedent(
        """\
        You are being asked the following question: {{question_text}}
        The options are 
        {% for option in question_options %}
        {{ loop.index0 }}: {{option}}
        {% endfor %}                       
        Return a valid JSON formatted as follows, with a dictionary for your "answer"
        where the keys are the option numbers and the values are the amounts you want 
        to allocate to the options, and the sum of the values is {{budget_sum}}:
        {"answer": {<put dict of option numbers and allocation amounts here>},
        "comment": "<put explanation here>"}
        Example response for a budget of 100 and 4 options: 
        {"answer": {"0": 25, "1": 25, "2": 25, "3": 25},
        "comment": "I allocated 25 to each option."}
        There must be an allocation listed for each item (including 0).
        """
    )

    budget_sum: int = IntegerDescriptor(none_allowed=False)
    question_options: list[str] = QuestionOptionsDescriptor()

    def __init__(
        self,
        question_name: str,
        question_text: str,
        question_options: list[str],
        budget_sum: int,
        short_names_dict: dict[str, str] = None,
        instructions: str = None,
    ):
        self.question_name = question_name
        self.question_text = question_text
        self.question_options = question_options
        self.budget_sum = budget_sum
        self.short_names_dict = short_names_dict or dict({})
        self.instructions = instructions or self.default_instructions

    ################
    # Answer methods
    ################
    def validate_answer(self, answer: dict[str, Any]) -> dict[str, Union[int, str]]:
        self.validate_answer_template_basic(answer)
        self.validate_answer_key_value(answer, "answer", dict)
        self.validate_answer_budget(answer)
        return answer

    def translate_answer_code_to_answer(
        self, answer_codes: dict[str, int], scenario: Scenario = None
    ):
        """Translates the answer codes to the actual answers.
        For example, for a budget question with options ["a", "b", "c"],
        the answer codes are 0, 1, and 2. The LLM will respond with 0.
        This code will translate that to "a".
        """
        translated_codes = []
        for answer_code, response in answer_codes.items():
            translated_codes.append({self.question_options[int(answer_code)]: response})

        return translated_codes

    def simulate_answer(self, human_readable=True):
        "Simulates a valid answer for debugging purposes (what the validator expects)"
        if human_readable:
            keys = self.question_options
        else:
            keys = range(len(self.question_options))
        values = [random.randint(0, 100) for _ in range(len(self.question_options))]
        current_sum = sum(values)
        modified_values = [v * self.budget_sum / current_sum for v in values]
        answer = dict(zip(keys, modified_values))
        return {
            "answer": answer,
            "comment": random_string(),
        }

    ################
    # Helpful methods
    ################
    @classmethod
    def example(cls):
        return cls(
            question_name="food_budget",
            question_text="How would you allocate $100?",
            question_options=["Pizza", "Ice Cream", "Burgers", "Salad"],
            budget_sum=100,
        )


def main():
    from edsl.questions.QuestionBudget import QuestionBudget

    q = QuestionBudget.example()
    q.question_text
    q.question_options
    q.question_name
    q.short_names_dict
    q.instructions
    # validate an answer
    q.validate_answer(
        {"answer": {0: 100, 1: 0, 2: 0, 3: 0}, "comment": "I like custard"}
    )
    # translate answer code
    q.translate_answer_code_to_answer({0: 100, 1: 0, 2: 0, 3: 0})
    # simulate answer
    q.simulate_answer()
    q.simulate_answer(human_readable=False)
    q.validate_answer(q.simulate_answer(human_readable=False))
    # serialization (inherits from Question)
    q.to_dict()
    q.from_dict(q.to_dict()) == q
