from __future__ import annotations

from flask import Flask, g, redirect, request, session, url_for

from app.config import Config
from app.club_assets import club_logo_url
from app.extensions import csrf, db
from app.i18n import get_locale, t
from app.security import current_user


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    csrf.init_app(app)

    from app.admin.routes import bp as admin_bp
    from app.auth.routes import bp as auth_bp
    from app.clubs.routes import bp as clubs_bp
    from app.main.routes import bp as main_bp
    from app.reservations.routes import bp as reservations_bp
    from app.rooms.routes import bp as rooms_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(clubs_bp, url_prefix="/clubs")
    app.register_blueprint(rooms_bp, url_prefix="/rooms")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.cli import register_cli

    register_cli(app)

    @app.before_request
    def load_request_context() -> None:
        g.locale = get_locale()
        g.user = current_user()

    @app.context_processor
    def inject_helpers() -> dict[str, object]:
        return {
            "current_user": g.get("user"),
            "locale": g.get("locale", "pl"),
            "t": t,
            "club_logo_url": club_logo_url,
        }

    @app.route("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok", "service": "studentspot"}, 200

    @app.route("/set-language/<lang>")
    def set_language(lang: str):
        if lang not in {"pl", "en"}:
            lang = "pl"
        session["lang"] = lang
        return redirect(request.referrer or url_for("main.index"))

    return app
