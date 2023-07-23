import pytest

from pydantic_core import SchemaValidator


class MyModel:
    # __slots__ is not required, but it avoids __pydantic_fields_set__ falling into __dict__
    __slots__ = '__dict__', '__pydantic_fields_set__', '__pydantic_extra__', '__pydantic_private__'


schema_unique = SchemaValidator(
    {
        'type': 'model',
        'cls': MyModel,
        'schema': {
            'type': 'model-fields',
            'fields': {
                's': {
                    'type': 'model-field',
                    'schema': {'type': 'list', 'unique': True, 'items_schema': {'type': 'str'}},
                }
            },
        },
    }
)
schema_multiple_unique = SchemaValidator(
    {
        'type': 'model',
        'cls': MyModel,
        'schema': {
            'type': 'model-fields',
            'fields': {
                's': {
                    'type': 'model-field',
                    'schema': {
                        'type': 'list',
                        'items_schema': {'type': 'list', 'unique': True, 'items_schema': {'type': 'str'}},
                    },
                }
            },
        },
    }
)


@pytest.mark.benchmark
def test_list_unique_empty(benchmark):
    assert schema_unique.validate_python({'s': []}).s == []
    benchmark(schema_unique.validate_python, {'s': []})


@pytest.mark.benchmark
def test_list_unique_5(benchmark):
    data = list(map(str, range(5)))
    assert schema_unique.validate_python({'s': data}).s == data
    benchmark(schema_unique.validate_python, {'s': data})


@pytest.mark.benchmark
def test_list_unique_50(benchmark):
    data = list(map(str, range(50)))
    assert schema_unique.validate_python({'s': data}).s == data
    benchmark(schema_unique.validate_python, {'s': data})


@pytest.mark.benchmark
def test_list_unique_200(benchmark):
    data = list(map(str, range(200)))
    assert schema_unique.validate_python({'s': data}).s == data
    benchmark(schema_unique.validate_python, {'s': data})


@pytest.mark.benchmark
def test_list_unique_1_000(benchmark):
    data = list(map(str, range(1_000)))
    assert schema_unique.validate_python({'s': data}).s == data
    benchmark(schema_unique.validate_python, {'s': data})


@pytest.mark.benchmark
def test_multiple_list_5(benchmark):
    inner = list(map(str, range(10)))
    data = [inner.copy() for _ in range(5)]
    assert schema_multiple_unique.validate_python({'s': data}).s == data
    benchmark(schema_multiple_unique.validate_python, {'s': data})


@pytest.mark.benchmark
def test_multiple_list_100(benchmark):
    inner = list(map(str, range(10)))
    data = [inner.copy() for _ in range(100)]
    assert schema_multiple_unique.validate_python({'s': data}).s == data
    benchmark(schema_multiple_unique.validate_python, {'s': data})
