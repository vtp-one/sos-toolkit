import python_on_whales as POW

def get_client(**kwargs):
    #
    # TODO
    # - check if client is valid
    # - handle docker in docker
    # - download client if we need it
    # - check docker_socket
    # - permissions / registry identities / whatever
    # - do we have compose / buildx
    # - could be handled by the sandbox container?

    return POW.DockerClient(**kwargs)