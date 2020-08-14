"""
docat
~~~~~

Host your docs. Simple. Versioned. Fancy.

:copyright: (c) 2019 by docat, https://github.com/randombenj/docat
:license: MIT, see LICENSE for more details.
"""

import os
from http import HTTPStatus
from pathlib import Path

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

from docat.docat.utils import create_symlink, extract_archive

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.getenv("DOCAT_DOC_PATH", "/var/docat/doc")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100M


@app.route("/api/projects", methods=["GET"])
def get_projects():
    docs_folder = Path(app.config["UPLOAD_FOLDER"])
    if not docs_folder.exists():
        return (
            {"message": f"Your docat instance is not configured correctly"},
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    return (
        {
            "projects": [
                str(x.relative_to(docs_folder))
                for x in docs_folder.iterdir()
                if x.is_dir()
            ]
        },
        HTTPStatus.OK,
    )


@app.route("/api/projects/<project>", methods=["GET"])
def get_project(project):
    docs_folder = Path(app.config["UPLOAD_FOLDER"]) / project
    if not docs_folder.exists():
        return {"message": f"Project {project} does not exist"}, HTTPStatus.NOT_FOUND

    tags = [x for x in docs_folder.iterdir() if x.is_dir() and x.is_symlink()]

    return (
        {
            "name": project,
            "versions": sorted([
                {
                    "name": str(x.relative_to(docs_folder)),
                    "tags": [
                        str(t.relative_to(docs_folder))
                        for t in tags
                        if t.resolve() == x
                    ],
                }
                for x in docs_folder.iterdir()
                if x.is_dir() and not x.is_symlink()
            ], key=lambda k: k["name"], reverse=True),
        },
        HTTPStatus.OK,
    )


@app.route("/api/<project>/<version>", methods=["POST"])
def upload(project, version):
    if "file" not in request.files:
        return {"message": "No file part in the request"}, HTTPStatus.BAD_REQUEST

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return {"message": "No file selected for uploading"}, HTTPStatus.BAD_REQUEST

    project_base_path = Path(app.config["UPLOAD_FOLDER"]) / project
    base_path = project_base_path / version
    target_file = base_path / secure_filename(uploaded_file.filename)

    # ensure directory for the uploaded doc exists
    base_path.mkdir(parents=True, exist_ok=True)

    # save the upploaded documentation
    uploaded_file.save(str(target_file))
    extract_archive(target_file, base_path)

    return {"message": "File successfully uploaded"}, HTTPStatus.CREATED


@app.route("/api/<project>/<version>/tags/<new_tag>", methods=["PUT"])
def tag(project, version, new_tag):
    source = version
    destination = Path(app.config["UPLOAD_FOLDER"]) / project / new_tag

    if create_symlink(source, destination):
        return (
            {"message": f"Tag {new_tag} -> {version} successfully created"},
            HTTPStatus.CREATED,
        )
    else:
        return (
            {"message": f"Tag {new_tag} would overwrite an existing version!"},
            HTTPStatus.CONFLICT,
        )


# serve_local_docs for local testing without a nginx
if os.environ.get("DOCAT_SERVE_FILES"):

    @app.route("/doc/<path:path>")
    def serve_local_docs(path):
        return send_from_directory(app.config["UPLOAD_FOLDER"], path)
