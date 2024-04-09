from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_2_1.value

ClaudeTwoOne = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeTwoOne"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeTwoOne
    q = QuestionMultipleChoice.example()
    m = ClaudeTwoOne()
    results = q.by(m).run()
    print(results)