# Changelog

## [Unreleased]

## [v1.2.0] - 2023-01-14

### Added

- Lint checks that ensure `patch` is called with any one or more of the `new`,
  `spec`, `spec_set`, `autospec` or `new_callable` arguments

### Fix

- Ensure that error codes are correctly mapped for `NonCallableMock` and
  `AsyncMock` which were mapped to the `MagicMock` code before

### Changed

- Changed codes for mock checks:
   - `Mock`: `TMS001` -> `TMS010`,
   - `MagicMock`: `TMS002` -> `TMS011`,
   - `NonCallableMock`: `TMS003` -> `TMS012` and
   - `AsyncMock`: `TMS004` -> `TMS013`.

## [v1.1.0] - 2023-01-14

### Added

- Lint checks that ensure `NonCallableMock` and `AsyncMock` constructors have
  the `spec` or `spec_set` argument

## [v1.0.0] - 2023-01-14

### Added

- Lint checks that ensure `Mock` and `MagicMock` constructors have the `spec`
  or `spec_set`argument

[//]: # "Release links"
[v1.0.0]: https://github.com/jdkandersson/flake8-mock-spec/releases/v1.0.0
[v1.1.0]: https://github.com/jdkandersson/flake8-mock-spec/releases/v1.1.0
[v1.2.0]: https://github.com/jdkandersson/flake8-mock-spec/releases/v1.2.0
