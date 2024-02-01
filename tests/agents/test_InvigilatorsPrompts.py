import pytest
from edsl.enums import LanguageModelType
from edsl.agents.Agent import Agent

# Import other necessary modules and classes

from edsl.prompts.Prompt import Prompt
from edsl.prompts.registry import get_classes
from edsl.exceptions import QuestionScenarioRenderError
from edsl.prompts.registry import get_classes

from edsl.agents.Invigilator import InvigilatorAI


class MockModel:
    model = LanguageModelType.GPT_4.value


class MockQuestion:
    question_type = "free_text"
    question_text = "How are you feeling?"
    question_name = "feelings_question"
    data = {
        "question_name": "feelings",
        "question_text": "How are you feeling?",
        "question_type": "feelings_question",
    }


# Assuming get_classes and InvigilatorAI are defined elsewhere in your codebase
# from your_module import get_classes, InvigilatorAI


@pytest.fixture
def mock_model():
    return MockModel()


@pytest.fixture
def mock_question():
    return MockQuestion()


def test_invigilator_ai_no_trait_template(mock_model, mock_question):
    applicable_prompts = get_classes(
        component_type="question_instructions",
        question_type=mock_question.question_type,
        model=mock_model.model,
    )

    a = Agent(
        instruction="You are a happy-go lucky agent.",
        traits={"feeling": "happy", "age": "Young at heart"},
        codebook={"feeling": "Feelings right now", "age": "Age in years"},
        trait_presentation_template="",
    )

    i = InvigilatorAI(
        agent=a,
        question=mock_question,
        scenario={},
        model=mock_model,
        memory_plan=None,
        current_answers=None,
    )

    assert i.get_prompts()["system_prompt"].text == "You are a happy-go lucky agent."


def test_invigilator_ai_with_trait_template(mock_model, mock_question):
    a = Agent(
        instruction="You are a happy-go lucky agent.",
        traits={"feeling": "happy", "age": "Young at heart"},
        codebook={"feeling": "Feelings right now", "age": "Age in years"},
        trait_presentation_template="You are feeling {{ feeling }}.",
    )

    i = InvigilatorAI(
        agent=a,
        question=mock_question,
        scenario={},
        model=mock_model,
        memory_plan=None,
        current_answers=None,
    )

    assert (
        i.get_prompts()["system_prompt"].text
        == "You are a happy-go lucky agent. You are feeling happy."
    )


def test_invigilator_ai_with_incomplete_trait_template(mock_model, mock_question):
    a = Agent(
        instruction="You are a happy-go lucky agent.",
        traits={"feeling": "happy", "age": "Young at heart"},
        codebook={"feeling": "Feelings right now", "age": "Age in years"},
        trait_presentation_template="You are feeling {{ feeling }}. You eat lots of {{ food }}.",
    )

    i = InvigilatorAI(
        agent=a,
        question=mock_question,
        scenario={},
        model=mock_model,
        memory_plan=None,
        current_answers=None,
    )

    # Assuming QuestionScenarioRenderError is a specific exception you expect
    with pytest.raises(QuestionScenarioRenderError):
        i.get_prompts()["system_prompt"]


# Add more test functions as needed