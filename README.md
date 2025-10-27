<h1 align='center'> oncequinox </h1>
<h2 align="center">Create singleton Equinox modules.</h2>

This is a micro-package, containing the single metaclass `SingletonModuleMeta`.
</br> `SingletonModuleMeta` can be used to create Equinox modules that are
singletons, meaning that only one instance of the module can exist at any given
time.

## Installation

[![PyPI platforms][pypi-platforms]][pypi-link]
[![PyPI version][pypi-version]][pypi-link]

<!-- [![Conda-Forge][conda-badge]][conda-link] -->

```bash
pip install oncequinox
```

## Documentation

[![Actions Status][actions-badge]][actions-link]

### Basic Usage

Create a singleton Equinox module:

```python
import equinox as eqx
from oncequinox import SingletonModuleMeta


class MySingletonModule(eqx.Module, metaclass=SingletonModuleMeta):
    value: str = "this is a singleton module"


# Create the singleton instance
singleton1 = MySingletonModule()

# Attempt to create another instance
singleton2 = MySingletonModule()

print(singleton1 is singleton2)  # True
```

### Singleton Per Class

Different classes maintain separate singleton instances:

```python
import equinox as eqx
from oncequinox import SingletonModuleMeta


class ConfigA(eqx.Module, metaclass=SingletonModuleMeta):
    name: str = "A"


class ConfigB(eqx.Module, metaclass=SingletonModuleMeta):
    name: str = "B"


config_a = ConfigA()
config_b = ConfigB()

print(config_a is config_b)  # False
print(config_a.name)  # A
print(config_b.name)  # B
```

### With Initialization Arguments

Arguments are only used for the first instantiation:

```python
import equinox as eqx
from oncequinox import SingletonModuleMeta


class HasValue(eqx.Module, metaclass=SingletonModuleMeta):
    value: int

    def __init__(self, value: int):
        self.value = value


v1 = HasValue(10)
print(v1.value)  # 10

# Subsequent calls ignore arguments and return existing instance
v2 = HasValue(20)
print(v2.value)  # 10
print(v1 is v2)  # True
```

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/GalacticDynamics/oncequinox/workflows/CI/badge.svg
[actions-link]:             https://github.com/GalacticDynamics/oncequinox/actions
[pypi-link]:                https://pypi.org/project/oncequinox/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/oncequinox
[pypi-version]:             https://img.shields.io/pypi/v/oncequinox

<!-- prettier-ignore-end -->
