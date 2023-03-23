import plotly.express as px
from typing import  Dict, List, Optional


countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Falkland Islands", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"]
colors = ["blue", "green", "red", "yellow"]



class Country():
    def __init__(self) -> None:
        self.countryWithNeighbors: Dict[str,List[str]]= {}
        self.addNeighbors(country='Argentina',neighbor=['Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Uruguay'])
        self.addNeighbors(country='Bolivia', neighbor=['Argentina', 'Brazil', 'Chile', 'Paraguay', 'Peru'])
        self.addNeighbors(country='Brazil',neighbor=['Argentina', 'Bolivia', 'Colombia', 'Guyana', 'Paraguay', 'Peru', 'Suriname','Uruguay', 'Venezuela'])
        self.addNeighbors(country='Chile', neighbor=['Argentina', 'Bolivia', 'Peru'])
        self.addNeighbors(country='Colombia', neighbor=['Brazil', 'Ecuador', 'Peru', 'Venezuela'])
        self.addNeighbors(country='Ecuador', neighbor=['Colombia', 'Peru'])
        self.addNeighbors(country='Falkland Island', neighbor=[])
        self.addNeighbors(country='Guyana', neighbor=['Brazil', 'Suriname', 'Venezuela'])
        self.addNeighbors(country='Paraguay', neighbor=['Argentina', 'Bolivia', 'Brazil'])
        self.addNeighbors(country='Peru', neighbor=['Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador'])
        self.addNeighbors(country='Suriname', neighbor=['Brazil', 'Guyana'])
        self.addNeighbors(country='Uruguay', neighbor=['Argentina', 'Brazil'])
        self.addNeighbors(country='Venezuela', neighbor=['Brazil', 'Colombia', 'Guyana'])

    def addNeighbors(self,country,neighbor):
        self.countryWithNeighbors[country]=neighbor

class ContraintSearch(list[str, str]):
    def __init__(self, variableList, domainList) -> None:
        self.constraintList = {}
        self.variableList = variableList
        self.domainList = domainList
        for var in self.variableList:
            self.constraintList[var] = []
            if var not in self.domainList:
                raise Exception("Country has to be in domains list.")

    def AddContraint(self,countries) -> None:
        for var in countries:
            if var not in self.variableList:
                raise Exception("Country in constraint not in csp variables")
            else:
                self.constraintList[var].append(countries)

    def Check(self,country1,country2, assignedList) -> bool:
        if country1 not in assignedList or country2 not in assignedList:
            return True
        if assignedList[country1] != assignedList[country2]:
            return True
        else:
            return False

    def Relative(self, variable, assignment) -> bool:
        print(variable)
        print(assignment)
        for const in self.constraintList[variable]:
            checkSame = self.Check(const[0],const[1],assignment)
            if checkSame == False:
                return False
        return True


    def BacktrackingSearch(self, assignedList = {}) -> Optional[Dict[str, str]]:

        if len(assignedList) == len(self.variableList):
            return assignedList

        unassignedElement= [item for item in self.variableList if item not in assignedList]
        firstElement = unassignedElement[0]
        for color in self.domainList[firstElement]:
            assignment = assignedList.copy()
            assignment[firstElement] = color
            isRelative = self.Relative(firstElement, assignment)
            if isRelative == True:
                solution= self.BacktrackingSearch(assignment)
                if solution is not None:
                    return solution
        return None


def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[c] for c in countries],
                        scope="south america")
    fig.show()


if __name__ == "__main__":

    country:Country = Country()
    domainList:Dict[str,List[str]] = {}
    for ct in countries:
        domainList[ct] = colors
    print(domainList)
    cs =ContraintSearch(variableList=countries,domainList=domainList)

    for key in country.countryWithNeighbors:
        for item in country.countryWithNeighbors[key]:
            cs.AddContraint([key,item])

    solutionMapProblem = cs.BacktrackingSearch()
    print(solutionMapProblem)
    if solutionMapProblem is None:
        print("Solution cannot be found!")
    else:
        plot_choropleth(colormap=solutionMapProblem)


