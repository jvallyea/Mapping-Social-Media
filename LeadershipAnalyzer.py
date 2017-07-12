# Analyzing leadership through news articles in forestry
import csv

class LeadershipAnalyzer():

    def choose_file(self, filename):
        actor_names = []
        with open(filename, 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            raw_actor_names = list(filereader)
        return raw_actor_names

    def generate_names(self, raw_actor_names):
        actor_names = []
        for i in range(len(raw_actor_names)):
            print len(raw_actor_names[i])
            for j in range(len(raw_actor_names[i])):
                if raw_actor_names[i][j] not in [item[0] for item in actor_names]:
                    print raw_actor_names[i][j]
                    actor_names.append([raw_actor_names[i][j], 1])
                elif raw_actor_names[i][j] in [item[0] for item in actor_names]:
                    for k in range(len(actor_names)):
                        if raw_actor_names[i][j] == actor_names[k][0]:
                            actor_names[k][1] += 1

        actor_names = sorted(actor_names, key=lambda x: int(x[1]))
        actor_names = list(reversed(actor_names))

        return actor_names

l_a = LeadershipAnalyzer()
print l_a.generate_names(l_a.choose_file('20170630Actors.csv'))
