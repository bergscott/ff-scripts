import random

class League(object):
    def __init__(self, name):
        """
        create a new League object and give it name name. Initialize empty dicts
        for teams and divisions.

        name: a string
        """
        self.name = str(name)
        self.teams = {}
        self.divisions = set()
        
    def get_name(self):
        """
        Return the name of the League.

        returns: a string
        """
        return self.name
    
    def set_name(self, name):
        """
        Set the name of the league to NAME.

        name: a string
        """
        self.name = name
        
    def create_team(self, team_name):
        """
        Instantiates a new Team object and sets its name to TEAM_NAME.
        Adds key of TEAM_NAME to self.names and sets its value to the new
        Team object.

        team_name: a string 
        """
        self.teams[team_name] = Team(team_name)
        
    def remove_team(self, team_name):
        """
        If TEAM_NAME is key in self.teams, deletes that entry from self.teams,
        otherwise raises error.

        team_name: a string in self.teams.keys()
        """
        if team_name in self.teams:
            del self.teams[team_name]
        else: raise ValueError(team_name + ' is not in league.')
        
    def get_team(self, team_name):
        """
        Return the Team object in self.teams with name attribute TEAM_NAME.

        team_name: a string in self.teams.keys()
        Returns: a Team object
        """
        try:
            return self.teams[team_name]
        except:
            raise ValueError(team_name + ' is not in League.')
        
    def get_team_dict(self):
        """
        Return the dictionary of teams in the league.
        
        returns: a dict
        """
        return self.teams
    
    def add_division(self, division_name):
        """
        Adds an entry to the self.divisions set with DIVISION_NAME

        division_name: a string
        """
        self.divisions.add(division_name)
        
    def remove_division(self, division_name):
        """
        Deletes entry with key DIVISON_NAME from self.divisions set.

        division_name: a string in self.divisions
        """
        if division_name in self.divisions:
            self.divisions.remove(division_name)
        else: raise ValueError(division_name + ' is not a division in league.')
        
    def get_divisions(self):
        """
        Returns a dict of division name and list of division members pairs

        returns: a dict
        """
        divisions = {}
        for d in self.divisions:
            divisions[d] = []
        for t in self:
            try: divisions[t.get_division()].append(t.get_name())
            except KeyError:
                if '<Not Assigned>' in divisions:
                    divisions['<Not Assigned>'].append(t.get_name())
                else: divisions['<Not Assigned>'] = [t.get_name(),]
        return divisions

    def shuffle_divisions(self):
        """
        Randomly evenly assigns divisions from self.divisions to teams in
        self.teams.
        Mutates the name attributes of the Team objects in self.teams
        """
        # map divisions to size (number of teams in division (initial: 0))
        divisions = {}
        for d in self.divisions:
            divisions[d] = 0  
        # calculate maximum division size
        max_teams = len(self.teams) / len(divisions)
        large_divs_remaining = len(self.teams) % len(divisions)
        if large_divs_remaining > 0: max_teams += 1
        # randomly assign a division to each team, update dict
        for t in self:
            d = random.choice(divisions.keys())
            t._set_division(d)
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
        """
        Sets the division attribute of the Team object with name TEAM_NAME in
        self.teams to DIVISION_NAME. Checks to make sure division is found in
        self.divisions and if not, raises error.
        
        team_name: a string in self.teams.keys()
        division_name: a string in self.divisions.keys()
        """
        try:
            if division_name in self.divisions:
                self.teams[team_name]._set_division(division_name)
            else: raise ValueError(division_name +
                    ' is not a division in league')
        except KeyError:
            raise ValueError(team_name + ' is not in League')
    
    def generate_schedule(self, weeks):
        """
        Creates a regular season schedule of WEEKS number of weeks
        for the league. Teams are matched once against each team in their
        division and then once against each team outside their division,
        if there are weeks reamaining, the process repeats until
        all weeks are filled. Number of teams in league must be even.

        weeks: an int
        returns: a list of lists of matchups. (each list of matchups is a week
        in the season).
        """
        schedule = []
        divisions = self.get_divisions()
        # initialize matchupFreqs dict
        matchupFreqs = {}
        for team in self:
            matchupFreqs[str(team)] = {}
            for opponent in self:
                if not opponent == team:
                    matchupFreqs[str(team)][str(opponent)] = {}
                    matchupFreqs[str(team)][str(opponent)]['home'] = 0
                    matchupFreqs[str(team)][str(opponent)]['away'] = 0
                
        for w in xrange(1, weeks+1):
            schedule.append(self._generate_week(divisions, matchupFreqs,
                                                w, weeks))
        return schedule

    def _generate_week(self, divisions, matchupFreqs, weekNum, totalWeeks):
        """
        Generates a list of matchups representing a week schedule. Modifies
        matchupFreqs to reflect returned matchups.

        matchupFreqs: a dict of dicts of dicts. (each team is a key in the top
        dict, which contains a dict with a key for each possible opponent, 
        whose value is a dict with two keys: 'home' and 'away'.  The values
        for 'home' and 'away' are ints representing the frequency of this
        matchup.
        e.g. matchupFreqs['Team 1']['Team 2']['home'] = 1, represents one 
        matchup of Team 1 vs Team 2, where Team1 is the home team. In this case,
        matchupFreqs['Team 2']['Team 1']['away'] will also equal 1.
        
        weekNum: an int
        totalWeeks: an int
        returns: a list of Matchups
        modifies: matchupFreqs
        """
        maxMatchups = (weekNum // len(self.teams)) + 1
        divisionSize = len(self.teams) / len(divisions)
        usedDict = {}
        for team in self.teams.keys():
            usedDict[team] = False
        if 0 < (weekNum % (len(self.teams) - 1)) < divisionSize:
            return self._get_divisional_matchups(divisions, matchupFreqs,
                                                 maxMatchups)
        else:
            assert sum(usedDict.values()) == 0
            return self._get_interdivisional_matchups_v3(divisions, 
                    matchupFreqs, maxMatchups, usedDict, [])
        
    def _get_divisional_matchups(self, divisions, matchupFreqs, maxMatchups):
        matchupList = []
        for d in divisions.keys():
            availableTeams = divisions[d][:]
            for team in availableTeams:
                availableTeams.remove(team)
                validMatchups = self._get_valid_matchups(team, availableTeams,
                                                         matchupFreqs, 
                                                         maxMatchups)
                toAdd = random.choice(validMatchups)
                self._add_matchup(team, toAdd, matchupList, matchupFreqs)
                availableTeams.remove(toAdd[0])
        return matchupList

##    def _get_interdivisional_matchups(self, divisions, matchupFreqs, 
##                                      maxMatchups):
##        matchupList = []
##        availableTeams = self.teams.keys()
##        for team in availableTeams:
##            print team
##            availableTeams.remove(team)
##            tempAvail = availableTeams[:]
##            for divTeam in divisions[self.get_team(team).get_division()]:
##                try: tempAvail.remove(divTeam)
##                except ValueError: pass
##            print str(len(tempAvail)) + ' to choose from'
##            validMatchups = self._get_valid_matchups(team, tempAvail,
##                                                     matchupFreqs, maxMatchups)
##            print str(len(validMatchups)) + ' are valid.'
##            toAdd = random.choice(validMatchups)
##            print toAdd
##            self._add_matchup(team, toAdd, matchupList, matchupFreqs)
##            availableTeams.remove(toAdd[0])
##            print str(len(availableTeams)) + ' available teams.'
##        return matchupList
##
##    def _get_interdivisional_matchups_v2(self, divisions, matchupFreqs, 
##                                          maxMatchups):
##       matchupList = []
##       usedDict = {}
##       for team in self.teams.keys():
##           usedDict[team] = False
##        for team in self:
##            if usedDict[str(team)] == True:
##                continue
##            usedDict[str(team)] = True
##            tempAvail = []
##            for tempTeam in self:
##                if usedDict[str(tempTeam)] == False and \
##                        tempTeam not in divisions[team.get_division()]:
##                    tempAvail.append(tempTeam)
##            validMatchups = self._get_valid_matchups(team, tempAvail,
##                                                     matchupFreqs, maxMatchups)
##            toAdd = random.choice(validMatchups)
##            self._add_matchup(team, toAdd, matchupList, matchupFreqs)
##            usedDict[str(toAdd[0])] = True
##        return matchupList
##
    def _get_interdivisional_matchups_v3(self, divisions, matchupFreqs,
                                         maxMatchups, usedDict, ignoreList):
        currentTeam = None
        for team in self:
            if usedDict[str(team)] == False:
                currentTeam = team
                break
        if currentTeam == None:
            return []
        else:
            print 'current team: ' + str(currentTeam)
            tempUsedDict = usedDict.copy()
            tempUsedDict[str(team)] = True
            tempAvail = []
            for team in self:
                if tempUsedDict[str(team)] == False and \
                        team not in divisions[currentTeam.get_division()] and \
                        team not in ignoreList:
                    tempAvail.append(team)
            validMatchups = self._get_valid_matchups(currentTeam, tempAvail,
                                                     matchupFreqs, maxMatchups)
            print str(len(ignoreList)) + ' to ignore.'
            print 'available teams: ' + str(len(tempAvail))
            print 'valid teams: ' + str(len(validMatchups))
            if validMatchups == []:
                print 'reached end, returning False'
                return False
            else:
                tempMatchupFreqs = matchupFreqs.copy()
                toAdd = random.choice(validMatchups)
                matchup = self._create_matchup(currentTeam, toAdd, 
                                               tempMatchupFreqs)
                tempUsedDict[str(toAdd[0])] = True
                recurse = self._get_interdivisional_matchups_v3(divisions,
                        tempMatchupFreqs, maxMatchups, tempUsedDict, [])
                if recurse == False:
                    ignoreList.append(toAdd[0])
                    return self._get_interdivisional_matchups_v3(divisions,
                            matchupFreqs, maxMatchups, usedDict, ignoreList)
                elif type(recurse) == list:
                    return [matchup,] + recurse

    def _create_matchup(self, team, toAdd, matchupFreqs):
        if toAdd[1] == 'home':
            self._update_matchup_freqs(team, toAdd[0], matchupFreqs)
            return Matchup(team, toAdd[0])
        else:
            self._update_matchup_freqs(toAdd[0], team, matchupFreqs)
            return Matchup(toAdd[0], team)

    def _add_matchup(self, team, toAdd, matchupList, matchupFreqs):
        if toAdd[1] == 'home':
            matchupList.append(Matchup(team, toAdd[0]))
            self._update_matchup_freqs(team, toAdd[0], matchupFreqs)
        else:
            matchupList.append(Matchup(toAdd[0], team))
            self._update_matchup_freqs(toAdd[0], team, matchupFreqs)

    def _get_valid_matchups(self, team, teamList, matchupFreqs, maxMatchups):
        """
        Returns a list of tuples consisting of an opponent and 'home' or 'away'
        representing all possible matchups between team and teamList that could
        be scheduled.

        team: a Team object
        teamList: a list of Team objects
        matchupFreqs: a dict (see _generate_week for explaination
        maxMatchups: an int
        returns: a list of tuples (Team, str)
        """
        result = []
        for opponent in teamList:
            test = self._check_matchup(team, opponent, matchupFreqs, maxMatchups)
            if test != False:
                result.append((opponent, test))
        return result

    def _check_matchup(self, team, opponent, matchupFreqs, maxMatchups):
        """
        Checks matchupFreqs dictionary to see if a matchup is suitable to
        schedule based on maxMatchups.  If team and opponent have played
        each other more or equal times than MAXMATCHUPS, returns False,
        otherwise returns 'home' or 'away' based on which matchup has occured
        less. Tie goes to 'home'.

        team: a Team object
        opponent: a Team object
        matchupFreqs: a dict (see _generate_week for explaination)
        maxMatchups: an int
        returns: one of: False or str ('home' or 'away')
        """
        homeMatchups = matchupFreqs[str(team)][str(opponent)]['home']
        awayMatchups = matchupFreqs[str(team)][str(opponent)]['away']
        if homeMatchups + awayMatchups >= maxMatchups:
            return False
        elif homeMatchups <= awayMatchups:
            return 'home'
        else:
            return 'away'

    def _update_matchup_freqs(self, home, away, matchupFreqs):
        matchupFreqs[str(home)][str(away)]['home'] += 1
        matchupFreqs[str(away)][str(home)]['away'] += 1


        
    def __iter__(self):
        """
        Yields each Team object in self.teams
        """
        for t in self.teams.values():
            yield t
            
    def __str__(self):
        """
        Returns a string representation of the league containing its name and
        teams sorted by their divisions.  If a team in self.teams has no
        division or a division not in self.divisions, it is sorted under
        '<Not Assigned>'.

        returns: a string
        """
        result = 'League Name: ' + self.name + '\nTeams and Divisions:\n'
        divisions = self.get_divisions()
        sorted_divs = sorted(divisions.keys(), key=str.lower)
        for d in sorted_divs:
            result = result + 'Division Name: ' + d + '\n'
            if len(divisions[d]) > 0:
                for t in divisions[d]:
                    result = result + '\t' + t + '\n'
            else: result = result + '\t<empty>\n'
        return result[:-1]
            
class Team(object):
    """
    Represents a fantasy sports team in a league.
    Teams should be created within League objects with the League.create_team
    method.
    """
    def __init__(self, name):
        """
        Initializes a Team with the given name and sets its initial owner and
        division to None

        name: a string
        """
        self.name = str(name)
        self.owner = None
        self.division = None

    def get_name(self):
        """
        Returns the name of the team.

        returns: a string
        """
        return self.name

    def set_owner(self, owner):
        """
        Sets the name of the team's owner to OWNER.

        owner: a string
        """
        self.owner = str(owner)

    def get_owner(self):
        """
        Returns the name of the owner of the team.

        returns: a string
        """
        return self.owner    
    
    def _set_division(self, division):
        """
        Sets which division the team belongs to. Should only be called by
        methods in a League object to maintain compatibility.
        
        division: a string
        """
        self.division = division               

    def get_division(self):
        """
        Returns the name of the division the team belongs to.

        returns: a string
        """
        return self.division    

    def __str__(self):
        """
        Returns a string representation of a Team (its name)

        returns: a string
        """
        return self.name

class Matchup(object):
    def __init__(self, home, away):
        """
        Initialize a Matchup object representing a matchup between fantasy
        teams with home team, HOME, and away team, AWAY.

        home: a Team object
        away: a Team object
        """
        self.homeTeam = home
        self.awayTeam = away
        self.homeScore = None
        self.awayScore = None

    def __str__(self):
        """
        Returns a string representation of a Matchup.

        returns: a string
        """
        return str(self.awayTeam) + ' at ' + str(self.homeTeam)

def print_schedule(schedule):
    for week in range(1, len(schedule)+1):
        print 'Week ' + str(week)
        if schedule[week-1] == False:
            print 'FALSE!'
        else:
            for game in schedule[week-1]:
                    print game

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
print_schedule(grassmasters.generate_schedule(14))
