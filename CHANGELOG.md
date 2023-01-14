# Changelog

## [Unreleased]

## [v1.2.0] - 2023-01-14

### Added

- Lint checks that ensure `patch` is called with any one or more of the `new`,
  `spec`, `spec_set`, `autospec` or `new_callable` arguments

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
