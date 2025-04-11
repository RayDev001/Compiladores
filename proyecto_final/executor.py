def execute_code(intermediate_code):
    env = {}
    output = []
    for line in intermediate_code:
        try:
            exec(line, {}, env)
        except:
            pass
    for k, v in env.items():
        output.append(f'{k} = {v}')
    return output
