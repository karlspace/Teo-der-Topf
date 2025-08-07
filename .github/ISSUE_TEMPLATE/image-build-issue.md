---
name: Image Building Issue
about: Report problems with the Raspberry Pi image building process
title: '[IMAGE BUILD] '
labels: ['image-build', 'bug']
assignees: ''

---

## Build Method
<!-- How were you trying to build the image? -->
- [ ] GitHub Actions workflow
- [ ] Manual build script (`./scripts/build_image.sh`)
- [ ] Other (please specify):

## Environment
<!-- If building manually, provide your environment details -->
- **OS**: (e.g., Ubuntu 22.04, Debian 12)
- **Architecture**: (e.g., x86_64, arm64)
- **Available Memory**: (e.g., 8GB)
- **Available Disk Space**: (e.g., 50GB)

## Expected Behavior
<!-- What should have happened? -->

## Actual Behavior
<!-- What actually happened? -->

## Error Output
<!-- Please paste any error messages or logs -->
```
[Paste error output here]
```

## Build Logs
<!-- For GitHub Actions, provide workflow run URL -->
<!-- For manual builds, provide relevant log output -->

## Additional Context
<!-- Any other information that might be relevant -->

## Validation Results
<!-- Please run ./scripts/validate.sh and paste the output -->
```
[Paste validation script output here]
```

## Checklist
- [ ] I have read the [build documentation](../scripts/README.md)
- [ ] I have checked that all prerequisites are installed
- [ ] I have sufficient disk space (at least 20GB free)
- [ ] I have tried building a clean checkout of the repository