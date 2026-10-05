# Executable Templates and Configuration

- Validate source data before rendering; escape for the actual HTML, JavaScript, URL, shell or serialization context. Avoid string-built executable commands.
- Render valid syntax across supported branches, including empty, missing and malformed inputs. Test generated behavior, not just template text.
- Keep defaults and precedence explicit. Missing required security or production configuration must fail clearly rather than silently enabling an unsafe fallback.
- Verify effective environment/profile values, credentials boundaries and output paths. A test profile or alternate port alone does not prove data/effect isolation.
- For migrations or deployment configuration, verify compatibility, backup prerequisites, bounded success/failure criteria and the supported recovery path.
- Use repository-native schema validators, parsers or dry runs and relevant runtime checks. Read output diffs; generated snapshots do not approve themselves.
