from pydantic import BaseModel
from typing import Optional, Type, Callable
from edsl.questions import Question, QuestionData


class QuestionFunctional(QuestionData):
    """Pydantic data model for QuestionFunctional"""

    question_name: Optional[str] = None
    func: Callable

    # see QuestionFreeText for an explanation of how __new__ works
    def __new__(cls, *args, **kwargs) -> "QuestionFunctionalEnhanced":
        instance = super(QuestionFunctional, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        return QuestionFunctionalEnhanced(instance)

    def __init__(self, **data):
        super().__init__(**data)


class QuestionFunctionalEnhanced(Question):
    """
    A special type of question that's *not* answered by an LLM
    - Instead, it is "answered" by a function that is passed in, `func`.
    - Useful for questions that require some kind of computation first
      or are the result of a multi-step process.
    See `compose_questions` in `compose_functions.py` for an example of how this is used.

    Notes
    - 'func' is a function that takes in a scenario and agent traits and returns an answer.
    - QuestionFunctional is not meant to be instantiated directly by end-users, but rather
      it is meant to be subclassed by us to create new function types.
    - It is probably *not* safe to allow end-users to have the ability to pass functional-derived questions.
      They could monkey-patch the function to do something malicious, e.g., to replace our function logic
      with "os.system('rm -rf /')".
    - One possible solution is to have interfaces they can pass via the API, like so:
      QuestionDropdown(question_name = "dropdown", question_options = ["a", "b", "c"]...)
      which we then translate to the real QuestionFunctional `under the hood.`

    To see how it's used, see `tests/test_QuestionFunctional_construction_from_function`
    """

    question_type = "functional"

    def __init__(self, question: BaseModel):
        super().__init__(question)

    @property
    def instructions(self):
        """Required by Question, but not used by QuestionFunctional"""
        return None

    def answer_question_directly(self, scenario, agent_traits=None):
        return {"answer": self.func(scenario, agent_traits), "comment": None}

    def translate_answer_code_to_answer(self, answer, scenario):
        """Required by Question, but not used by QuestionFunctional"""
        return None

    def construct_answer_data_model(self) -> Type[BaseModel]:
        """Required by Question, but not used by QuestionFunctional"""
        return None

    def form_elements(self) -> str:
        """Required by Question, but not used by QuestionFunctional"""
        raise NotImplementedError

    def simulate_answer(self, human_readable=True) -> dict[str, str]:
        """Required by Question, but not used by QuestionFunctional"""
        raise NotImplementedError