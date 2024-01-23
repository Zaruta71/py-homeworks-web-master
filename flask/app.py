from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Session, User, CreateUserModel, Ad
from validator import validate

app = Flask('app')


class UserView(MethodView):

    def get(self):
        pass

    def post(self):
        user_data = request.json
        with Session() as session:
            register_data = validate(request.json, CreateUserModel)
            return User.register(session, **register_data).to_dict()


class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = session.query(Ad).filter(Ad.id == request.headers.get(ad_id).all())
            return jsonify(ad.to_dict())

    def post(self):
        ad_data = request.json
        with Session() as session:
            new_ad = Ad(title=ad_data['title'], body=ad_data['body'],
                        owner_id=ad_data['owner_id'])
            session.add(new_ad)
            session.commit()
            return jsonify(new_ad.to_dict())


    def delete(self, ad_id: int):
        with Session() as session:
            ad = session.query(Ad).filter(Ad.id == request.headers.get(ad_id).all())
            session.delete(ad)
            session.commit()


app.add_url_rule("/user/", view_func=UserView.as_view("register_user"), methods=["POST"])
app.add_url_rule("/ad/", view_func=AdView.as_view("post_ad"), methods=["POST"])
app.add_url_rule("/ad/<int:ad_id>", view_func=AdView.as_view("get_ad"), methods=["GET"])
app.add_url_rule("/ad/<int:ad_id>", view_func=AdView.as_view("del_ad"), methods=["DELETE"])

if __name__ == '__main__':
    app.debug = True
    app.run()
