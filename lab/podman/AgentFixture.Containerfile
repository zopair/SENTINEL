FROM python:3.12-alpine
COPY lab/podman/agent_fixture.py /agent_fixture.py
USER 65532:65532
ENTRYPOINT ["python", "-I", "/agent_fixture.py"]
