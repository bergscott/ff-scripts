class League(object):
    def __init__(self, name):
        self.name = str(name)
        self.teams = {}
        self.divisions = {}
        
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def create_team(self, team_name):
        self.teams[team_name] = Team(team_name)
        
    def remove_team(self, team_name):
        if team_name in self.teams:
            del self.teams[team_name]
        else: raise ValueError(team_name + ' is not in league.')
        
    def get_team(self, team_name):
        try:
            return self.teams[team_name]
        except:
            raise ValueError(team_name + ' is not in League.')
        
    def get_team_dict(self):
        return self.teams
    
    def add_division(self, division_name):
        self.divisions[division_name] = True
        
    def remove_division(self, division_name):
        if division_name in self.divisions:
            del self.divisions[division_name]
        else: raise ValueError(division_name + ' is not a division in league.')
        
    def get_divisions(self):
            return self.divisions.keys()
        
    def shuffle_divisions(self):
        '''
        randomly evenly assigns divisions from self.divisions to teams in
        self.teams
        '''
        # map divisions to size (number of teams in division (initial: 0))
        divisions = {}
        for d in self.divisions.keys():
            divisions[d] = 0  
        # calculate maximum division size
        max_teams = len(self.teams) / len(divisions)
        large_divs_remaining = len(self.teams) % len(divisions)
        if large_divs_remaining > 0: max_teams += 1
        # randomly assign a division to each team, update dict
        for t in self:
            d = random.choice(divisions.keys())
            t.set_division(d)
            divisions[d] += 1
            # if division is full, remove it from dict, update max size
            if divisions[d] >= max_teams:
                del divisions[d]
                if large_divs_remaining > 1:
                    large_divs_remaining -= 1
                elif large_divs_remaining == 1:
                    max_teams -= 1
                    large_divs_remaining = -1

    def assign_team_to_division(self, team_name, division_name):
        try:
            if division_name in self.divisions:
                self.teams[team_name].set_division(division_name)
            else: raise ValueError(division_name + ' is not a division in league')
        except KeyError:
            raise ValueError(team_name + ' is not in League')
        
    def __iter__(self):
        for t in self.teams.values():
            yield t
            
    def __str__(self):
        result = 'League Name: ' + self.name + '\nTeams and Divisions:\n'
        divisions = {}
        for d in self.divisions.keys():
            divisions[d] = []
        for t in self:
            try: divisions[t.get_division()].append(t.get_name())
            except KeyError:
                if '<Not Assigned>' in divisions:
                    divisions['<Not Assigned>'].append(t.get_name())
                else: divisions['<Not Assigned>'] = [t.get_name(),]
        sorted_divs = sorted(divisions.keys(), key=str.lower)
        for d in sorted_divs:
            result = result + 'Division Name: ' + d + '\n'
            if len(divisions[d]) > 0:
                for t in divisions[d]:
                    result = result + '\t' + t + '\n'
            else: result = result + '\t<empty>\n'
        return result[:-1]
            
class Team(object):
    def __init__(self, name):
        self.name = str(name)
        self.owner = None
        self.division = None
    def get_name(self):
        return self.name
    def set_owner(self, owner):
        self.owner = str(owner)
    def get_owner(self):
        return self.owner    
    def set_division(self, division):
        self.division = division               
    def get_division(self):
        return self.division    
    def __str__(self):
        return self.name

grassmasters = League('Frozen Grassmasters of Lambeau')
grassmasters.create_team('Training Camp Hookie')
grassmasters.create_team('T-bone Chicken')
grassmasters.create_team('Dark Helmet')
grassmasters.create_team('Wish Sandwiches')

grassmasters.create_team('Flaming Moes')
grassmasters.create_team('Jello Puddin\' Pops')
grassmasters.create_team('The Schlubs')
grassmasters.create_team('Kentucky Clears')

grassmasters.create_team('Mother of Dragons')
grassmasters.create_team('Demaryius Targaryen')
grassmasters.create_team('Winter is Coming')
grassmasters.create_team('King in the North')

grassmasters.add_division('Beer')
grassmasters.add_division('Cheese')
grassmasters.add_division('Sausage')

grassmasters.shuffle_divisions()

print grassmasters

