from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_3_SONNET.value

ClaudeSonnet = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeSonnet"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeSonnet
    q = QuestionMultipleChoice.example()
    m = ClaudeSonnet()
    results = q.by(m).run()
    print(results)