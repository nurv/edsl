from edsl.data.CacheEntry import CacheEntry
import time
import pytest

def test_eq():
    entry1 = CacheEntry.example()
    entry2 = CacheEntry.example()
    assert entry1 == entry2

    entry2.timestamp = int(time.time()) + 1
    assert entry1 != entry2

def test_example_dict():
    example_dict = CacheEntry.example_dict()
    assert len(example_dict) == 1
    key = list(example_dict.keys())[0]
    assert key == CacheEntry.example().key

def test_fetch_input_example():
    fetch_input = CacheEntry.fetch_input_example()
    assert 'timestamp' not in fetch_input
    assert 'output' not in fetch_input
    assert all(field in fetch_input for field in CacheEntry.key_fields)

def test_store_input_example():
    store_input = CacheEntry.store_input_example()
    assert 'timestamp' not in store_input
    assert 'response' in store_input
    assert 'output' not in store_input
    assert all(field in store_input for field in CacheEntry.key_fields + ['response'])

def test_gen_key():
    key = CacheEntry.gen_key(
        model="gpt-3.5-turbo",
        parameters="{'temperature': 0.5}",
        system_prompt="The quick brown fox jumps over the lazy dog.",
        user_prompt="What does the fox say?",
        iteration=1
    )
    assert key == '55ce2e13d38aa7fb6ec848053285edb4'

def test_key_property():
    entry = CacheEntry.example()
    assert entry.key == '55ce2e13d38aa7fb6ec848053285edb4'

def test_to_dict():
    entry = CacheEntry.example()
    entry_dict = entry.to_dict()
    assert all(field in entry_dict for field in CacheEntry.all_fields)
    assert entry_dict['model'] == entry.model
    assert entry_dict['parameters'] == entry.parameters
    assert entry_dict['system_prompt'] == entry.system_prompt
    assert entry_dict['user_prompt'] == entry.user_prompt
    assert entry_dict['output'] == entry.output
    assert entry_dict['iteration'] == entry.iteration
    assert entry_dict['timestamp'] == entry.timestamp

def test_from_dict():
    entry_dict = CacheEntry.example().to_dict()
    entry = CacheEntry.from_dict(entry_dict)
    assert isinstance(entry, CacheEntry)
    assert all(getattr(entry, field) == entry_dict[field] for field in CacheEntry.all_fields)

def test_repr():
    entry = CacheEntry.example()
    expected_repr = f"CacheEntry(model={entry.model}, parameters={entry.parameters}, system_prompt={entry.system_prompt}, user_prompt={entry.user_prompt}, output={entry.output}, iteration={entry.iteration}, timestamp={entry.timestamp})"
    assert repr(entry) == expected_repr