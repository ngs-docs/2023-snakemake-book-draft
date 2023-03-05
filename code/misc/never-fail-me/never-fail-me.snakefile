rule always_succeed:
    shell: """
        ./does-not-exist.sh || true
    """
