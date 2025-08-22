from flask import Flask, request, jsonify
from services.match_percentage import get_match_score
from services.skills_analysis import analyze_skills

app = Flask(__name__)

@app.route("/match-percentage", methods=["POST"])
def match_percentage():
    data = request.json
    resume = data.get("resume")
    jd = data.get("job_description")
    result = get_match_score(resume, jd)
    return jsonify(result)

@app.route("/skills-analysis", methods=["POST"])
def skills_analysis():
    data = request.json
    resume = data.get("resume")
    jd = data.get("job_description")
    result = analyze_skills(resume, jd)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
