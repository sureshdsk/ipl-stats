from flask import Flask, request, render_template
from stats import IplStats

app = Flask(__name__, template_folder='templates')
stats = IplStats()


@app.route('/')
def home():
    all_seasons = stats.get_all_seasons()
    chosen_season = int(request.args.get("season", 0))
    context = {
        "chosen_season": chosen_season,
        "all_seasons": all_seasons
    }
    if chosen_season:
        context.update({
            "top_4_teams": stats.top_successful_teams(chosen_season, 4),
            "most_toss_wins": stats.most_toss_wins(chosen_season),
            "most_man_of_the_match": stats.most_man_of_the_match(chosen_season),
            "max_match_wins": stats.top_successful_teams(chosen_season, 1),
            "percentage_toss_decisions": stats.toss_win_batting(chosen_season),
            "location_hosted_max_matches": stats.location_hosted_max_matches(chosen_season),
            "won_by_highest_margin": stats.won_by_highest_margin(chosen_season),
            "top_team_wins_by_location": stats.top_team_wins_by_location(chosen_season),
        })

    return render_template('home.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
