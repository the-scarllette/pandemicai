import json
import matplotlib.pyplot as plt


def pie_chart_cures(data):
    labels = ['0', '1', '2', '3', '4']
    sizes = [0 for i in range(5)]

    for run in data:
        sizes[run["cured_diseases"]] += 1

    # Removing 0 sizes
    i = 4
    while i >= 0:
        if sizes[i] <= 0:
            del (sizes[i])
            del (labels[i])
        i -= 1

    plot_pie_chart(labels, sizes)
    return


def plot_pie_chart(labels, sizes):
    total = sum(sizes)

    print("Cure data results")
    print("Total results " + str(total))
    for i in range(len(sizes)):
        print(labels[i] + " - " + str(sizes[i]))

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct=lambda p: '{:.0f}'.format(p * total / 100),
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.show()
    return


class ResultsManager:

    def __init__(self, file_name):
        self.__file_name = file_name
        self.__returns_sum = 0
        self.__turn_count = 0
        return

    def add_return(self, value):
        self.__returns_sum += value
        return

    def average_graph(self, total_agents):
        with open(self.__file_name) as json_file:
            graph_data = json.load(json_file)

        # Average result
        ave_returns = [[] for i in range(len(graph_data["run_0"]))]
        ave_turns_survived = [[] for i in range(len(graph_data["run_0"]))]

        for k in range(total_agents - 1):
            key = "run_" + str(k)
            for i in range(len(graph_data[key])):
                data = graph_data[key][i]
                ave_returns[i].append(data['return'])
                ave_turns_survived[i].append(data['turn_count'])

        y = [sum(elm) / total_agents for elm in ave_returns]
        x = [i for i in range(len(y))]

        plt.plot(x, y)
        plt.xlabel('run number')
        plt.ylabel('return sum')
        plt.title('Average Return Sum')
        plt.show()

        y = [sum(elm) / total_agents for elm in ave_turns_survived]#
        plt.plot(x, y)
        plt.xlabel('run number')
        plt.ylabel('turns survived')
        plt.title('Average Turns survived')
        plt.show()

        return

    def get_cured_data(self):
        with open(self.__file_name) as json_file:
            graph_data = json.load(json_file)

        cured_array = [0, 0, 0, 0, 0]
        total_runs = 0

        for data in graph_data["run"]:
            cured_array[data["cured_diseases"]] += 1
            total_runs += 1

        print("total runs: " + str(total_runs))
        print(cured_array)
        return

    def graph_and_save(self, filename, agent_num=None):
        with open(self.__file_name) as json_file:
            graph_data = json.load(json_file)

        key = "run"
        if agent_num is not None:
            key += "_" + str(agent_num)

        # Graphing Sum Return
        y = []
        for data in graph_data[key]:
            y.append(data["return"])
        x = [i for i in range(len(y))]

        plt.plot(x, y)
        plt.xlabel('run number')
        plt.ylabel('return sum')
        plt.title('Return Sum')
        # Saving Return Sum Graph
        plt.savefig(filename)

        # Graphing cures as pie chart
        pie_chart_cures(graph_data[key])
        return

    def graph_results(self, agent_num=None):
        with open(self.__file_name) as json_file:
            graph_data = json.load(json_file)

        key = "run"
        if agent_num is not None:
            key += "_" + str(agent_num)

        # Printing number of runs
        print("Number of runs: " + str(len(graph_data[key])))

        self.graph_and_save('return_sum.pdf', agent_num)

        # Graphing turns survived
        y = []
        for data in graph_data[key]:
            y.append(data["turn_count"])
        x = [i for i in range(len(y))]

        plt.plot(x, y)
        plt.xlabel('run number')
        plt.ylabel('Turns Survived')
        plt.title('Turns survived')

        plt.show()
        return

    def increment_turn_count(self):
        self.__turn_count += 1
        return

    def split_graph(self):
        index = 100285 - 40000

        with open(self.__file_name) as json_file:
            graph_data = json.load(json_file)

        # Graphing Sum Return
        y = []
        i = 0
        for data in graph_data["run"]:
            if i >= index:
                y.append(data["return"])
            i += 1
        x = [i for i in range(len(y))]

        plt.plot(x, y)
        plt.xlabel('run number')
        plt.ylabel('return sum')
        plt.title('Return Sum')
        plt.savefig('return_sum_02.pdf')

        # Graphing Cures
        labels_1 = ['0', '1', '2', '3', '4']
        sizes_1 = [0 for i in range(5)]

        i = 0
        for run in graph_data["run"]:
            if i >= index:
                sizes_1[run["cured_diseases"]] += 1
            i += 1

        # Removing 0 sizes
        i = 4
        while i >= 0:
            if sizes_1[i] <= 0:
                del (sizes_1[i])
                del (labels_1[i])
            i -= 1

        plot_pie_chart(labels_1, sizes_1)
        return

    def write_data(self, infected_cities=0, cured_diseases=0, turn_count=0, agent_num=None):
        with open(self.__file_name, 'r') as json_file:
            data = json.load(json_file)

        key = "run"
        if agent_num is not None:
            key += '_' + str(agent_num)
        try:
            data[key].append({'turn_count': turn_count,
                          'infected_cities': infected_cities,
                          'cured_diseases': cured_diseases,
                          'return': self.__returns_sum})
        except KeyError:
            data[key] = [{'turn_count': turn_count,
                          'infected_cities': infected_cities,
                          'cured_diseases': cured_diseases,
                          'return': self.__returns_sum}]

        with open(self.__file_name, 'w') as json_file:
            json.dump(data, json_file)

        return
