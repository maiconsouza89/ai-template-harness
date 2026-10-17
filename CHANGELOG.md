# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.

Formato: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versionamento: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Fundação do repositório: EditorConfig, atributos de texto, hook `commit-msg`, ADRs e guia de contribuição.
- Nomes de branch no formato `<tipo>/<descricao>`, validados por `make check-branch`.
- CI agnóstica: workflows `ci` (`make check`, gitleaks) e `pr-title`, contrato de alvos `lint`, `format`, `test`, `build`.
- Harness para agentes: `AGENTS.md`, `CLAUDE.md`, `Makefile` com `make check`, e `docs/ARCHITECTURE.md`, `SETUP.md`, `TESTING.md`.
