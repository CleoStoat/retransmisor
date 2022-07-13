def main():
    with open("sample.env") as f:
        keys = [line.split("=")[0] for line in f.readlines()]

    env_vars = {}
    for key in keys:
        value = input(f"{key}=")
        value = value.strip()
        env_vars[key] = value

    env_vars_strings = [f"{key}={value}\n" for key, value in env_vars.items()]

    with open(".env", mode="w") as f:
        f.writelines(env_vars_strings)


if __name__ == "__main__":
    main()
