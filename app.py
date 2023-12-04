from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set to a random string

# Hardcoded user passwords (in a real app, use a database and hashed passwords)
user_passwords = {
    'Feli': 'Feli2372',
    'Fran': 'FranquitoSal',
    'Facu': 'Facu110kg',
    'Rodri': 'RodriPutin',
    'Teo': 'Tiroteo',
    'Tiago': 'TiagoogaiT',
    'Joaco': 'ComeGordas',
    'Marte': 'Pitodulce',
    'Dami': 'CojeExtranjeras',
    'Pedro': 'PedroVLLC'
}

# Store the votes (in a real app, use a database)
votes = {
    'Feli': {'yes': 0, 'no': 0},
    'Fran': {'yes': 0, 'no': 0},
    'Facu': {'yes': 0, 'no': 0},
    'Rodri': {'yes': 0, 'no': 0},
    'Teo': {'yes': 0, 'no': 0},
    'Tiago': {'yes': 0, 'no': 0},
    'Joaco': {'yes': 0, 'no': 0},
    'Marte': {'yes': 0, 'no': 0},
    'Dami': {'yes': 0, 'no': 0},
    'Pedro': {'yes': 0, 'no': 0}
    # ... initialize for all users
}

user_voted = {username: False for username in user_passwords}

def calculate_multipliers():
    multipliers = {}
    for name, vote_counts in votes.items():
        total_votes = vote_counts['yes'] + vote_counts['no']
        if total_votes > 0:
            multipliers[name] = {
                'yes_multiplier': round(total_votes / (vote_counts['yes'] or 1), 2),
                'no_multiplier': round(total_votes / (vote_counts['no'] or 1), 2)
            }
        else:
            multipliers[name] = {'yes_multiplier': 1, 'no_multiplier': 1}
    return multipliers

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_passwords and user_passwords[username] == password:
            session['username'] = username  # Log in the user
            return redirect(url_for('vote'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if user_voted[session['username']]:  # Check if user has already voted
        return redirect(url_for('results'))

    if request.method == 'POST':
        for name in user_passwords.keys():
            vote = request.form.get(name, 'no')
            votes[name]['yes' if vote == 'yes' else 'no'] += 1
        user_voted[session['username']] = True  # Mark user as having voted
        return redirect(url_for('results'))
    return render_template('vote.html', names=user_passwords.keys())

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))

    remaining_participants = sum(not voted for voted in user_voted.values())
    if remaining_participants == 0:
        multipliers = calculate_multipliers()
    else:
        multipliers = None  # Multipliers are not shown until all votes are in

    return render_template('results.html', votes=votes, multipliers=multipliers, remaining_participants=remaining_participants)

if __name__ == '__main__':
    app.run(debug=True)