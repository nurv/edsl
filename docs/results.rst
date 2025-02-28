.. _results:

Results
=======
A `Results` object is the result of running a survey. 
It is a list of individual `Result` objects, each of which represents a response to a `Survey` for each combination of `Agent`, `Model` and `Scenario` objects used with the survey.
For example, the `Results` of a survey administered to 2 agents and 2 models (with no question scenarios) will contain 4 individual `Result` objects.
If the survey questions are parameterized with 2 scenarios then 8 `Result` objects are generated.

A `Results` object is not typically instantiated directly, but is returned by calling the `run` method of a survey after optionally specifying agents, models and scenarios. 
To see example `Results` we can call the `example` method:

.. code-block:: python

   from edsl import Results

   results = Results.example()

For purposes of showing how to unpack and interact with results, we'll use the following code to generate results for a simply survey:

.. code-block:: python

   # Create questions
   from edsl.questions import QuestionMultipleChoice, QuestionFreeText

   q1 = QuestionMultipleChoice(
      question_name = "yesterday", 
      question_text = "How did you feel yesterday {{ period }}?", 
      question_options = ["Good", "OK", "Terrible"]
   )

   q2 = QuestionFreeText(
      question_name = "tomorrow", 
      question_text = "How do you expect to feel tomorrow {{ period }}?"
   )

   # Optionally parameterize the questions with scenarios
   from edsl import Scenario 

   scenarios = [Scenario({"period": period}) for period in ["morning", "evening"]]

   # Optionally create agents with traits
   from edsl import Agent 

   agents = [Agent(traits = {"status": status}) for status in ["happy", "sad"]]

   # Optionally specify language models
   from edsl import Model 

   models = [Model(model) for model in ['llama-2-70b-chat-hf', 'mixtral-8x7B-instruct-v0.1']]

   # Create a survey with the questions
   from edsl import Survey 

   survey = Survey([q1, q2])

   # Run the survey with the scenarios, agents and models 
   results = survey.by(scenarios).by(agents).by(models).run()

For more details on each of the above steps, please see the relevant sections of the docs.

Result objects 
^^^^^^^^^^^^^^
We can check the number of `Result` objects created by inspecting the length of the `Results`:

.. code-block:: python

   len(results)

This will count 2 (scenarios) x 2 (agents) x 2 (models) = 8 `Result` objects:

   8

We can readily inspect a result:

.. code-block:: python

   results[0]

.. code-block:: text

   Result(
      agent=Agent(traits = {'status': 'happy'}), 
      scenario={'period': 'morning'}, 
      model=Mixtral8x7B(
         model = 'mixtral-8x7B-instruct-v0.1', 
         parameters={'temperature': 0.5, 'top_p': 1, 'top_k': 1, 'max_new_tokens': 2048, 'stopSequences': [], 'use_cache': True}), 
      iteration=1, 
      answer={
         'yesterday': 'Good', 
         'yesterday_comment': 'I felt good yesterday morning, thank you for asking!', 
         'tomorrow': 'I expect to feel happy and refreshed tomorrow morning, ready to start a new day with enthusiasm and positivity!'
         }, 
      prompt={
         'tomorrow_user_prompt': {'text': 'You are being asked the following question: How do you expect to feel tomorrow morning?\nReturn a valid JSON formatted like this:\n{"answer": "<put free text answer here>"}', 'class_name': 'FreeText'}, 
         'tomorrow_system_prompt': {'text': "You are answering questions as if you were a human. Do not break character. You are an agent with the following persona:\n{'status': 'happy'}", 'class_name': 'AgentInstruction'}, 
         'yesterday_user_prompt': {'text': 'You are being asked the following question: How did you feel yesterday morning?\nThe options are\n\n0: Good\n\n1: OK\n\n2: Terrible\n\nReturn a valid JSON formatted like this, selecting only the number of the option:\n{"answer": <put answer code here>, "comment": "<put explanation here>"}\nOnly 1 option may be selected.', 'class_name': 'MultipleChoiceTurbo'}, 
         'yesterday_system_prompt': {'text': "You are answering questions as if you were a human. Do not break character. You are an agent with the following persona:\n{'status': 'happy'}", 'class_name': 'AgentInstruction'}
         }
   )

We can use the `rich_print` method to display the `Result` object in a more readable format:

.. code-block:: python

   results[0].rich_print()

.. code-block:: text

                                                         Result                                                       
   ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Attribute          ┃ Value                                                                                      ┃
   ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ agent              │                                      Agent Attributes                                      │
   │                    │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
   │                    │ ┃ Attribute               ┃ Value                                                        ┃ │
   │                    │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
   │                    │ │ _name                   │ None                                                         │ │
   │                    │ │ _traits                 │ {'status': 'happy'}                                          │ │
   │                    │ │ _codebook               │ {}                                                           │ │
   │                    │ │ _instruction            │ 'You are answering questions as if you were a human. Do not  │ │
   │                    │ │                         │ break character.'                                            │ │
   │                    │ │ set_instructions        │ False                                                        │ │
   │                    │ │ dynamic_traits_function │ None                                                         │ │
   │                    │ │ current_question        │ QuestionFreeText(question_text = 'How do you expect to feel  │ │
   │                    │ │                         │ tomorrow {{ period }}?', question_name = 'tomorrow',         │ │
   │                    │ │                         │ allow_nonresponse = False)                                   │ │
   │                    │ └─────────────────────────┴──────────────────────────────────────────────────────────────┘ │
   │ scenario           │          Scenario Attributes                                                               │
   │                    │ ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓                                                      │
   │                    │ ┃ Attribute ┃ Value                 ┃                                                      │
   │                    │ ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩                                                      │
   │                    │ │ data      │ {'period': 'morning'} │                                                      │
   │                    │ └───────────┴───────────────────────┘                                                      │
   │ model              │                                       Language Model                                       │
   │                    │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
   │                    │ ┃ Attribute                   ┃ Value                                                    ┃ │
   │                    │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
   │                    │ │ model                       │ 'mixtral-8x7B-instruct-v0.1'                             │ │
   │                    │ │ parameters                  │ {'temperature': 0.5, 'top_p': 1, 'top_k': 1,             │ │
   │                    │ │                             │ 'max_new_tokens': 2048, 'stopSequences': [],             │ │
   │                    │ │                             │ 'use_cache': True}                                       │ │
   │                    │ │ temperature                 │ 0.5                                                      │ │
   │                    │ │ top_p                       │ 1                                                        │ │
   │                    │ │ top_k                       │ 1                                                        │ │
   │                    │ │ max_new_tokens              │ 2048                                                     │ │
   │                    │ │ stopSequences               │ []                                                       │ │
   │                    │ │ use_cache                   │ True                                                     │ │
   │                    │ │ api_queue                   │ <queue.Queue object at 0x7f48b86c0400>                   │ │
   │                    │ │ crud                        │ <edsl.data.crud.CRUDOperations object at 0x7f48b2c4c9d0> │ │
   │                    │ │ _LanguageModel__rate_limits │ {'rpm': 10000, 'tpm': 2000000}                           │ │
   │                    │ │ url                         │ 'https://api.deepinfra.com/v1/inference/mistralai/Mixtr… │ │
   │                    │ └─────────────────────────────┴──────────────────────────────────────────────────────────┘ │
   │ iteration          │ 1                                                                                          │
   │ answer             │                                          Answers                                           │
   │                    │ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
   │                    │ ┃ Attribute         ┃ Value                                                              ┃ │
   │                    │ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
   │                    │ │ yesterday         │ 'Good'                                                             │ │
   │                    │ │ yesterday_comment │ 'I felt good yesterday morning, thank you for asking!'             │ │
   │                    │ │ tomorrow          │ 'I expect to feel happy and refreshed tomorrow morning, ready to   │ │
   │                    │ │                   │ start a new day with enthusiasm and positivity!'                   │ │
   │                    │ └───────────────────┴────────────────────────────────────────────────────────────────────┘ │
   │ prompt             │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
   │                    │ ┃ Attribute               ┃ Value                                                        ┃ │
   │                    │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
   │                    │ │ tomorrow_user_prompt    │ {'text': 'You are being asked the following question: How do │ │
   │                    │ │                         │ you expect to feel tomorrow morning?\nReturn a valid JSON    │ │
   │                    │ │                         │ formatted like this:\n{"answer": "<put free text answer      │ │
   │                    │ │                         │ here>"}', 'class_name': 'FreeText'}                          │ │
   │                    │ │ tomorrow_system_prompt  │ {'text': "You are answering questions as if you were a       │ │
   │                    │ │                         │ human. Do not break character. You are an agent with the     │ │
   │                    │ │                         │ following persona:\n{'status': 'happy'}", 'class_name':      │ │
   │                    │ │                         │ 'AgentInstruction'}                                          │ │
   │                    │ │ yesterday_user_prompt   │ {'text': 'You are being asked the following question: How    │ │
   │                    │ │                         │ did you feel yesterday morning?\nThe options are\n\n0:       │ │
   │                    │ │                         │ Good\n\n1: OK\n\n2: Terrible\n\nReturn a valid JSON          │ │
   │                    │ │                         │ formatted like this, selecting only the number of the        │ │
   │                    │ │                         │ option:\n{"answer": <put answer code here>, "comment": "<put │ │
   │                    │ │                         │ explanation here>"}\nOnly 1 option may be selected.',        │ │
   │                    │ │                         │ 'class_name': 'MultipleChoiceTurbo'}                         │ │
   │                    │ │ yesterday_system_prompt │ {'text': "You are answering questions as if you were a       │ │
   │                    │ │                         │ human. Do not break character. You are an agent with the     │ │
   │                    │ │                         │ following persona:\n{'status': 'happy'}", 'class_name':      │ │
   │                    │ │                         │ 'AgentInstruction'}                                          │ │
   │                    │ └─────────────────────────┴──────────────────────────────────────────────────────────────┘ │
   │ raw_model_response │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
   │                    │ ┃ Attribute                    ┃ Value                                                   ┃ │
   │                    │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
   │                    │ │ yesterday_raw_model_response │ {'inference_status': {'runtime_ms': 500, 'cost':        │ │
   │                    │ │                              │ 4.563e-05, 'tokens_generated': 23, 'tokens_input':      │ │
   │                    │ │                              │ 146}, 'results': [{'generated_text': ' {"answer": 0,    │ │
   │                    │ │                              │ "comment": "I felt good yesterday morning, thank you    │ │
   │                    │ │                              │ for asking!"}'}], 'num_tokens': 23, 'num_input_tokens': │ │
   │                    │ │                              │ 146, 'elapsed_time': 1.6693482398986816, 'timestamp':   │ │
   │                    │ │                              │ 1712429824.1722908, 'cached_response': False}           │ │
   │                    │ │ tomorrow_raw_model_response  │ {'inference_status': {'runtime_ms': 747, 'cost':        │ │
   │                    │ │                              │ 3.564e-05, 'tokens_generated': 29, 'tokens_input':      │ │
   │                    │ │                              │ 103}, 'results': [{'generated_text': ' {"answer": "I    │ │
   │                    │ │                              │ expect to feel happy and refreshed tomorrow morning,    │ │
   │                    │ │                              │ ready to start a new day with enthusiasm and            │ │
   │                    │ │                              │ positivity!"}'}], 'num_tokens': 29, 'num_input_tokens': │ │
   │                    │ │                              │ 103, 'elapsed_time': 2.170380115509033, 'timestamp':    │ │
   │                    │ │                              │ 1712429824.6782303, 'cached_response': False}           │ │
   │                    │ └──────────────────────────────┴─────────────────────────────────────────────────────────┘ │
   └────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┘

Results components
^^^^^^^^^^^^^^^^^^
Results contain components that can be accessed and analyzed individually or collectively.
A list of components is displayed by calling the `columns` method:

.. code-block:: python

   results.columns()

The following list will be returned for the results generated by the above code:

.. code-block:: python

   ['agent.agent_name',
   'agent.status',
   'answer.tomorrow',
   'answer.yesterday',
   'answer.yesterday_comment',
   'iteration.iteration', 
   'model.frequency_penalty', 
   'model.logprobs', 
   'model.max_new_tokens', 
   'model.max_tokens', 
   'model.model', 
   'model.presence_penalty', 
   'model.stopSequences', 
   'model.temperature', 
   'model.top_k', 
   'model.top_logprobs', 
   'model.top_p', 
   'model.use_cache', 
   'prompt.tomorrow_system_prompt',
   'prompt.tomorrow_user_prompt',
   'prompt.yesterday_system_prompt',
   'prompt.yesterday_user_prompt',
   'raw_model_response.tomorrow_raw_model_response',
   'raw_model_response.yesterday_raw_model_response',
   'scenario.period']

The columns include information about each *agent*, *model* and corresponding *prompts* that were used to simulate an *answer* to each question in the survey and for any question *scenario*, together with the *raw model response*.

*Agent* information:

* **agent.agent_name**: The name of the agent is a unique identifier that can be passed to the agent when it is created; otherwise, it is added automatically (in the form `Agent_0`, etc.) when results are generated.
* **agent.status**: The code above specified a "status" trait for each of 2 agents. Each agent trait created has its own column in results. (The key for the trait in the traits dict should be a valid Python key.)
For example, if we also specified an agent "persona" there would be a corresponding **agent.persona** column in the results. 

*Answer* information:

* **answer.tomorrow**: The agent's answer to the `tomorrow` question.
* **answer.yesterday**: The agent's answer to the `yesterday` question.
* **answer.yesterday_comment**: An additional comment for the answer to the `yesterday` question.
A comment field is automatically included for every question in a survey other than free text questions, to allow the LLM to optionally provide additional information about its response to the question.

*Model* information:
Each of `model` columns is a modifiable parameter of the model used to generate a response.

* **model.frequency_penalty**: The frequency penalty for the model.
* **model.max_tokens**: The maximum number of tokens for the model.
* **model.model**: The model used.
* **model.presence_penalty**: The presence penalty for the model.
* **model.temperature**: The temperature for the model.
* **model.top_p**: The top p for the model.
* **model.use_cache**: Whether the model uses cache.

*Prompt* information:

* **prompt.tomorrow_system_prompt**: The system prompt for the `tomorrow` question.
* **prompt.tomorrow_user_prompt**: The user prompt for the `tomorrow` question.
* **prompt.yesterday_system_prompt**: The system prompt for the `yesterday` question.
* **prompt.yesterday_user_prompt**: The user prompt for the `yesterday` question.
For more details about prompts, please see the :ref:`prompts` section.

*Raw model response* information:

* **raw_model_response.tomorrow_raw_model_response**: The raw model response for the `tomorrow` question.
* **raw_model_response.yesterday_raw_model_response**: The raw model response for the `yesterday` question.

*Scenario* information:

* **scenario.period**: The values provided for the "period" scenario for the questions.


Creating tables by selecting and printing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each of these columns can be accessed directly by calling the `select` method, and then printed by appending the `print` method.
For example, the following code will print a table showing `answer.yesterday` together with `model.model`, `agent.status` and `scenario.period` columns
(because the column names are unique we can drop the `model`, `agent`, `scenario` and `answer` prefixes when selecting them):

.. code-block:: python

   results.select("model", "status", "period", "yesterday").print()

The following table will be printed:

.. code-block:: text

   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
   ┃ model                      ┃ agent   ┃ scenario ┃ answer     ┃
   ┃ .model                     ┃ .status ┃ .period  ┃ .yesterday ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ evening  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ evening  │ Terrible   │
   └────────────────────────────┴─────────┴──────────┴────────────┘

We can sort the columns by calling the `sort_by` method and passing it the column name to sort by:

.. code-block:: python

   (results
   .sort_by("model", reverse=False)
   .select("model", "status", "period", "yesterday")
   .print()
   )

.. code-block:: text
   
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
   ┃ model                      ┃ agent   ┃ scenario ┃ answer     ┃
   ┃ .model                     ┃ .status ┃ .period  ┃ .yesterday ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
   │ llama-2-70b-chat-hf        │ happy   │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ evening  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ evening  │ Terrible   │
   └────────────────────────────┴─────────┴──────────┴────────────┘

The `sort_by` method can be applied multiple times:

.. code-block:: python

   (results
   .sort_by("model", reverse=False)
   .sort_by("status", reverse=True)
   .select("model", "status", "period", "yesterday")
   .print()
   )

.. code-block:: text
   
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
   ┃ model                      ┃ agent   ┃ scenario ┃ answer     ┃
   ┃ .model                     ┃ .status ┃ .period  ┃ .yesterday ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
   │ llama-2-70b-chat-hf        │ sad     │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ evening  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ morning  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ evening  │ Good       │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ morning  │ Terrible   │
   ├────────────────────────────┼─────────┼──────────┼────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ evening  │ Terrible   │
   └────────────────────────────┴─────────┴──────────┴────────────┘

We can also add some table labels by passing a dictionary to the `pretty_labels` argument of the `print` method:

.. code-block:: python

   (results
   .sort_by("model", reverse=False)
   .sort_by("status", reverse=True)
   .select("model", "status", "period", "yesterday")
   .print(pretty_labels={
      "model": "LLM", 
      "status": "Agent", 
      "period": "Period", 
      "yesterday": q1.question_text
      })
   )

.. code-block:: text
   
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ LLM                        ┃ Agent   ┃ scenario ┃ How did you feel yesterday {{ period }}?   ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ llama-2-70b-chat-hf        │ sad     │ morning  │ Good                                       │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ llama-2-70b-chat-hf        │ sad     │ evening  │ Good                                       │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ morning  │ Terrible                                   │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ llama-2-70b-chat-hf        │ happy   │ evening  │ Terrible                                   │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ morning  │ Good                                       │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ sad     │ evening  │ Good                                       │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ morning  │ Terrible                                   │
   ├────────────────────────────┼─────────┼──────────┼────────────────────────────────────────────┤
   │ mixtral-8x7B-instruct-v0.1 │ happy   │ evening  │ Terrible                                   │
   └────────────────────────────┴─────────┴──────────┴────────────────────────────────────────────┘

Filtering
^^^^^^^^^
Results can be filtered by using the `filter` method and passing it a logical expression identifying the results that should be selected.
For example, the following code will filter results where the answer to `yesterday` is "Good" and then just print the `yesterday_comment` and `tomorrow` columns:

.. code-block:: python

   (results
   .filter("yesterday == 'Good'")
   .select("yesterday_comment", "tomorrow")
   .print()
   )

.. code-block:: text

   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ answer                                                 ┃ answer                                                 ┃
   ┃ .yesterday_comment                                     ┃ .tomorrow                                              ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ I felt good yesterday morning, thank you for asking!   │ I expect to feel happy and refreshed tomorrow morning, │
   │                                                        │ ready to start a new day with enthusiasm and           │
   │                                                        │ positivity!                                            │
   ├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
   │ I woke up feeling refreshed and ready to take on the   │ I expect to feel refreshed and ready to tackle the day │
   │ day!                                                   │ with a positive attitude tomorrow morning!             │
   ├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
   │ I felt good yesterday evening. I had a productive day  │ I expect to feel happy and content tomorrow evening.   │
   │ and was able to help many users with their questions.  │                                                        │
   │ I am looking forward to continuing to assist users     │                                                        │
   │ today!                                                 │                                                        │
   ├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
   │ I'm always happy, so yesterday evening was great!      │ I expect to feel content and fulfilled tomorrow        │
   │                                                        │ evening, with a sense of accomplishment from a         │
   │                                                        │ productive day. I will have had a chance to help many  │
   │                                                        │ people and make a positive impact in their lives,      │
   │                                                        │ which will give me a feeling of purpose and            │
   │                                                        │ satisfaction. I will also have had time to relax and   │
   │                                                        │ unwind, enjoying the company of my loved ones and      │
   │                                                        │ engaging in activities that bring me joy. Overall, I   │
   │                                                        │ am looking forward to a wonderful tomorrow evening!    │
   └────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘

Interacting via SQL
^^^^^^^^^^^^^^^^^^^
We can also interact with the results via SQL using the `sql` method.

.. code-block:: python

   results.sql("select data_type, key, value from self where data_type = 'answer' limit 3", shape="long")



Exporting to other formats
^^^^^^^^^^^^^^^^^^^^^^^^^^
We can also export results to other formats, such as pandas DataFrames or CSV files.
The `to_pandas` method will return a pandas DataFrame:

.. code-block:: python

   results.to_pandas()

For example, here we use it to inspect the first set of (default) prompts used in the results:

.. code-block:: python

   results.to_pandas()[["prompt.tomorrow_user_prompt", "prompt.tomorrow_system_prompt"]].iloc[0]

.. code-block:: text

   prompt.tomorrow_user_prompt    {'text': 'You are being asked the following question: How do you expect to feel tomorrow morning?\nReturn a valid JSON formatted like this:\n{"answer": "<put free text answer here>"}', 'class_name': 'FreeText'}
   prompt.tomorrow_system_prompt  {'text': "You are answering questions as if you were a human. Do not break character. You are an agent with the following persona:\n{'status': 'happy'}", 'class_name': 'AgentInstruction'}
   Name: 0, dtype: object


The `to_csv` method will write the results to a CSV file:

.. code-block:: python

   results.to_pandas().to_csv("results.csv")

The `to_json` method will write the results to a JSON file:

.. code-block:: python

   results.to_pandas().to_json("results.json")



Result class
------------
.. automodule:: edsl.results.Result
   :members: rich_print, 
   :inherited-members:
   :exclude-members: 
   :undoc-members:
   :special-members: __init__

Results class
-------------
.. automodule:: edsl.results.Results
   :members:
   :inherited-members:
   :exclude-members: append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort, known_data_types, Mixins, main
   :undoc-members:
   :special-members: __init__

