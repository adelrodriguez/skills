# skills

My agent skills, one folder each in `skills/<name>/SKILL.md`. [instructions](https://github.com/adelrodriguez/instructions) depends on this package, and [dotagents](https://github.com/adelrodriguez/dotagents) installs both through [APM](https://github.com/microsoft/apm).

## Installing

To install every skill at user scope:

```sh
apm install --global adelrodriguez/skills
```

To install some of them, list them in `apm.yml`:

```yaml
dependencies:
  apm:
    - git: adelrodriguez/skills
      skills: [pr, testing]
```

## Updating

Push the change to `main`, then run `apm update --global` in `~/.apm` to install it.
