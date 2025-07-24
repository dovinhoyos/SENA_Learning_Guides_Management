from shared.config import create_app
from auth.infra.auth_routes import auth_bp
from guides.infra.flask_routes import guides_bp

app = create_app()
app.register_blueprint(auth_bp)
app.register_blueprint(guides_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
