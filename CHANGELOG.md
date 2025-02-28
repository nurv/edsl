# Changelog

## Unreleased

## [0.1.0] - 2023-12-20
### Added
- Base feature

## [0.1.1] - 2023-12-24
### Added
- Changelog file

### Fixed
- Image display and description text in README.md

### Removed
- Unused files

## [0.1.4] - 2024-01-22
### Added
- Support for several large language models
- Async survey running
- Asking for API keys before they are used

### Fixed
- Bugs in survey running
- Bugs in several question types 

### Removed
- Unused files
- Unused package dependencies

## [0.1.5] - 2024-01-23

### Fixed
- Improvements in async survey running

## [0.1.6] - 2024-01-24

### Fixed
- Improvements in async survey running

## [0.1.7] - 2024-01-25

### Fixed
- Improvements in async survey running
- Added logging

## [0.1.8] - 2024-01-26

### Fixed
- Better handling of async failures
- Fixed bug in survey logic

## [0.1.9] - 2024-01-27

### Added
- Report functionalities are now part of the main package.

### Fixed
- Fixed a bug in the Results.print() function

### Removed
- The package no longer supports a report extras option.
- Fixed a bug in EndofSurvey

## [0.1.11] - 2024-02-01

### Added
- 

### Fixed
- Question options can now be 1 character long or more (down from 2 characters)
- Fixed a bug where prompts displayed were incorrect (prompts sent were correct)

### Removed
- 

## [0.1.12] - 2024-02-12

### Added
- Results now provides a `.sql()` method that can be used to explore data in a SQL-like manner.
- Results now provides a `.ggplot()` method that can be used to create ggplot2 visualizations.
- Agent now admits an optional `name` argument that can be used to identify the Agent.

### Fixed
- Fixed various issues with visualizations. They should now work better.

### Removed

## [0.1.13] - 2024-03-01

### Added
- The `answer` component of the `Results` object is printed in a nicer format.

### Fixed
- `trait_name` descriptor was not working; it is now fixed.
- `QuestionList` is now working properly again

### Removed

## [0.1.14] - 2024-03-06

### Added
- The raw model response is now available in the `Results` object, accessed via "raw_model_response" keyword. 
There is one for each question. The key is the question_name + `_raw_response_model`
- The `.run(progress_bar = True)` returns a much more informative real-time view of job progress.

### Fixed

### Removed

## [0.1.15] - 2024-03-09

### Added

### Fixed
- Various fixes and small improvements

### Removed


## [0.1.16] - TBD

### Added
- <b>New documentation:</b> https://docs.expectedparrot.com

- <b>Progress bar:</b> 
You can now pass `progress_bar=True` to the `run()` method to see a progress bar as your survey is running. Example:
```
from edsl import Survey 
results = Survey.example().run(progress_bar=True)

                            Job Status                             
                                                                   
  Statistic                                            Value       
 ───────────────────────────────────────────────────────────────── 
  Elapsed time                                         1.1 sec.    
  Total interviews requested                           1           
  Completed interviews                                 1           
  Percent complete                                     100 %       
  Average time per interview                           1.1 sec.    
  Task remaining                                       0           
  Estimated time remaining                             0.0 sec.    
  Model Queues                                                     
  gpt-4-1106-preview;TPM (k)=1200.0;RPM (k)=8.0                    
  Number question tasks waiting for capacity           0           
   new token usage                                                 
   prompt_tokens                                       0           
   completion_tokens                                   0           
   cost                                                $0.00000    
   cached token usage                                              
   prompt_tokens                                       104         
   completion_tokens                                   35          
   cost                                                $0.00209    
```

- <b>New language models</b>: 
We added new models from Anthropic and Databricks. To view a complete list of available models see <a href="https://docs.expectedparrot.com/en/latest/enums.html#edsl.enums.LanguageModelType">edsl.enums.LanguageModelType</a> or run:
```python
from edsl import Model
Model.available()
```
This will return:
```python
['claude-3-haiku-20240307', 
'claude-3-opus-20240229', 
'claude-3-sonnet-20240229', 
'dbrx-instruct', 
'gpt-3.5-turbo',
'gpt-4-1106-preview',
'gemini_pro',
'llama-2-13b-chat-hf',
'llama-2-70b-chat-hf',
'mixtral-8x7B-instruct-v0.1']
```
For instructions on specifying models to use with a survey see new documentation on <a href="https://docs.expectedparrot.com/en/latest/language_models.html">Language Models</a>.
<i>Let us know if there are other models that you would like us to add!</i>

### Changed
- <b>Cache:</b> 
We've improved user options for caching LLM calls. 

<i>Old method:</i>
Pass a `use_cache` boolean parameter to a `Model` object to specify whether to access cached results for the model when using it with a survey (i.e., add `use_cache=False` to generate new results, as the default value is True).

<i>How it works now:</i>
All results are (still) cached by default. To avoid using a cache (i.e., to generate fresh results), pass an empty `Cache` object to the `run()` method that will store everything in it. This can be useful if you want to isolate a set of results to share them independently of your other data. Example:
```
from edsl.data import Cache
c = Cache() # create an empty Cache object

from edsl.questions import QuestionFreeText
results = QuestionFreeText.example().run(cache = c) # pass it to the run method

c # inspect the new data in the cache
```
We can inspect the contents:
```python
Cache(data = {‘46d1b44cd30e42f0f08faaa7aa461d98’: CacheEntry(model=‘gpt-4-1106-preview’, parameters={‘temperature’: 0.5, ‘max_tokens’: 1000, ‘top_p’: 1, ‘frequency_penalty’: 0, ‘presence_penalty’: 0, ‘logprobs’: False, ‘top_logprobs’: 3}, system_prompt=‘You are answering questions as if you were a human. Do not break character. You are an agent with the following persona:\n{}’, user_prompt=‘You are being asked the following question: How are you?\nReturn a valid JSON formatted like this:\n{“answer”: “<put free text answer here>“}‘, output=’{“id”: “chatcmpl-9CGKXHZPuVcFXJoY7OEOETotJrN4o”, “choices”: [{“finish_reason”: “stop”, “index”: 0, “logprobs”: null, “message”: {“content”: “```json\\n{\\“answer\\“: \\“I\‘m doing well, thank you for asking! How can I assist you today?\\“}\\n```“, “role”: “assistant”, “function_call”: null, “tool_calls”: null}}], “created”: 1712709737, “model”: “gpt-4-1106-preview”, “object”: “chat.completion”, “system_fingerprint”: “fp_d6526cacfe”, “usage”: {“completion_tokens”: 26, “prompt_tokens”: 68, “total_tokens”: 94}}’, iteration=0, timestamp=1712709738)}, immediate_write=True, remote=False)
```
For more details see new documentation on <a href="https://docs.expectedparrot.com/en/latest/data.html">Caching LLM Calls</a>.

<i>Coming soon: Automatic remote caching options.</i>

- <b>API keys:</b> 
You will no longer be prompted to enter your API keys when running a session. We recommend storing your keys in a private `.env` file in order to avoid having to enter them at each session. Alternatively, you can still re-set your keys whenever you run a session. See instructions on setting up an `.env` file in our <a href="https://docs.expectedparrot.com/en/latest/starter_tutorial.html#part-1-using-api-keys-for-llms">Starter Tutorial</a>.

<i>The Expected Parrot API key is coming soon! It will let you access all models at once and come with automated remote caching of all results. If you would like to test it out, please let us know!</i>

- <b>Prompts:</b> 
We made it easier to modify the agent and question prompts that are sent to the models.
For more details see new documentation on <a href="https://docs.expectedparrot.com/en/latest/prompts.html">Prompts</a>.

### Deprecated
- `Model` attribute `use_cache` is now deprecated. See details above about how caching now works.

### Removed

### Fixed
- `.run(n = ...)` now works and will run your survey with fresh results the specified number of times.


