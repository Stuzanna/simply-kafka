Run this command to export the current env definition to a `.yml`, in the pwd.
```bash
conda env export > environment.yml
```

To recreate the same environment on a different machine, copy the `environment.yml` file to the new machine and run the following command:
```bash
conda env create -f environment.yml
```

Can change the name if wish using the `--name` option:
```bash
conda env create --name my_new_env -f environment.yml
```