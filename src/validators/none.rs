use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::errors::{ErrorType, ValError, ValResult};
use crate::input::Input;
use crate::recursion_guard::RecursionGuard;

use super::{BuildValidator, CombinedValidator, Definitions, DefinitionsBuilder, Extra, Validator};

#[derive(Debug, Clone)]
pub struct NoneValidator;

impl BuildValidator for NoneValidator {
    const EXPECTED_TYPE: &'static str = "none";

    fn build(
        _schema: &PyDict,
        _config: Option<&PyDict>,
        _definitions: &mut DefinitionsBuilder<CombinedValidator>,
    ) -> PyResult<CombinedValidator> {
        Ok(Self.into())
    }
}

impl_py_gc_traverse!(NoneValidator {});

impl Validator for NoneValidator {
    fn validate<'s, 'data>(
        &'s self,
        py: Python<'data>,
        input: &'data impl Input<'data>,
        _extra: &Extra,
        _definitions: &'data Definitions<CombinedValidator>,
        _recursion_guard: &'s mut RecursionGuard,
    ) -> ValResult<'data, PyObject> {
        match input.is_none() {
            true => Ok(py.None()),
            false => Err(ValError::new(ErrorType::NoneRequired, input)),
        }
    }

    fn different_strict_behavior(
        &self,
        _definitions: Option<&DefinitionsBuilder<CombinedValidator>>,
        _ultra_strict: bool,
    ) -> bool {
        false
    }

    fn get_name(&self) -> &str {
        Self::EXPECTED_TYPE
    }

    fn complete(&mut self, _definitions: &DefinitionsBuilder<CombinedValidator>) -> PyResult<()> {
        Ok(())
    }
}
