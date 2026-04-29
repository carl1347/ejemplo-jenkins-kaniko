from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
}

swagger_template = {
    "info": {
        "title": "Greeting API",
        "description": "A simple API to set and retrieve a greeting name.",
        "version": "1.0.0",
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

current_name = None


@app.route("/greeting", methods=["POST"])
def set_greeting():
    """
    Set the greeting name.
    ---
    tags:
      - Greeting
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Alice
    responses:
      200:
        description: Name saved successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Name 'Alice' saved"
      400:
        description: Missing name field
        schema:
          type: object
          properties:
            error:
              type: string
              example: name is required
    """
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    global current_name
    current_name = data["name"]
    return jsonify({"message": f"Name '{current_name}' saved"}), 200


@app.route("/greeting", methods=["GET"])
def get_greeting():
    """
    Get the current greeting.
    ---
    tags:
      - Greeting
    responses:
      200:
        description: A greeting message
        schema:
          type: object
          properties:
            greeting:
              type: string
              example: "Hello, Alice!"
    """
    if current_name:
        return jsonify({"greeting": f"Hello, {current_name}!"}), 200
    return jsonify({"greeting": "Hello, stranger!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
