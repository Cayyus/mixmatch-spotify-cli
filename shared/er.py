def hide_error(e: str):
    print('\b' * len(e) + ' ' * len(e) + '\b' * len(e), end='', flush=True)
