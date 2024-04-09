from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_INSTANT_1_2.value

ClaudeInstantOneTwo = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeInstantOneTwo"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeInstantOneTwo
    q = QuestionMultipleChoice.example()
    m = ClaudeInstantOneTwo()
    results = q.by(m).run()
    print(results)