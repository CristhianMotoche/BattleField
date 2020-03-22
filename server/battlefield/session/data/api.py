from http import HTTPStatus

from quart import jsonify
from quart_openapi import Resource, PintBlueprint

from ..domain.use_cases.creator import SessionCreator
from ..domain.use_cases.lister import SessionLister
from .data_access import SessionDataAccess
from .presenters import SessionPresenter


# TODO: Separate in to modules to use __name__:
# - Multiple sessions
# - Single sessions
sessions = PintBlueprint("multi_session", "sessions")

resp_obj = {
    "type": "array",
    "items": {
        "type": "Session",
    }
}
resp = sessions.create_validator("response", resp_obj)


@sessions.route("/sessions")
class Sessions(Resource):
    async def post(self):
        saver = SessionDataAccess()
        creation_result = await SessionCreator(saver).create()
        result = SessionPresenter(creation_result).to_dict()
        return jsonify(result)

    @sessions.response(HTTPStatus.OK, "OK", resp)
    async def get(self, session_id=None):
        da = SessionDataAccess()
        if session_id:
            return jsonify({})
        sessions = await SessionLister(da).list()
        return jsonify(sessions)


session = PintBlueprint("single_session", "session")


@session.route("/sessions/<int:id>")
class Session(Resource):
    async def post(self, id):
        return jsonify({})

    async def get(self, id):
        return jsonify({})
