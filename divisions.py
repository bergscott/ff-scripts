class League(object):
    def __init__(self, name):
        self.name = str(name)
        self.teams = {}
        self.divisions = {}
        
    def get_name(self):
        return self.name
    
    def add_team(self, team):
        self.teams[str(team)] = team
        
    def remove_team(self, team_name):
        team = self.teams[team_name]
        if team_name in self.teams:
            if not team.get_division() == None:
                team.get_division().remove_team(team)
            del self.teams[team_name]
        else: raise ValueError(str(team) + ' is not in league.')
        
    def get_team(self, team_name):
        try:
            return self.teams[team_name]
        except:
            raise ValueError(team_name + ' is not in League.')

    def get_teams(self):
        return self.teams
    
    def add_division(self, division):
        self.divisions[division.get_name()] = division
        
    def remove_division(self, division_name):
        if division_name in self.divisions:
            self.divisions[division_name].clear_teams()
            del self.divisions[division_name]
        else: raise ValueError(str(team) + ' is not in league.')
        
    def get_division(self, division_name):
        try:
            return self.divisions[division_name]
        except:
            raise ValueError(division_name + ' is not in League.')
        
    def shuffle_divisions(self):
        divs = []
        for d in self.divisions.values():
            d.clear_teams()
            divs.append(d)
        max_teams = len(self.teams) / len(divs)
        balanced = len(self.teams) % len(divs) == 0
        if not balanced: max_teams += 1
        for t in self:
            d = random.choice(divs)
            d.add_team(t)
            if len(d.get_teams()) >= max_teams:
                divs.remove(d)
                if not balanced:
                    max_teams -= 1
                    balanced = True

    def assign_team_to_division(self, team_name, division_name):
        try:
            self.divisions[division_name].add_team(self.teams[team_name])
        except KeyError:
            raise ValueError('Invalid team_name or division_name')
            
    def __iter__(self):
        for t in self.teams.values():
            yield t
            
    def __str__(self):
        result = 'League: ' + self.name + '\n'
        for d in self.divisions.values():
            result = result + '\t' + str(d) + '\n'
        return result[:-1]
    
class Division(League):
    def clear_teams(self):
        for t in self: self.remove_team(t)

    def add_team(self, team):
        team.set_division(self)
        self.teams[str(team)] = team

    def remove_team(self, team):
        if str(team) in self.teams:
            team.clear_division()
            del self.teams[str(team)]
        else: raise ValueError(str(team) + ' is not in league.')
        
    def __str__(self):
        result = 'Division: ' + self.name + '\n'
        for t in self:
            result = result + '\t-' + str(t) + '\n'
        return result[:-1]

class Team(object):
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.division = None
        
    def set_owner(self, owner):
        self.owner = owner
        
    def get_owner(self):
        return self.owner
    
    def set_division(self, division):
        if not self.division == None: self.division.remove_team(self)
        self.division = division
        
    def clear_division(self):
        self.division = None
        
    def get_division(self):
        return self.division
    
    def __str__(self):
        return self.name

grassmasters = League('Frozen Grassmasters of Lambeau')
grassmasters.add_team(Team('Training Camp Hookie'))
grassmasters.add_team(Team('T-bone Chicken'))
grassmasters.add_team(Team('Dark Helmet'))
grassmasters.add_team(Team('Wish Sandwiches'))

grassmasters.add_team(Team('Flaming Moes'))
grassmasters.add_team(Team('Jello Puddin\' Pops'))
grassmasters.add_team(Team('The Schlubs'))
grassmasters.add_team(Team('Kentucky Clears'))

grassmasters.add_team(Team('Mother of Dragons'))
grassmasters.add_team(Team('Demaryius Targaryen'))
grassmasters.add_team(Team('Winter is Coming'))
grassmasters.add_team(Team('King in the North'))

grassmasters.add_division(Division('Beer'))
grassmasters.add_division(Division('Cheese'))
grassmasters.add_division(Division('Sausage'))

grassmasters.shuffle_divisions()

print grassmasters

