"""Unit tests."""

import equinox as eqx
import pytest

from oncequinox import SingletonModuleMeta

# =============================================================================
# Fixtures


@pytest.fixture
def singleton_module():
    """Create a basic singleton module class."""

    class TestModule(eqx.Module, metaclass=SingletonModuleMeta):
        value: int = 42

    return TestModule


@pytest.fixture
def singleton_module_with_args():
    """Create a singleton module class that requires init arguments."""

    class TestModuleWithArgs(eqx.Module, metaclass=SingletonModuleMeta):
        value: int

        def __init__(self, value: int):
            self.value = value

    return TestModuleWithArgs


@pytest.fixture
def two_singleton_modules():
    """Create two different singleton module classes."""

    class TestModuleA(eqx.Module, metaclass=SingletonModuleMeta):
        name: str = "A"

    class TestModuleB(eqx.Module, metaclass=SingletonModuleMeta):
        name: str = "B"

    return TestModuleA, TestModuleB


@pytest.fixture
def base_and_derived_modules():
    """Create a base module and a derived module."""

    class BaseModule(eqx.Module, metaclass=SingletonModuleMeta):
        name: str = "base"

    class DerivedModule(BaseModule):
        name: str = "derived"

    return BaseModule, DerivedModule


# =============================================================================
# Tests


def test_basic_singleton(singleton_module):
    """Test that the same instance is returned for multiple calls."""
    # Create two instances
    instance1 = singleton_module()
    instance2 = singleton_module()

    # They should be the same object
    assert instance1 is instance2


def test_singleton_with_init_args(singleton_module_with_args):
    """Test singleton behavior when __init__ has arguments."""
    # First call creates the instance
    instance1 = singleton_module_with_args(42)
    assert instance1.value == 42

    # Second call returns the same instance (args ignored)
    instance2 = singleton_module_with_args(999)
    assert instance2 is instance1
    assert instance2.value == 42  # Original value, not 999


def test_different_classes_different_singletons(two_singleton_modules):
    """Test that different classes have different singleton instances."""
    module_a, module_b = two_singleton_modules

    instance_a = module_a()
    instance_b = module_b()

    # Different classes should have different instances
    assert instance_a is not instance_b
    assert instance_a.name == "A"
    assert instance_b.name == "B"


def test_subclass_has_own_singleton(base_and_derived_modules):
    """Test that subclasses have their own singleton instances."""
    base_module, derived_module = base_and_derived_modules

    base_instance1 = base_module()
    base_instance2 = base_module()
    derived_instance1 = derived_module()
    derived_instance2 = derived_module()

    # Same class should return same instance
    assert base_instance1 is base_instance2
    assert derived_instance1 is derived_instance2

    # Different classes should have different instances
    assert base_instance1 is not derived_instance1


def test_singleton_with_dataclass_fields():
    """Test singleton with various Equinox field types."""

    class ComplexModule(eqx.Module, metaclass=SingletonModuleMeta):
        static_field: int = eqx.field(static=True, default=100)
        converter_field: str = eqx.field(
            converter=str,
            default="test",
        )

    instance1 = ComplexModule()
    instance2 = ComplexModule()

    assert instance1 is instance2
    assert instance1.static_field == 100
    assert instance1.converter_field == "test"


def test_isinstance_check(singleton_module):
    """Test that singleton instances are proper instances of their class."""
    instance = singleton_module()

    assert isinstance(instance, singleton_module)
    assert isinstance(instance, eqx.Module)


def test_type_check(singleton_module):
    """Test that type() returns the correct class."""
    instance = singleton_module()

    assert type(instance) is singleton_module
    # Check that it's a subclass of Module
    assert issubclass(type(instance), eqx.Module)


def test_multiple_inheritance():
    """Test singleton with multiple inheritance."""

    class Mixin:
        def get_value(self) -> int:
            return 42

    class TestModule(Mixin, eqx.Module, metaclass=SingletonModuleMeta):
        pass

    instance1 = TestModule()
    instance2 = TestModule()

    assert instance1 is instance2
    assert instance1.get_value() == 42


def test_singleton_with_kwargs():
    """Test singleton creation with keyword arguments."""

    class TestModule(eqx.Module, metaclass=SingletonModuleMeta):
        x: int
        y: int

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    instance1 = TestModule(x=1, y=2)
    instance2 = TestModule(x=999, y=888)  # Args ignored

    assert instance1 is instance2
    assert instance1.x == 1
    assert instance1.y == 2
